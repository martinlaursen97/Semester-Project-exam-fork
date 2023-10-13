lint: ## Run linter
	@echo "Running linter..."
	poetry run black .
	poetry run ruff --fix .
	poetry run mypy .

run: ## Run the application
	@echo "Running application..."
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build

reset:  ## Reset api
	docker rm -vf $$(docker ps -a -q)
	docker rmi rpg_api

reset-db:  ## Remove database
	docker volume rm rpg_api-db-data

reset-full: reset reset-db  ## Reset api and database

reboot: reset run  ## Reset api and run the project

reboot-full: reset-full run  ## Reset api and database and run the project