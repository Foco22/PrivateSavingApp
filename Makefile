.PHONY: build up up-logs down restart logs shell migrate makemigrations

SERVICE_NAME := app

build:
	@echo "Building Docker images..."
	docker-compose build

up:
	@echo "Starting Django application..."
	docker-compose up -d --build
	@echo "Django application started at http://localhost:8000 ✔︎"

up-logs:
	@echo "Starting Django application with logs..."
	docker-compose up --build

down:
	@echo "Stopping Django application..."
	docker-compose down

restart:
	@echo "Restarting Django application..."
	docker-compose down
	docker-compose up -d --build
	@echo "Django application started at http://localhost:8000 ✔︎"

logs:
	@echo "Fetching logs..."
	docker-compose logs -f

shell:
	@echo "Opening shell..."
	docker-compose exec $(SERVICE_NAME) sh

migrate:
	@echo "Applying migrations..."
	docker-compose exec $(SERVICE_NAME) python manage.py migrate

makemigrations:
	@echo "Creating new migrations..."
	docker-compose exec $(SERVICE_NAME) python manage.py makemigrations


