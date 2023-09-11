# BrewUnifiedAPI

# To start the services

First you have to run a command, from your main directory (Task_project), you need to run

# make setup

# make serve

# make migrate_all


For details of Makefile commands:
# make help

# For Kubernetes
kubectl apply -f k8s-deployment.yaml

eval $(minikube docker-env)

for log in kube
 kubectl logs accounting-7f6cd5ff5f-nrn4d -c accounting
kubectl describe pod accounting