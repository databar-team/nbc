ARTIFACT=map-data-pipeline-flyway
ARCHIVE=$(ARTIFACT).tar.gz
VERSION=$(BUILD_NUMBER)
BUILD_DIR=build
DEFINITIONS_DIR=$(BUILD_DIR)/definitions
PIPELINE_RUNNER_DIRECTORY=${BUILD_DIR}/.pipeline-runner

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

clean:
	rm -rf $(BUILD_DIR)

build:
	mkdir -p $(DEFINITIONS_DIR)
	./build-pipeline-definitions.sh $(DEFINITIONS_DIR) $(VERSION)
	mkdir -p $(PIPELINE_RUNNER_DIRECTORY)
	# Invoke pipeline-runnerw.sh to download the pipeline-runner artifact.
	# The "-" ignores the exit status of pipeline-runnerw.sh.
	-./pipeline-runnerw.sh
	mv .pipeline-runner ${BUILD_DIR}
	# Build the archive
	tar -cpzf $(BUILD_DIR)/$(ARCHIVE) \
		src/pipeline \
		src/s3files/sql \
		src/s3files/fi_specific_migrations \
		src/s3files/flyway-runner.sh \
		pipeline-values \
		pipeline-runner.properties \
		requirements.txt \
		$(DEFINITIONS_DIR) \
		-C $(PIPELINE_RUNNER_DIRECTORY) \
		. \
		--exclude='*.pyc'

publish:
	curl -m 300 \
		-u "$(ORG_GRADLE_PROJECT_nexusUsername):$(ORG_GRADLE_PROJECT_nexusPassword)" \
		-T "./$(BUILD_DIR)/$(ARCHIVE)" \
		"$(ORG_GRADLE_PROJECT_repositoryReleaseUrl)/com/bancvue/$(ARTIFACT)/$(VERSION)/$(ARTIFACT)-$(VERSION).tar.gz"

tearDown:
	touch $(VIRTUAL_ENVIRONMENT_NAME)/bin/deactivate
	# Look like we are done with what we are supposed to do, now its time to kick our good friend "virtualenv" out.
	# rm -rf ${VIRTUAL_ENVIRONMENT_NAME}


ci: clean build publish

.PHONY: test
