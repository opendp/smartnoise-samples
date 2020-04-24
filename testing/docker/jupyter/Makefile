start:
	docker run  -p 8989:8989 --name whitenoise-run -d privacy:whitenoise

stop:
	docker stop whitenoise-run
	docker rm whitenoise-run

docker:	
	docker build --tag privacy:whitenoise .

list:
	docker container list

sqlcmd:
	sudo docker run -it --rm --network host -p 5432:5432 privacy:whitenoise psql -h 127.0.0.1 -U postgres

bashh:
	docker run -it --rm -p 8989:8989 privacy:whitenoise bash

bash:
	sudo docker exec -it whitenoise-run "bash"
