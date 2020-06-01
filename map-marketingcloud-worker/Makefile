PREFIX=map
ARTIFACT=$(shell basename $(PWD))
# version is defined in the build.properties file.
VERSION=$(version)

ifndef AWS_ECR
override AWS_ECR = 304872096477.dkr.ecr.us-west-2.amazonaws.com
endif
ifndef BUILD_NUMBER
override BUILD_NUMBER = test_build
endif
ifndef version
override version = test_version
endif

guard-%:
	@ if [ "${${*}}" = "" ]; then \
        echo "Environment variable $* not set"; \
        exit 1; \
	fi

default: build test

clean:
	find . -name '__pycache__' -delete -print \
		-o -name '*.pyc' -delete -print

build: guard-AWS_ECR guard-BUILD_NUMBER guard-version
	docker build --no-cache \
		-t "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):latest" \
		-t "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):$(VERSION)" \
		-t "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):$(VERSION).${BUILD_NUMBER}" .

build-for-test:
	docker build -t "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):test" -f Dockerfile.test .

test: guard-AWS_ECR build-for-test
	docker start ${ARTIFACT}_db_test || docker run --rm --name ${ARTIFACT}_db_test \
		-e "MYSQL_USER=test" \
		-e "MYSQL_PASSWORD=test_password" \
		-e "MYSQL_ROOT_PASSWORD=test_root_password" \
		-e "MYSQL_DATABASE=test_db" \
		-d mysql:5.7 --max-connections=300

	# sleep to ensure the db container is ready to go for the test env run
	sleep 10

	docker run \
		--rm --env-file=tests/.env.test \
		--link ${ARTIFACT}_db_test:db-test ${AWS_ECR}/$(PREFIX)/$(ARTIFACT):test

publish: guard-AWS_ECR guard-BUILD_NUMBER guard-version
	docker push "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):latest"
	docker push "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):$(VERSION)"
	docker push "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):$(VERSION).${BUILD_NUMBER}"

ci: test build publish