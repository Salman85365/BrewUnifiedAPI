#####################################################################
# Make file for Automation and Ease of Use.
#####################################################################

######################################################################
# Management and Utility targets
######################################################################

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'


logs_%: ## Trail logs of the mentioned service
	docker logs -f --tail 100 $*

serve: ## run all docker services
	docker-compose -f docker-compose-services.yaml up -d --build


restart_%: ## Restart specific service (make restart_warehouse)
	docker-compose -f docker-compose-services.yaml stop $*
	docker-compose -f docker-compose-services.yaml  up -d --build $*


stop: ## Stop all docker Backend Services
	docker-compose -f docker-compose-services.yaml stop



down: ## Remove all service containers
	docker-compose -f docker-compose-services.yaml down

shell_%:
	docker-compose -f docker-compose-services.yaml exec $* python manage.py shell

logs_%: ## Trail logs of the service (make logs_warehouse)
	docker logs -f --tail 500 $*


command_%: ## Run custom docker django-admin command (make command_warehouse args="shell")
	docker-compose -f docker-compose-services.yaml  exec $* python manage.py ${args}

migrate_%: ## Migrate docker specific backend docker services (make migrate_warehouse)
	docker-compose -f docker-compose-services.yaml exec $* python manage.py migrate --noinput

migrate_all: ## Migrate all docker containers
	make migrate_warehouse
	make migrate_sales
	make migrate_accounting



send_images_to_ec2_tag_%: ## Create and send images to ec2
	aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 449874233708.dkr.ecr.ap-south-1.amazonaws.com
	docker tag class 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-class-prod-ap-south-1:$*
	docker push 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-class-prod-ap-south-1:$*
	docker tag content 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-content-prod-ap-south-1:$*
	docker push 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-content-prod-ap-south-1:$*
	docker tag school 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-school-prod-ap-south-1:$*
	docker push 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-school-prod-ap-south-1:$*
	docker tag teacher 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-teacher-prod-ap-south-1:$*
	docker push 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-teacher-prod-ap-south-1:$*
	docker tag frontend 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-fe-frontend-ap-south-1:$*
	docker push 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-fe-frontend-ap-south-1:$*
	docker tag admin 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-man-admin-prod-ap-south-1:$*
	docker push 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-man-admin-prod-ap-south-1:$*
	docker tag warehouse 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-man-warehouse-prod-ap-south-1:$*
	docker push 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-man-warehouse-prod-ap-south-1:$*
	docker tag teachertraining 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-teacher_training-prod-ap-south-1:$*
	docker push 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-teacher_training-prod-ap-south-1:$*
	docker tag exam 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-exam-prod-ap-south-1:$*
	docker push 449874233708.dkr.ecr.ap-south-1.amazonaws.com/ecr-be-exam-prod-ap-south-1:$*



checkout_%: ## Recreate volumes and restart services
	git checkout $*
	docker volume rm $(docker volume ls -q)
	make create_volumes
	make stop
	make serve
	make migrate_all
	

upgrade_%: ## Compile requirements.txt for a given backend service.
	docker run --rm -v `pwd`:/web pipupgrade:latest python -m piptools compile --upgrade --verbose --rebuild -o services/$*/requirements.txt services/$*/requirements.in

setup:
	echo "Setting permissions..."
	@chmod +x ./services/sales/wait-for-it.sh
