start:
	docker run  -p 8989:8989 --name whitenoise-run -d privacy:whitenoise

stop:
	docker stop whitenoise-run
	docker rm whitenoise-run

docker:	
	docker build --tag privacy:whitenoise .

bash:
	docker run -it --rm -p 8989:8989 privacy:whitenoise bash

