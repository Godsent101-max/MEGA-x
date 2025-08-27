.PHONY: build up down logs shell clean

build:
	docker-compose build

up:
	docker-compose up -d --remove-orphans

down:
	docker-compose down

logs:
	docker-compose logs -f backend

shell-backend:
	docker-compose exec backend /bin/sh

clean:
	rm -rf backend/__pycache__ frontend/dist