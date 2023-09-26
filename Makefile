#####################################################################
# Make file for Automation and Ease of Use.
#####################################################################

######################################################################
# Management and Utility targets
######################################################################

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'


serve: ## run all docker services
	docker compose -f docker-compose-services.yaml up -d --build


restart_%: ## Restart specific service (make restart_warehouse)
	docker compose -f docker-compose-services.yaml stop $*
	docker compose -f docker-compose-services.yaml  up -d --build $*


stop: ## Stop all docker Backend Services
	docker compose -f docker-compose-services.yaml stop

loaddata_%: ## Load fixtures for specific service (make loaddata_warehouse)
	docker compose -f docker-compose-services.yaml exec $* python manage.py loaddata fixtures/initial_data.json

down: ## Remove all service containers
	docker compose -f docker-compose-services.yaml down

shell_%:
	docker compose -f docker-compose-services.yaml exec $* python manage.py shell

logs_%: ## Trail logs of the service (make logs_warehouse)
	docker logs -f --tail 500 $*


command_%: ## Run custom docker django-admin command (make command_warehouse args="shell")
	docker compose -f docker-compose-services.yaml  exec $* python manage.py ${args}

migrate_%: ## Migrate docker specific backend docker services (make migrate_warehouse)
	docker compose -f docker-compose-services.yaml exec $* python manage.py migrate --noinput

migrate_all: ## Migrate all docker containers
	make migrate_warehouse
	make migrate_sales
	make migrate_accounting



checkout_%: ## Recreate volumes and restart services
	git checkout $*
	docker volume rm $(docker volume ls -q)
	make create_volumes
	make stop
	make serve
	make migrate_all
	

setup:
	echo "Setting permissions..."
	@chmod +x ./services/sales/wait-for-it.sh
	@chmod +x ./services/warehouse/wait-for-it.sh

test_%: ## Run tests for specific service (make test_warehouse)
	docker compose -f docker-compose-services.yaml exec $* python manage.py test


user_%: ## Create superuser for specific service (make createsuperuser_warehouse)
	docker compose -f docker-compose-services.yaml exec $* python manage.py createsuperuser