all: black build

black:
	isort --apply ./api/
	python -m black ./api/

lint:
	pylint --load-plugins pylint_django .

sast:
	cd api
	bandit -r .

build:
	docker compose up -d --build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs

clean:
	docker compose down -v

.PHONY: black lint sast model build up down logs clean
