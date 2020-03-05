start:
	sudo docker run  -p 5432:5432 --name some-postgres -e 'POSTGRES_PASSWORD=$(POSTGRES_PASSWORD)' -d privacy:postgres

stop:
	sudo docker stop some-postgres
	sudo docker rm some-postgres

docker:
	cp ../*.csv .
	cat ../../../../datasets/data/PUMS_california_demographics/data.csv | tail -n +2 > PUMS_large.csv
	cat ../../../../datasets/data/PUMS_california_demographics_1000/data.csv | tail -n +2 > PUMS.csv
	sudo docker build --tag privacy:postgres .
	rm *.csv

list:
	sudo docker container list

cmd:
	sudo docker run -it --rm --network host -p 5432:5432 privacy:postgres psql -h 127.0.0.1 -U postgres

bash:
	sudo docker exec -it some-postgres "bash"

