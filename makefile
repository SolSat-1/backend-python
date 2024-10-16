build-venv:
	python3 -m venv venv
	source venv/bin/activate

build-docker:
	docker build -t todo-api:v1 .

docker-compose-up:
	docker-compose up

dev:
	uvicorn main:app --reload

requirements:
	pip freeze > requirements.txt

lint-check:
	ruff check .

lint:
	ruff format .