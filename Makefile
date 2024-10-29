all:build

build:
	@echo "Building Smart IDS..."
	docker-compose up -d --build

up:
	@echo "Starting Smart IDS..."
	docker-compose up -d

down:
	@echo "Stopping Smart IDS..."
	docker-compose down

rebuild:
	@echo "Recreating all services..."
	docker-compose down && docker-compose build --no-cache && docker-compose up -d

clean:
	@echo "Delete all containers and volumes..."
	docker-compose down -v

bash:
	@echo "Enter to container $(CONTAINER)..."
	docker-compose exec $(CONTAINER) /bin/bash

logs:
	@echo "Printing logs..."
	docker-compose logs

.PHONY: build up down rebuild clean bash logs
