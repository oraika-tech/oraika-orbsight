
ifndef frontend_dir
	frontend_dir=.
endif

pkg-unused:
	cd $(frontend_dir); \
	for pkg in $$(yarn workspaces info --json | sed '1d;$$d' | jq -r '.[] | .location'); do \
		echo "\n--- Checking $$pkg...\n"; \
		depcheck --ignore-bin-package $$pkg; \
	done

pkg-upgrade:
	cd $(frontend_dir); \
	yarn upgrade-interactive --latest

pkg-upgrade-dev:
	cd $(frontend_dir); \
	npx yarn-upgrade-all 

clean-deps:
	cd $(frontend_dir); \
	rm -rf node_modules apps/*/node_modules packages/*/node_modules

clean-next:
	cd $(frontend_dir); \
	rm -rf apps/*/.next
  
clean: clean-deps clean-next

