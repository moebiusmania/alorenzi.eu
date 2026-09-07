.PHONY: install serve build sync-media deploy

install:
	bundle install

serve: install
	bundle exec jekyll serve --watch

build: install
	bundle exec jekyll build

sync-media:
	aws --profile alorenzi s3 sync _media/ s3://alorenzi-eu-media/

deploy: build sync-media
	rsync -avc _site/ home:/srv/alorenzi_eu/
