FROM mysql:latest

MAINTAINER me

ENV MYSQL_DATABASE=db \
    MYSQL_ROOT_PASSWORD=root

ADD /sql/init.sql /docker-entrypoint-initdb.d

EXPOSE 3306
