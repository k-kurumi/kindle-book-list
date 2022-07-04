# Kindle for mac の所有書籍情報が入ったXML
KINDLE_XML_PATH := ~/Library/Application\ Support/Kindle/Cache/KindleSyncMetadataCache.xml

# https://postd.cc/auto-documented-makefile/
.DEFAULT_GOAL := help
.PHONY: help
help: ## help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(word 1,$(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

.PHONY: copy-xml
copy-xml: ## copy KindleSyncMetadataCache.xml to data dir and reformat
	mkdir -p data
# 元ファイルは長い1行のため確認しやすく整形する
	xmllint --encode utf-8 --format $(KINDLE_XML_PATH) > ./data/KindleSyncMetadataCache.xml

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
