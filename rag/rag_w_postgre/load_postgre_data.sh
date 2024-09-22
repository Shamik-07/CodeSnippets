#!/bin/bash

# exports the DB env variables
export $(grep -v '^#' .env | xargs)
# loads the data into postgre DB
pg_restore --host=$DBHOST --username=$DBUSER --dbname=$DBNAME --password --verbose video_backup.db