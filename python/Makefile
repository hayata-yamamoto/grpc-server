fmt: 
	poetry run yapf -r -i --style pep8 src

mypy:
	poetry run mypy --html-report ./report src/

server: 
	poetry run python3 src/commands/server.py

client: 
	poetry run python3 src/commands/client.py