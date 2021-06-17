start:
	docker run --rm -p 8989:8989 --name smartnoise-run privacy:smartnoise

stop:
	docker stop smartnoise-run
	docker rm smartnoise-run

docker:	
	docker build --tag privacy:smartnoise .

bash:
	docker exec -it smartnoise-run bash

clean:
	docker system prune -a

publish:
	docker tag privacy:smartnoise opendp/smartnoise:privacy
	docker login
	docker push opendp/smartnoise:privacy