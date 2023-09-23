# Service API Makefile

ifndef svc_api_dir
	svc_api_dir=.
endif

port=8080

svc-api-compile:
	cd $(svc_api_dir); \
	pip-compile --no-strip-extras --resolver=backtracking -U pyproject.toml

svc-api-dep:
	cd $(svc_api_dir); \
	pip install -r requirements.txt

svc-api-dev:
	cd $(svc_api_dir); \
	pip install '.[dev]'

svc-api-run:
	cd $(svc_api_dir); \
	uvicorn service.main:app --reload --port=$(port)

svc-api-test:
	pytest $(svc_api_dir)/tests

svc-api-docker-build:
	mypy processing
	cd $(svc_api_dir); \
    docker build -t api-service-local .

svc-api-docker-run:
	cd $(svc_api_dir); \
	docker-compose up

prefect-tunneling:
	cd $(svc_api_dir); \
	bash scripts/prefect-tunneling.sh

prefect-local-run:
	cd $(svc_api_dir); \
	bash scripts/prefect-run.sh

