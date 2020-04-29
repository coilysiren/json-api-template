.DEFAULT_GOAL := help

help: # automatically documents the makefile, by outputing everything behind a ##
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.init: # check that dependencies are installed
	@./scripts/check_docker.sh
	@./scripts/check_docker_compose.sh

dev: ## 🛠  setup developement environment
	PIPENV_VENV_IN_PROJECT=true pipenv install --dev

run: .init ## 🏃🏽‍♀️ Run local web server
	docker-compose down
	docker-compose build migrations
	docker-compose up -d database
	docker-compose run --rm migrations
	docker-compose up --remove-orphans --build server

name ?= "TODO: enforce a name here"
create-migration-revision: .init ## 📝 Create a new migration revision (inputs: name=<name>)
	docker-compose down
	docker-compose build migrations
	docker-compose up -d database
	docker-compose run --rm migrations
	docker-compose run --rm migrations alembic -c setup.cfg revision --autogenerate -m "$(name)"

test: .init ## ✅ Run tests
	docker-compose down
	docker-compose build migrations
	docker-compose build tests
	docker-compose up -d database
	docker-compose run --rm migrations
	docker-compose run --rm tests

test-watch: .init ## ✅ Run tests 🦅 and watch for changes
	docker-compose down
	docker-compose build migrations
	docker-compose build tests
	docker-compose up -d database
	docker-compose run --rm migrations
	docker-compose run --rm tests ptw
