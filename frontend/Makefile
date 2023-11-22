
pkg-unused:
	for pkg in $$(yarn workspaces info --json | sed '1d;$$d' | jq -r '.[] | .location'); do \
		echo "\n--- Checking $$pkg...\n"; \
		depcheck --ignore-bin-package $$pkg; \
	done

pkg-upgrade:
	yarn upgrade-interactive --latest

pkg-upgrade-dev:
	npx yarn-upgrade-all 

clean-deps:
	rm -rf node_modules apps/*/node_modules packages/*/node_modules

clean-next:
	rm -rf apps/*/.next
  
clean: clean-deps clean-next
