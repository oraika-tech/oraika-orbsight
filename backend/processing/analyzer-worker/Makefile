# Service Analyzer Makefile

ifndef svc_analyzer_dir
	svc_analyzer_dir=.
endif

port=8080

svc-analyzer-dep:
	cd $(svc_analyzer_dir); \
	pip install -e .

svc-analyzer-dev:
	cd $(svc_analyzer_dir); \
	pip install '.[dev]'

svc-analyzer-run:
	cd $(svc_analyzer_dir); \
	uvicorn analyzer.api.api:app --reload --port=$(port)
