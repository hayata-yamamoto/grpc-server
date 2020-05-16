default: | help

fmt: ## format codes ## make fmt
	poetry run yapf -r -i --style pep8 src

mypy: ## check static typing ## make mypy
	poetry run mypy --html-report ./report src/

flake8: ## check PEP8 style ## make flake8
	poetry run flake8 src/

server: ## start gRPC server ## make server
	poetry run python3 src/commands/server.py

client: ## call sample request to a started gRPC server ## make client 
	poetry run python3 src/commands/client.py


# This help command is cited from https://ktrysmt.github.io/blog/write-useful-help-command-by-shell/
help: ## print this message
	@echo "Example operations by makefile."
	@echo ""
	@echo "Usage: make SUB_COMMAND argument_name=argument_value"
	@echo ""
	@echo "Command list:"
	@echo ""
	@printf "\033[36m%-30s\033[0m %-50s %s\n" "[Sub command]" "[Description]" "[Example]"
	@grep -E '^[/a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | perl -pe 's%^([/a-zA-Z_-]+):.*?(##)%$$1 $$2%' | awk -F " *?## *?" '{printf "\033[36m%-30s\033[0m %-50s %s\n", $$1, $$2, $$3}'	