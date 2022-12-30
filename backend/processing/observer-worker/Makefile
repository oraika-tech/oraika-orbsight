# Service Observer Makefile

ifndef svc_observer_dir
	svc_observer_dir=.
endif

port=8080

svc-observer-dep:
	cd $(svc_observer_dir); \
	pip install -e .

svc-observer-dev:
	cd $(svc_observer_dir); \
	pip install '.[dev]'

svc-observer-run:
	cd $(svc_observer_dir); \
	uvicorn observer.presentation.observer_job_controller:app --reload --port=$(port)

svc-observer-test:
	pytest $(svc_observer_dir)/test
