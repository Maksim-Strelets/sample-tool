DOCKER_COMPOSE ?= docker-compose.yml

# run autoformat
.PHONY: dev/autoformat
.ONESHELL:
dev/autoformat:
	@docker-compose -f $(DOCKER_COMPOSE) run --rm app-inspect /bin/bash -c \
		"autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place src tests cli.py"
	@docker-compose -f $(DOCKER_COMPOSE) run --rm app-inspect /bin/bash -c \
		"black src tests cli.py"
	@docker-compose -f $(DOCKER_COMPOSE) run --rm app-inspect /bin/bash -c \
		"isort src tests cli.py"

# run full pre-commit check
.PHONY: dev/lint
dev/lint:
	@pre-commit run --all-files

# run local required environment
.PHONY: dev/up-env
.ONESHELL:
dev/up-env: dev/stop-all
	@docker-compose -f $(DOCKER_COMPOSE) up db-local;\
	$(MAKE) dev/stop-all;\

# run local full application
.PHONY: dev/up-app
.ONESHELL:
dev/up-app: dev/stop-all
	@docker-compose -f $(DOCKER_COMPOSE) up --detach db-local
	@docker-compose -f $(DOCKER_COMPOSE) run --rm app-local /bin/bash -c "python cli.py db:upgrade"
	@docker-compose -f $(DOCKER_COMPOSE) up app-local;\
	$(MAKE) dev/stop-all;\

# stop all docker compose services
.PHONY: dev/stop-all
.ONESHELL:
dev/stop-all:
	@docker-compose -f $(DOCKER_COMPOSE) stop

# run all tests in one-click
.PHONY: tests/all
tests/all: tests/flake8 tests/mypy tests/black tests/isort tests/pytest

# run all checks except tests in one-click
.PHONY: tests/lint
tests/lint: tests/flake8 tests/mypy tests/black tests/isort

# up environment for tests
.PHONY: tests/up-compose
.ONESHELL:
tests/up-compose:
	# Add here run other containers necessary for pytests
	@docker-compose -f $(DOCKER_COMPOSE) up --detach localstack-test

# stop environment for tests
.PHONY: tests/stop-compose
tests/stop-compose:
	@docker-compose -f $(DOCKER_COMPOSE) stop

# run flake8 check in docker
.PHONY: tests/flake8
tests/flake8:
	@docker-compose -f $(DOCKER_COMPOSE) run --rm app-inspect /bin/bash -c "flake8 ./src"

# run mypy check in docker
.PHONY: tests/mypy
tests/mypy:
	@docker-compose -f $(DOCKER_COMPOSE) run --rm app-inspect /bin/bash -c "mypy --show-traceback ./src"

# run black check in docker
.PHONY: tests/black
tests/black:
	@docker-compose -f $(DOCKER_COMPOSE) run --rm app-inspect /bin/bash -c "black --check ./src --diff"

# run isort check in docker
.PHONY: tests/isort
tests/isort:
	@docker-compose -f $(DOCKER_COMPOSE) run --rm app-inspect /bin/bash -c "isort --check-only ./src"

# run pytest check in docker
.PHONY: tests/pytest
tests/pytest:
	@docker-compose -f $(DOCKER_COMPOSE) run --rm app-test /bin/bash -c "pytest -s -vv --verbose"
