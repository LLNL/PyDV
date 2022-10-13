SHELL := /bin/bash

USER_WORKSPACE := $(if $(USER_WORKSPACE), $(USER_WORKSPACE),/usr/workspace/$(USER))
WORKSPACE = $(USER_WORKSPACE)/gitlab/weave/pydv
PYDV_ENV := $(if $(PYDV_ENV), $(PYDV_ENV),pydv_env)

PKG_REGISTRY_URL = $(CI_API_V4_URL)/projects/$(CI_PROJECT_ID)/packages/generic/archive
DEPLOY_PATH = /usr/gapps/pydv
CI_UTILS = /usr/gapps/weave/ci_utils

CZ_GITLAB = "ssh://git@czgitlab.llnl.gov:7999"
RZ_GITLAB = "ssh://git@rzgitlab.llnl.gov:7999"
PROJECT = "weave/pydv.git"

RZ_TESTS_WORKDIR = /usr/gapps/pydv/wsc_tests_workdir
PYTHON_CMD = /usr/tce/packages/python/python-3.8.2/bin/python3

define create_env
	# call from the directory where env will be created
	# arg1: name of env
	$(PYTHON_CMD) -m venv --system-site-packages $1
	source $1/bin/activate &&
	pip3 install --upgrade pip &&
	pip3 install --force pytest &&
	pip3 install numpy scipy matplotlib PySide2 &&
	which pytest
endef

define run_pydv_tests
	# call from the top repository directory
	# arg1: full path to venv
	source $1/bin/activate && which pip && which pytest && 
	if [ -z $(DISPLAY) ]; then 
	  xvfb-run --auto-servernum pytest --capture=tee-sys -v tests/test_pydv_images.py; 
	else 
	  pytest --capture=tee-sys -v tests/test_pydv_images.py;
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
	@echo "Run RZ tests...RZ_TESTS_WORKDIR: $(RZ_TESTS_WORKDIR)"
	xsu weaveci -c "sg us_cit" <<AS_WEAVECI_USER
		cd $(RZ_TESTS_WORKDIR) && rm -rf pydv
		/usr/tce/bin/git clone -b develop $(RZ_GITLAB)/$(PROJECT)
		cd pydv
		$(call create_env,$(PYDV_ENV))
		cd tests && ln -s /usr/gapps/pydv/dev/tests/wsc_tests . && cd ..
		$(call run_pydv_tests,$(RZ_TESTS_WORKDIR)/pydv/$(PYDV_ENV))
		for t in tests/wsc_tests/test_*py; do
			echo RUNNING \$$t
			if [ -z $(DISPLAY) ]; then
				xvfb-run --auto-servernum python3 -m pytest \$$t
			else
				python3 -m pytest -v \$$t
			fi
		done
	AS_WEAVECI_USER


.PHONY: create_and_push_tag
create_and_push_tag:
	$(shell git checkout $(CI_COMMIT_BRANCH))
	$(shell git fetch)
	$(eval TAG=$(shell python3 $(CI_UTILS)/utils/get_project_version.py --git_repo_dir $(CI_PROJECT_DIR) --file_with_version setup.py))
	@echo "Create a tag and push the tag $(TAG) to $(CI_COMMIT_BRANCH) branch, CI_PROJECT_DIR: $(CI_PROJECT_DIR)..."; \
	git config --global User.email "$(GITLAB_USER_EMAIL)"; \
	git config --global user.name "$(GITLAB_USER_NAME)"; \
	git remote rm origin && \
	if [ $(SOURCE_ZONE) == "CZ" ]; then \
		git remote add origin $(CZ_GITLAB)/$(PROJECT); \
	else \
		git remote add origin $(RZ_GITLAB)/$(PROJECT); \
	fi; \
	git pull origin $(CI_COMMIT_BRANCH); \
	git fetch; \
	git status; \
	echo "Create and push pydv-$(TAG) tag..."; \
	git tag -a pydv-$(TAG) -m "Adding tag pydv-$(TAG)"; \
	git commit -a -m"add tag pydv-$(TAG)"; \
	git push origin pydv-$(TAG)


.PHONY: release
release:
	@echo "...create a release....TAG: $(CI_COMMIT_TAG), PKG_REGISTRY_URL: $(PKG_REGISTRY_URL)"; \
	$(eval TAG=$(shell  echo $(CI_COMMIT_TAG) | sed -e "s/^pydv-//"))
	env; \
	$(CI_UTILS)/bin/release-cli create --name "PyDV $(CI_COMMIT_TAG)" --tag-name $(CI_COMMIT_TAG); \
	tar -cvf $(TAG).tar pydv; \
	ls; \
	gzip $(TAG).tar; \
	curl --header "JOB-TOKEN: $(CI_JOB_TOKEN)" --upload-file $(TAG).tar.gz $(PKG_REGISTRY_URL)/$(CI_COMMIT_TAG)/$(TAG).tar.gz


.PHONY: deploy
.ONESHELL:
deploy:
	@echo "...deploy...only run from CI, DEPLOY_TO variable needs to be set"; \
	$(eval TAG=$(shell  echo $(CI_COMMIT_TAG) | sed -e "s/^pydv-//"))
	wget --header="JOB-TOKEN:$(CI_JOB_TOKEN)" $(PKG_REGISTRY_URL)/$(CI_COMMIT_TAG)/$(TAG).tar.gz -O $(TAG).tar.gz
	give weaveci $(TAG).tar.gz
	xsu weaveci -E -L -c "bash -l" <<AS_WEAVECI_USER
	set -x
	set -e
	sg us_cit
	cd $(DEPLOY_PATH)/$(DEPLOY_TO)
	take muryanto -f
	chmod 750 $(TAG).tar.gz
	gunzip $(TAG).tar.gz
	tar -xvf $(TAG).tar
	rm $(TAG).tar
	mv pydv $(TAG)
	chmod -R 750 $(TAG)
	rm -f latest
	ln -s $(TAG) latest
	AS_WEAVECI_USER
