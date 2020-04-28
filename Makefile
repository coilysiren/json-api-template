.DEFAULT_GOAL := help

help: # automatically documents the makefile, by outputing everything behind a ##
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.init: # check that dependencies are installed
	@./scripts/check_docker.sh
	@./scripts/check_docker_compose.sh

dev: ## 🛠  setup developement environment
	PIPENV_VENV_IN_PROJECT=true pipenv install --dev

run: .init ## 🏃🏽‍♀️ Run local web server
	docker-compose up --remove-orphans --build server

test: .init ## ✅ Run tests
	docker-compose build tests
	docker-compose run tests

test-watch: .init ## ✅ Run tests 🦅 and watch for changes
	docker-compose build tests
	docker-compose run tests ptw
