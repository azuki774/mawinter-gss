CURRENT_DIR=$(shell pwd)
CONTAINER_NAME_GSS:=mawinter-script-gss

.PHONY: build

build:
	docker build -t ${CONTAINER_NAME_GSS} -f build/gss/Dockerfile .

start:
	docker compose -f deployment/gss/compose.yml up
