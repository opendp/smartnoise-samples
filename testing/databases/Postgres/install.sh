#!/bin/bash

export PGUSER=postgres
psql <<- SHELL
  CREATE USER docker;
  CREATE DATABASE "PUMS";
  GRANT ALL PRIVILEGES ON DATABASE "PUMS" TO docker;
SHELL

psql -U postgres -d PUMS < /data/install_pums.sql
