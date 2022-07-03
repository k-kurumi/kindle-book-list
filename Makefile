
# https://postd.cc/auto-documented-makefile/
.DEFAULT_GOAL := help
.PHONY: help
help: ## help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(word 1,$(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

.PHONY: copy-xml
copy-xml: ## copy KindleSyncMetadataCache.xml to data dir
	mkdir -p data
	cp ~/Library/Application\ Support/Kindle/Cache/KindleSyncMetadataCache.xml ./data

.PHONY: fmt
fmt: ## format code
	isort .
	black .

.PHONY: docker-build
docker-build: ## docker build
	docker build -t kurumi/kindle-book-list:latest .

.PHONY: docker-push
docker-push: ## docker push
	docker push kurumi/kindle-book-list:latest

.PHONY: docker-run
docker-run: copy-xml ## docker run
	docker run --rm -v $(shell pwd):/app kurumi/kindle-book-list:latest -i data/KindleSyncMetadataCache.xml
