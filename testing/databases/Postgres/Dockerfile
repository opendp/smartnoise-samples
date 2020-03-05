FROM library/postgres

RUN apt-get update
RUN apt-get -y install dos2unix

RUN mkdir /data
COPY install*.sql /data/
COPY *.csv /data/

COPY install.sh /docker-entrypoint-initdb.d/
RUN dos2unix /docker-entrypoint-initdb.d/*.sh