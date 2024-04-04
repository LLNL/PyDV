SHELL := /bin/bash

USER_WORKSPACE := $(if $(USER_WORKSPACE), $(USER_WORKSPACE),/usr/workspace/$(USER))
WORKSPACE = $(USER_WORKSPACE)/gitlab/weave/pydv
PYDV_ENV := $(if $(PYDV_ENV), $(PYDV_ENV),pydv_env)

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

define create_env
	source $(WEAVE_DEVELOP_VENV)/bin/activate
	$(PYTHON_CMD) -m venv --system-site-packages $1
	deactivate
	echo export PATH=$(PATH):$(ADD_PATH) >> $1/bin/activate
	echo export PYTHONPATH=$(PYTHONPATH):$(ADD_PYTHONPATH) >> $1/bin/activate
	source $1/bin/activate
	which pytest
	pip list
endef

define run_pydv_tests
	# call from the top repository directory
	# arg1: full path to venv
	source $1/bin/activate && which pip && which pytest && 
	if [ -z $(DISPLAY) ]; then 
	  xvfb-run --auto-servernum pytest --capture=tee-sys -v tests/; 
	else 
	  pytest --capture=tee-sys -v tests/;
	fi
endef

define do_run_rz_tests
	cd $(RZ_TESTS_WORKDIR) && rm -rf pydv &&
	/usr/tce/bin/git clone -b $(CI_COMMIT_BRANCH) $(RZ_GITLAB)/$(PROJECT) &&
	chgrp -R weavedev pydv && cd pydv && 
	$(call create_env,$(PYDV_ENV)) &&
	cd tests && ln -s /usr/gapps/pydv/dev/tests/wsc_tests . && cd .. &&
	$(call run_pydv_tests,$(RZ_TESTS_WORKDIR)/pydv/$(PYDV_ENV)) &&
	source $(RZ_TESTS_WORKDIR)/pydv/$(PYDV_ENV)/bin/activate &&
	if [ -z $(DISPLAY) ]; then
		xvfb-run --auto-servernum python3 -m pytest tests/wsc_tests/test_*py
	else
		python3 -m pytest -v tests/wsc_tests/test_*py
	fi
endef

.PHONY: create_env
create_env:
	@echo "Create venv for running pydv...$(WORKSPACE)";
	@[ -d $(WORKSPACE) ] || mkdir -p $(WORKSPACE);
	cd $(WORKSPACE);
	if [ -d $(PYDV_ENV) ]; then \
	  rm -rf $(PYDV_ENV); \
	fi;
	$(call create_env,$(PYDV_ENV))


.PHONY: run_tests
run_tests:
	@echo "Run tests...";
	$(call run_pydv_tests,$(WORKSPACE)/$(PYDV_ENV))


.PHONY: run_rz_tests
.ONESHELL:
run_rz_tests:
	@echo "Run RZ tests...RZ_TESTS_WORKDIR: $(RZ_TESTS_WORKDIR)";
	xsu weaveci -c "umask 007 && sg weavedev -c '$(call do_run_rz_tests)'"


.PHONY: release
release:
	@echo "...create a release....TAG: $(CI_COMMIT_TAG), PKG_REGISTRY_URL: $(PKG_REGISTRY_URL)"; \
	$(eval TAG=$(shell  echo $(CI_COMMIT_TAG) | sed -e "s/^pydv-//"))
	env; \
	$(CI_UTILS)/bin/release-cli create --name "PyDV $(CI_COMMIT_TAG)" --tag-name $(CI_COMMIT_TAG); \
	tar -cvf $(TAG).tar pydv docs; \
	ls; \
	gzip $(TAG).tar; \
	curl --header "JOB-TOKEN: $(CI_JOB_TOKEN)" --upload-file $(TAG).tar.gz $(PKG_REGISTRY_URL)/$(CI_COMMIT_TAG)/$(TAG).tar.gz

.PHONY: deploy
.ONESHELL:
deploy:
	@echo "...deploy...only run from CI... "; \
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
		sed -i 's|python|$(PYTHON_CMD)|' $(TAG)/pdv
	AS_WEAVECI_USER


.PHONY: deploy_to_develop
.ONESHELL:
deploy_to_develop:
	$(eval VERSION=`cat $(CI_PROJECT_DIR)/pydv/scripts/version.txt`)
	echo "...deploy_to_develop...VERSION: $(VERSION)"
	cd pydv && if [ -d __pycache__ ]; then rm -rf __pycache__; fi
	if [ -f $(VERSION).tar.gz ]; then rm -f $(VERSION).tar.gz; fi 
	tar -cvf $(VERSION).tar * ../docs && gzip $(VERSION).tar
	give --force weaveci $(VERSION).tar.gz
	$(eval GIVE_USER=$(shell echo ${USER}))
	xsu weaveci -c "sg us_cit" <<AS_WEAVECI_USER
		umask 027
		cd $(DEPLOY_PATH)
		if [ ! -d $(DEPLOY_PATH)/develop ]; then mkdir -p $(DEPLOY_PATH)/develop; fi
		cd $(DEPLOY_PATH)/develop
		take $(GIVE_USER) -f
		gunzip $(VERSION).tar.gz
		tar -xvf $(VERSION).tar && rm $(VERSION).tar
		cd .. && chmod -R 750 develop
		sed -i 's|python|$(PYTHON_CMD)|' develop/pdv
	AS_WEAVECI_USER

