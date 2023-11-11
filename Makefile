LAMBDA_FUNC_NAME := snupy-bot
IMAGE_TAG := 327379428311.dkr.ecr.ap-northeast-1.amazonaws.com/snupy-bot/app:latest

PYTHON_MODULES := app.py $(shell find lib -type f -name '*.py')
REQUIREMENTS := requirements.txt

.PHONY: prepare
prepare: ## Prepare environment
ifeq "$(shell ls /var/run/docker.sock)" ""
	sudo ln -s "$(HOME)/.docker/run/docker.sock" /var/run/docker.sock
else
	@echo 'docker already configured.'
endif
	poetry install

### Test ###
.PHONY: build
build: ## Build sam for test
	sam build Bot

.PHONY: test
test: ## Run lambda in sam
	sam local invoke Bot --event events/test.json

### Deploy ###

# lambdaのpythonのパッチバージョンを揃えない
$(REQUIREMENTS): poetry.lock
	poetry export --without-hashes | sed 's/;.*//' > $@

deploy: $(REQUIREMENTS) $(PYTHON_MODULES) ## Deploy lambda
	docker build -t snupy-bot/app .
	docker tag snupy-bot/app:latest $(IMAGE_TAG)
	docker push 327379428311.dkr.ecr.ap-northeast-1.amazonaws.com/snupy-bot/app:latest

.PHONY: help
help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
