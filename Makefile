SHELL := /bin/bash

PYDV_ENV := $(if $(PYDV_ENV),$(PYDV_ENV),$(HOME)/pydv_env)

PKG_REGISTRY_URL = $(CI_API_V4_URL)/projects/$(CI_PROJECT_ID)/packages/generic/archive
DEPLOY_PATH = /usr/gapps/pydv
CI_UTILS = /usr/workspace/weave/ci_utils

RZ_GITLAB = "ssh://git@rzgitlab.llnl.gov:7999"
PROJECT = "weave/pydv.git"

RZ_TESTS_WORKDIR = /usr/gapps/pydv/wsc_tests_workdir
WEAVE_DEVELOP_VENV = /usr/apps/weave/weave-develop-cpu
PYTHON_CMD = $(WEAVE_DEVELOP_VENV)/bin/python3

ifeq ($(SOURCE_ZONE),SCF)
	WEAVE_DEPLOY_GROUP = sduser
else
	WEAVE_DEPLOY_GROUP = llnl_emp
endif
SPACK_WEAVE_VIEW = /usr/workspace/$(WEAVE_DEPLOY_GROUP)/weave/repos/spack/spack_core_environment/0.20/$(LCSCHEDCLUSTER)/local/
ADD_PATH = $(SPACK_WEAVE_VIEW)/bin:$(WEAVE_DEVELOP_VENV)/bin
ADD_PYTHONPATH = $(SPACK_WEAVE_VIEW)/lib/python3.9/site-packages:$(WEAVE_DEVELOP_VENV)/lib/python3.9/site-packages

define do_create_env
	source $(WEAVE_DEVELOP_VENV)/bin/activate && \
	$(PYTHON_CMD) -m venv --system-site-packages $1 && \
	deactivate
	echo export PATH=$(PATH):$(ADD_PATH) >> $1/bin/activate
	echo export PYTHONPATH=$(PYTHONPATH):$(ADD_PYTHONPATH) >> $1/bin/activate
	source $1/bin/activate && \
	which pytest && \
	pip list
endef

define run_pydv_tests
	# call from the top repository directory
	# arg1: full path to venv
	source $1/bin/activate && which pip && which pytest && \
	if [ -z $(DISPLAY) ]; then \
	  xvfb-run --auto-servernum pytest --capture=tee-sys -v tests/; \
	else \
	  pytest --capture=tee-sys -v tests/; \
	fi
endef

define do_run_rz_tests
	# arg1: full path to venv
	source $1/bin/activate && pip list && pwd
	cd tests && ln -s /usr/gapps/pydv/dev/tests/wsc_tests . && cd ..
	if [ -z $(DISPLAY) ]; then \
		xvfb-run --auto-servernum python3 -m pytest tests/wsc_tests/test_*py; \
	else \
		python3 -m pytest -v tests/wsc_tests/test_*py; \
	fi
endef

.PHONY: create_env
create_env:
	$(call do_create_env,$(PYDV_ENV))


.PHONY: run_tests
run_tests:
	@echo "Run tests...";
	$(call run_pydv_tests,$(PYDV_ENV))


.PHONY: run_rz_tests
.ONESHELL:
run_rz_tests:
	echo "Run RZ tests...RZ_TESTS_WORKDIR: $(RZ_TESTS_WORKDIR)"
	$(call do_run_rz_tests,$(PYDV_ENV))


.PHONY: release
release:
	@echo "...create a release....TAG: $(CI_COMMIT_TAG), PKG_REGISTRY_URL: $(PKG_REGISTRY_URL)"; \
	$(eval TAG=$(shell  echo $(CI_COMMIT_TAG) | sed -e "s/^pydv-//")) \
	env; \
	$(CI_UTILS)/bin/release-cli create --name "PyDV $(CI_COMMIT_TAG)" --tag-name $(CI_COMMIT_TAG); \
	tar -cvf $(TAG).tar pydv docs; \
	ls; \
	gzip $(TAG).tar; \
	curl --header "JOB-TOKEN: $(CI_JOB_TOKEN)" --upload-file $(TAG).tar.gz $(PKG_REGISTRY_URL)/$(CI_COMMIT_TAG)/$(TAG).tar.gz

.PHONY: deploy
.ONESHELL:
deploy:
	@echo "...deploy...only run from CI... ";
	$(eval TAG=$(shell  echo $(CI_COMMIT_TAG) | sed -e "s/^pydv-//"))
	wget --header="JOB-TOKEN:$(CI_JOB_TOKEN)" $(PKG_REGISTRY_URL)/$(CI_COMMIT_TAG)/$(TAG).tar.gz -O $(TAG).tar.gz
	give weaveci $(TAG).tar.gz
	$(eval GIVE_USER=$(shell echo ${USER}))
	xsu weaveci -c "sg us_cit" <<AS_WEAVECI_USER
		cd $(DEPLOY_PATH)
		take $(GIVE_USER) -f
		chmod 750 $(TAG).tar.gz
		gunzip $(TAG).tar.gz
		tar -xvf $(TAG).tar
		rm $(TAG).tar
		mv pydv $(TAG)
		mv docs $(TAG)
		chmod -R 750 $(TAG)
		rm -f current
		ln -s $(TAG) current
	AS_WEAVECI_USER


.PHONY: deploy_to_develop
.ONESHELL:
deploy_to_develop:
	$(eval VERSION=`cat $(CI_PROJECT_DIR)/pydv/scripts/version.txt`)
	echo "...deploy_to_develop...VERSION: $(VERSION)"
	cd pydv && rm -rf __pycache__
	rm -f $(VERSION).tar.gz
	tar -cvf $(VERSION).tar * ../docs && gzip $(VERSION).tar
	give --force weaveci $(VERSION).tar.gz
	$(eval GIVE_USER=$(shell echo ${USER}))
	xsu weaveci -c "sg us_cit" <<AS_WEAVECI_USER
		umask 027
		cd $(DEPLOY_PATH)
		mkdir -p $(DEPLOY_PATH)/develop
		cd $(DEPLOY_PATH)/develop
		take $(GIVE_USER) -f
		gunzip $(VERSION).tar.gz
		tar -xvf $(VERSION).tar && rm $(VERSION).tar
		cd .. && chmod -R 750 develop
	AS_WEAVECI_USER

