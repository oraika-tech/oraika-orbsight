# Service API Makefile

ifndef svc_api_dir
	svc_api_dir=.
endif

port=8080

svc-api-compile:
	cd $(svc_api_dir); \
	pip-compile --resolver=backtracking -U pyproject.toml

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
