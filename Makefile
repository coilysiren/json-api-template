.DEFAULT_GOAL := help

help: # automatically documents the makefile, by outputing everything behind a ##
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.init: # check that dependencies are installed
	@./scripts/check_aws.sh
	@./scripts/check_docker.sh
	@./scripts/check_docker_compose.sh

dev: .init ## 🛠  Setup local dev environment
	# docker resources
	-docker stop $(shell docker ps -a -q)
	docker system prune -a -f
	# python packages
	rm -rf .venv
	PIPENV_VENV_IN_PROJECT=true pipenv install --dev
	# data assets
	rm -rf data
	mkdir data
	aws s3 cp s3://net.energyhub.assets/public/dev-exercises/audit-data.tar.gz data/audit-data.tar.gz
	tar --extract --file data/audit-data.tar.gz -C data
	rm data/audit-data.tar.gz

run: .init ## 🏃🏽‍♀️ Run local web server
	docker-compose down
	docker-compose up -d database
	docker-compose build migrations
	docker-compose run migrations
	docker-compose up --remove-orphans --build server

name ?= "TODO: future optimization, enforce a name here"
create-migration-revision: .init ## 📝 Create a new migration revision (inputs: name=<name>)
	docker-compose down
	docker-compose up -d database
	docker-compose build migrations
	docker-compose run migrations
	docker-compose run migrations alembic -c setup.cfg revision --autogenerate -m "$(name)"

lint: .init ## 🧹 Run linters
	docker-compose build lint
	docker-compose run lint pylint --rcfile=./setup.cfg server tests
	docker-compose run lint isort --check-only **/*.py
	docker-compose run lint black --check server tests

lint-autoformat: .init ## 🧹 Run linters with automatic formatting
	docker-compose build lint
	docker-compose run lint isort **/*.py
	docker-compose run lint black server tests

args ?= "" # pytest args go here
test: .init ## ✅ Run tests (inputs: args=<"-k=MyTestName"|"--maxfail=1">)
	docker-compose down
	docker-compose up -d database
	docker-compose build migrations
	docker-compose build tests
	docker-compose run migrations
	docker-compose run tests pytest $(args)

test-watch: .init ## ✅ Run tests 🦅 and watch for changes
	docker-compose down
	docker-compose up -d database
	docker-compose build migrations
	docker-compose build tests
	docker-compose run migrations
	docker-compose run tests ptw
