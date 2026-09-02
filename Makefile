.PHONY: install serve build sync-media deploy

install:
	bundle install

serve: install
	bundle exec jekyll serve --watch

build: install
	bundle exec jekyll build

sync-media:
	aws --profile alorenzi s3 sync media/immobili s3://alorenzi-eu-media/immobili
	aws --profile alorenzi s3 sync media/posts s3://alorenzi-eu-media/posts
	aws --profile alorenzi s3 cp media/avatar.png s3://alorenzi-eu-media/avatar.png
	aws --profile alorenzi s3 cp media/avatar-profile.jpg s3://alorenzi-eu-media/avatar-profile.jpg
	aws --profile alorenzi s3 cp media/banner.jpg s3://alorenzi-eu-media/banner.jpg

deploy: build sync-media
	rsync -av _site/ home:/srv/alorenzi_eu/
