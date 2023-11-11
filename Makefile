.PHONY: prepare
prepare:
ifeq "$(shell ls /var/run/docker.sock)" ""
	sudo ln -s "$(HOME)/.docker/run/docker.sock" /var/run/docker.sock
else
	@echo 'docker already configured.'
endif

.PHONY: export
export:
	poetry export --without-hashes --format=requirements.txt -o requirements.txt

.PHONY: build
build:
	sam build Bot

.PHONY: test
test:
	sam local invoke Bot --event events/test.json
