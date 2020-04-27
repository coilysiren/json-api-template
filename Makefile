.DEFAULT_GOAL := help

help: # automatically documents the makefile, by outputing everything behind a ##
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.init: # check that dependencies are installed
	@./scripts/check_docker.sh
	@./scripts/check_docker_compose.sh
	@./scripts/check_yq.sh
	@./scripts/check_npx.sh

run: .init ## 🏃🏽‍♀️ Run local web server
	docker-compose up memcached server

unit-test: .init ## ✅ Run unit tests
	ls

integration-test: .init ## ✅ Run the integration tests
	docker-compose up --abort-on-container-exit --remove-orphans

test-all: .init ## ✅ Run unit tests and then integration tests
	$(MAKE) unit-test
	$(MAKE) integration-test
