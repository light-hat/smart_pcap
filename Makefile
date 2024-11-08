all: black build

black:
	@echo "Formatting with black..."
	isort --apply ./api/
	python -m black ./api/

lint:
	@echo "Linting project..."
	pylint --load-plugins pylint_django .

sast:
	@echo "Security static analysis..."
	cd api
	bandit -r .

model:
	@echo "Downloading model..."
	docker build -t model_loader ./model_repository
	docker run --rm model_loader
	docker rmi model_loader

build:
	@echo "Building Smart IDS..."
	docker-compose up -d --build

up:
	@echo "Starting Smart IDS..."
	docker-compose up -d

down:
	@echo "Stopping Smart IDS..."
	docker-compose down

logs:
	@echo "Logs..."
	docker-compose logs

clean:
	@echo "Cleaning workspace"
	docker-compose down -v

.PHONY: black lint sast model build up down logs clean
