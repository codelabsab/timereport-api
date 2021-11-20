NAME=timereport-api
VERSION=0.0.1

DB_PORT = 8000
API_PORT = 8010
CHALICE_API_KEY ?= development
CHALICE_ENV = "dev"


.PHONY: pull run stop restart rm

pull:
	docker pull amazon/dynamodb-local

dynamo:
	docker run --rm --name dynamodb-local -d -p $(DB_PORT):$(DB_PORT) amazon/dynamodb-local

config:
	sed "s/<CHALICE_API_KEY>/$(CHALICE_API_KEY)/" .chalice/config.json.template > .chalice/config.json
run:
	docker run --rm --name dynamodb-local -d -p $(DB_PORT):$(DB_PORT) amazon/dynamodb-local
	# Wait for local DB to start
	sleep 5
	chalice local --port $(API_PORT) --no-autoreload

stop:
	docker stop dynamodb-local

restart:
	docker restart dynamodb-local

chalice:
	chalice local --port $(API_PORT) --no-autoreload

ci-server:
	sh -c "chalice local --port $(API_PORT) --no-autoreload &"

deploy:
	chalice deploy --stage $(CHALICE_ENV)

default: run
clean: stop
