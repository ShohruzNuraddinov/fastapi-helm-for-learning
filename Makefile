#!/usr/bin/make

CURRENT_DIR=$(shell pwd)
APP=$(shell basename ${CURRENT_DIR})
APP_CMD_DIR=${CURRENT_DIR}/cmd

REGISTRY=registry.shohr.uz
TAG ?= latest
ENV_TAG ?= latest
PROJECT_NAME=fastapi_k8s

docker-login:
	@echo "$${REGISTRY_PASSWORD}" | docker login $(REGISTRY) -u $(REGISTRY_USER) --password-stdin

build-image:
	docker build --cache-from ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG} -t ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG} .

tag-image:
	docker tag ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG} ${REGISTRY}/${PROJECT_NAME}/${APP}:${ENV_TAG}

push-image:
	docker push ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG}

push-env-tag:
	docker push ${REGISTRY}/${PROJECT_NAME}/${APP}:${ENV_TAG}

clear-image:
	-docker rmi ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG}
	-docker rmi ${REGISTRY}/${PROJECT_NAME}/${APP}:${ENV_TAG}

.PHONY: docker-login build-image tag-image push-image push-env-tag clear-image