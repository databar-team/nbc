PREFIX=map
ARTIFACT=$(shell basename $(PWD))
# version is defined in the build.properties file.
VERSION=$(version)

guard-%:
	@ if [ "${${*}}" = "" ]; then \
        echo "Environment variable $* not set"; \
        exit 1; \
	fi

default: test

build: guard-AWS_ECR guard-BUILD_NUMBER guard-version
	docker build --no-cache \
		-t "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):latest" \
		-t "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):$(VERSION)" \
		-t "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):$(VERSION).${BUILD_NUMBER}" .

build-for-test: guard-AWS_ECR
	docker build -t "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):test" -f Dockerfile.test .

test: build-for-test guard-AWS_ECR
	docker start ${ARTIFACT}_db_test || docker run --rm --name ${ARTIFACT}_db_test \
		-e "MYSQL_USER=test" \
		-e "MYSQL_PASSWORD=test_password" \
		-e "MYSQL_ROOT_PASSWORD=test_root_password" \
		-e "MYSQL_DATABASE=test_db" \
		-d mysql:5.7 --max-connections=300

	# sleep to ensure the db container is ready to go for the test env run
	sleep 10

	docker run \
		--rm --env-file=app/tests/.env.test \
		--link ${ARTIFACT}_db_test:db-test ${AWS_ECR}/$(PREFIX)/$(ARTIFACT):test

local: build
	docker run --rm --env-file=app/.env.local ${AWS_ECR}/$(PREFIX)/$(ARTIFACT):latest

publish: guard-AWS_ECR guard-BUILD_NUMBER guard-version
	docker push "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):latest"
	docker push "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):$(VERSION)"
	docker push "${AWS_ECR}/$(PREFIX)/$(ARTIFACT):$(VERSION).${BUILD_NUMBER}"

ci: build test publish