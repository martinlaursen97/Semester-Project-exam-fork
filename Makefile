lint: ## Run linter
	@echo "Running linter..."
	poetry run black .
	poetry run ruff --fix .
	poetry run mypy .

run: ## Run the application
	@echo "Running application..."
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build

reboot:
	@echo "Removing containers"
	docker rm $$(docker ps -aq)
	@echo "Removing images"
	docker rmi $$(docker images -q)  
	@echo "Removing volumes"
	docker volume rm $$(docker volume ls -q)
	
reset:  ## Reset api
	docker rm -vf $$(docker ps -a -q)
	docker rmi rpg_api

reset-db:  ## Remove database
	docker volume rm semester-project_pg-data

test: ## Run tests
	@echo "Running tests..."
	docker container exec $$(docker ps | grep api-1 | awk '{print $$1}') pytest ./rpg_api/tests/pytest -s

migration-generate:  ## Generate a new migration file
	@echo "Generation migrations..."
	docker container exec $$(docker ps | grep rpg_api | awk '{print $$1}') alembic revision --autogenerate

migration-upgrade-head:  ## Upgrade to the latest migration
	@echo "Upgrading to latest..."
	docker container exec $$(docker ps | grep rpg_api | awk '{print $$1}') alembic upgrade head

migration-upgrade-one:  ## Upgrade one migration
	docker container exec $$(docker ps | grep rpg_api  | awk '{print $$1}') alembic upgrade +1

migration-downgrade-one:  ## Downgrade one migration
	docker container exec $$(docker ps | grep rpg_api  | awk '{print $$1}') alembic downgrade -1
