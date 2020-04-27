start:
	docker run --rm -p 8989:8989 --name whitenoise-run privacy:whitenoise

stop:
	docker stop whitenoise-run
	docker rm whitenoise-run

docker:	
	docker build --tag privacy:whitenoise .

bash:
	docker exec -it whitenoise-run bash

