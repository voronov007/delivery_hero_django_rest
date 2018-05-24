# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)


TARGET_MAX_CHAR_NUM=20
## show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''

## starts docker compose(db+container) in background mode
start:
	python manage.py runserver

## build and start docker-compose, apply migrations
init:
	make start
	make migrate

## create migrations files for the Django
migrations:
	python manage.py makemigrations

## apply migrations for the Django
migrate:
	python manage.py migrate

## open Django shell
shell:
	python manage.py shell

## change owner to current user for all files in the project
chown:
	sudo chown -R ${USER}:${USER} .

## delete database
dropdb:
	rm -vf db.sqlite3

## drop db -> recreate db -> run migrations
restart_db:
	make stop
	docker-compose rm -vf ras_db_service
	make start
	make migrate