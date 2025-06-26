CURRENT_DIR=$(shell pwd)

APP=fastapi-test

APP_CMD_DIR=fastapi-test/cmd

REGISTRY=registry.shohr.uz
TAG=latest
ENV_TAG=latest
PROJECT_NAME=project-fastapi

docker-login:
	docker login -u asd -p Asdasd ${REGISTRY}

build-image:
	docker build --cache-from ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG} -t ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG} .
	docker tag ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG} ${REGISTRY}/${PROJECT_NAME}/${APP}:${ENV_TAG}

push-image:
	docker push ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG}
	docker push ${REGISTRY}/${PROJECT_NAME}/${APP}:${ENV_TAG}

clear-image:
	docker rmi ${REGISTRY}/${PROJECT_NAME}/${APP}:${TAG}
	docker rmi ${REGISTRY}/${PROJECT_NAME}/${APP}:${ENV_TAG}
