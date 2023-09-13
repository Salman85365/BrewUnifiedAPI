# BrewUnifiedAPI

Unified API for a microbrewery to manage Warehouse, Accounting, and Sales services.

## Prerequisites

- Docker and Docker Compose
- Kubernetes (Optional)
- Postman or Insomnia (for API testing)

## Setup

### Environment Variables

1. Locate the `.env.example` file in the main directory where `docker-compose-services.yaml` exists.
2. Create a `.env` file in the main directory.
3. Copy the contents from `.env.example` into the new `.env` file.

### Starting the Services

From your main project directory (`Task_project`):

```shell
make setup  # This will allow permissions to wait-for-it.sh
make serve # This will run docker compose file, build and run containers 
make migrate_all # This will run migrations for all services
```

### Superuser Creation
Accounting service acts as the authentication provider. Follow the steps below:

Create a superuser:

```make user_accounting```

### To get the access token, navigate to:

Access Token Endpoint
   ```http://localhost:8000/api/token/```
Use Postman or Insomnia to fetch the token. Include it in subsequent requests as:

Authorization: Bearer {access_token}
    
## Service Endpoints

Accounting Service:  ```http://localhost:8000/accounting/ ```

Inventory Service: ```http://localhost:8000/warehouse/```

Sales Service: ```http://localhost:8000/sales/```

## Loading Data
To load initial data into a service, use:
```make loaddata_{service_name}```
for example:
```make loaddata_accounting```

## API Documentation
Swagger documentation is provided for each service:

Accounting Service: Swagger for Accounting
``` http://localhost:8002/swagger/ ```

Inventory Service: Swagger for Inventory

``` http://localhost:8001/swagger/ ```

Sales Service: Swagger for Sales
``` http://localhost:8003/swagger/ ```

## Available Makefile Commands
For a list of Makefile commands:
```make help```

## Restarting a Service
To restart a specific service:
```make restart_{service_name}```
for example:
```make restart_accounting```

## Kubernetes Deployment (Optional)
Apply the Kubernetes deployment:
```kubectl apply -f k8s-deployment.yaml```


## Testing
To run tests for a specific service:
```make test_{service_name}```
for example:
```make test_accounting```

