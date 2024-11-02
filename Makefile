all:build

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

.PHONY: build up down
