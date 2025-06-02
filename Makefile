DEFAULT_GOAL := help

ENV_FILE ?= .env
COMPOSE_FILE ?= docker-compose.yml

up: prepare-env ## Запуск всех контейнеров через docker-compose
  docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) up --detach --build

stop: prepare-env ## Остановка всех контейнеров
  docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) stop

down: prepare-env ## Удаление всех контейнеров
  docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) down

prepare-env: ## Подготовить переменные окружения для запуска сервисов в контейнерах
  cp example.env .env

logs: ## Просмотр логов приложения
  docker-compose --env-file $(ENV_FILE) -f $(COMPOSE_FILE) logs fastapi_app

help: ## Показывает список команд
  @awk -F':.*?## ' '/^[a-zA-Z0-9_-]+:.*## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
