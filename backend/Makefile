# Root Makefile

mypy-analyse:
	mypy service-api

clean:
	rm -rf .mypy_cache .pytest_cache src/lambda/tenant_onboarding/app/build

# $(*_dir) variable are required by respective Makefile to resolve parent directory

svc_api_dir=service-api
include $(svc_api_dir)/Makefile

db_dir=database
include $(db_dir)/Makefile

tenant_onboarding_dir=src/lambda/tenant_onboarding
