#!/usr/bin/env bash

# Step 1: Install all the prerequisites including flyway
# Step 2: Download known_fis.txt file from s3 location
# Step 3: Get mysql password from the secrets prefix
# Step 4: Iterate through known_fis.txt file and create database schemas
# Step 5: Invoke flyway for map_config schema
# Step 6: Invoke flyway for fi specific schemas
# Step 7: Finis!

BUCKET=$2
HOST_NAME=$4
USER=$5
PORT=$6
MYSQL=mysql

install_prerequisites() {
	sudo yum install -y mysql jq

	echo "Downloading flyway"
	curl -o flyway.tar.gz https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/4.0.3/flyway-commandline-4.0.3-linux-x64.tar.gz
	echo "Extracting flyway"
	tar -C ~/ -xpvzf flyway.tar.gz
	echo "Copying migrations and config from S3"
	cd ~/flyway-4.0.3
}

get_known_fis_file() {
  echo "getting known_fis file"
  mkdir ~/known-fis
  aws s3 cp s3://${BUCKET}/config/known_fis.txt ~/known-fis
}

get_mysql_password() {
	echo "getting password"
	PASSWORD=`aws s3 cp s3://${BUCKET}/secrets/passwords.json - | jq '.aurora_master_password'`
}

create_mysql_fi_database() {
  echo "Creating DB schemas from known-fis"
  while read fi; do
    #Going to iterate over the output we just generated each loop will have a distinct fi
    COMMAND="CREATE DATABASE IF NOT EXISTS fi_${fi};"
    ${MYSQL} -h ${HOST_NAME} -P ${PORT} -u ${USER} \
      --password=`echo ${PASSWORD} | tr -d '"'` -e "${COMMAND}" || exit 1
  done < ~/known-fis/known_fis.txt
}

do_global_flyway_migration() {
	echo "Calling flyway...global"
	URL="jdbc:mysql://${HOST_NAME}:${PORT}/flyway"
	./flyway migrate -user=$USER -password=`echo ${PASSWORD} | tr -d '"'` -url=$URL -locations=filesystem:/${INPUT1_STAGING_DIR}/sql
}

do_fi_specific_migration() {
	# Let's get a list of all the fi's...
	mysql -h $HOST_NAME -P $PORT -u $USER --password=`echo ${PASSWORD} | tr -d '"'` -e "show databases like 'fi_%';" > fis.txt

	# First line of the Resultset from the above statement contains the column name "Database (fi_%)""
	# So, take the first line off the file we just created
	sed '1d' fis.txt > fi_list.txt

	# Iterate over the fi's and apply the migrations stored in the fi_specific_migrations folder to the fi database
	echo "Calling flyway...fi_specific"
	while read fi; do
	  #Invoke flyway here...
	  URL="jdbc:mysql://${HOST_NAME}:${PORT}/${fi}"
	  ./flyway migrate -user=$USER -password=`echo ${PASSWORD} | tr -d '"'` -url=$URL -locations=filesystem:/${INPUT1_STAGING_DIR}/fi_specific_migrations
	done < fi_list.txt
}

echo "start!"

# Step 1: Install all the prerequisites including flyway
install_prerequisites || exit 1

# Step 2: Download known_fis.txt file from s3 location
get_known_fis_file  || exit 1

# Step 3: Get mysql password from the secrets prefix
get_mysql_password  || exit 1

# Step 4: Iterate through known_fis.txt file and create database schemas
create_mysql_fi_database || exit 1

# Step 5: Invoke flyway for map_config schema
do_global_flyway_migration || exit 1

# Step 6: Invoke flyway for fi specific schemas
do_fi_specific_migration || exit 1

echo "finis!"
