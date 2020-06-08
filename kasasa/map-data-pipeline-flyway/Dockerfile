FROM centos

WORKDIR /src

RUN yum install -y mysql jq

RUN mkdir known_fis
RUN (echo 2550; echo 2551; echo 2554; echo 2564; echo 52124; echo 99999) > known_fis/known_fis.txt

WORKDIR /src/s3files

RUN echo "Downloading flyway" && curl -o flyway.tar.gz https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/4.0.3/flyway-commandline-4.0.3-linux-x64.tar.gz
RUN echo "Extracting flyway" && tar -C ./ -xpvzf flyway.tar.gz

COPY ./src /src

RUN sed -i -e 's/`end_date` timestamp/`end_date` timestamp NULL/g' sql/V2201708071019__Add_map_configfico_orders_active.sql


CMD ./flyway-docker-runner.sh