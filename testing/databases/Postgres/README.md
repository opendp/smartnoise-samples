# Postgres Test Database Setup

You can use these scripts to set up a test docker container with the PUMS and PUMS_1000 datasets installed.

Make sure you have the `datasets` repository cloned in a folder that is a sibling to the folder where you have installed this samples repository.

```
git clone https://github.com/privacytoolsproject/datasets.git
```

Switch to this folder and install dependencies.

```
cd ~/Repos/burdock-samples/testing/databases/Postgres
python3 -m pip install -r requirements.txt
source packages.sh
```

Next, set a test password for Postgres to use:

```
export POSTGRES_PASSWORD=pass@word123
```

Finally, build the docker image and start it:

```
make docker
make start
```

You should now have a Postgres docker image running and listening on the default port.  To connect with the local client and verify that the databases have been created, you can connect with `make cmd`.

At the psql prompt, you can switch to PUMS and count records:

```
\c PUMS
SELECT COUNT(*) FROM PUMS.PUMS;
SELECT COUNT(*) FROM PUMS.PUMS_large;
```

You may now connect to the database using PostgresReader and PrivateReader, using the port and password specified.  To stop the running docker instance and delete it:

```
make stop
```

You can now repeatedly `make start` and `make stop` without needing to rbuild the docker image.