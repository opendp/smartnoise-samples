start:
	sudo docker run --name mssql -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=$(SA_PASSWORD)' -p 1433:1433 -d privacy:mssql
	sleep 15
	sqlcmd -S 127.0.0.1 -U sa -P $(SA_PASSWORD) -i restore.sql
	sed 's/\"//g' ../../../../datasets/data/PUMS_california_demographics/data.csv | tail -n +2 > ./PUMS_large.stripped.csv
	sed 's/\"//g' ../../../../datasets/data/PUMS_california_demographics_1000/data.csv | tail -n +2  > ./PUMS.stripped.csv
	bcp PUMS.PUMS in ./PUMS.stripped.csv -S 127.0.0.1 -U sa -P $(SA_PASSWORD) -d PUMS -c -t ','
	bcp PUMS.PUMS_large in ./PUMS_large.stripped.csv -S 127.0.0.1 -U sa -P $(SA_PASSWORD) -d PUMS -c -t ','
	rm ./PUMS.stripped.csv
	rm ./PUMS_large.stripped.csv

stop:
	sudo docker stop mssql
	sudo docker rm mssql

docker:
	sudo docker build --tag privacy:mssql .

cmd:
	sudo docker exec -it mssql /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $(SA_PASSWORD)

bash:
	sudo docker exec -it mssql "bash"
