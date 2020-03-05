# SQL Server Test Database Setup

You can use these scripts to set up a test docker container with the PUMS and PUMS_1000 datasets installed.

Make sure you have the `datasets` repository cloned in a folder that is a sibling to the folder where you have installed this samples repository.

```
git clone https://github.com/privacytoolsproject/datasets.git
```

Switch to this folder and install dependencies (use packages_mac.sh for MacOS).

```
cd ~/Repos/burdock-samples/testing/databases/Postgres
python3 -m pip install -r requirements.txt
source packages.sh
```

Next, set a test password for SQL Server to use:

```
export SA_PASSWORD=pass@word123
```

Finally, build the docker image and start it:

```
make docker
make start
```

You should now have a SQL Server docker image running and listening on the default port.  To connect with the local client and verify that the databases have been created, you can connect with `make cmd`.

At the sqlcmd prompt, you can switch to PUMS and count records:

```
USE PUMS;
GO
SELECT COUNT(*) FROM PUMS.PUMS;
SELECT COUNT(*) FROM PUMS.PUMS_large;
GO
```

You may now connect to the database using SqlServerReader and PrivateReader, using the port and password specified.  To stop the running docker instance and delete it:

```
make stop
```

You can repeatedly do `make start` and `make stop` without needing to rebuild the docker image.
