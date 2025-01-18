
ifndef backend_dir
	backend_dir=.
endif


mypy-analyse:
	cd $(backend_dir); \
	mypy service-api

clean:
	cd $(backend_dir); \
	rm -rf .mypy_cache .pytest_cache

# $(*_dir) variable are required by respective Makefile to resolve parent directory

svc_api_dir=$(backend_dir)/service-api
include $(svc_api_dir)/Makefile

db_dir=$(backend_dir)/database
include $(db_dir)/Makefile

