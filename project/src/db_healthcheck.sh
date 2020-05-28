#!/bin/bash
service mysql status;
service mysql status | grep "is running";
#LOG=$(docker inspect --format='{{.LogPath}}' QA-Atom-Mysql) && grep \"socket: '/var/run/mysqld/mysqld.sock'  port: 3306\" $LOG;
