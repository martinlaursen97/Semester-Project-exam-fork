make lint: ## Run linter
	@echo "Running linter..."
	poetry run isort .
	poetry run black .
	poetry run ruff --fix .
	poetry run mypy .

make run: ## Run the application
	@echo "Running application..."
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build