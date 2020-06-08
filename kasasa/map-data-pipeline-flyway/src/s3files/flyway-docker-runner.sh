#!/usr/bin/env bash

# Step 1: Iterate through known_fis.txt file and create database schemas
# Step 2: Invoke flyway for map_config schema
# Step 3: Invoke flyway for fi specific schemas
# Step 4: Grant admin user permission
# Step 5: Finis!

HOST_NAME=${MYSQL_HOST}
USER=${MYSQL_ROOT}
PASSWORD=${MYSQL_ROOT_PASSWORD}
PORT=${MYSQL_PORT}
MYSQL=mysql

wait_for_db_container() {
  until ${MYSQL} -h ${HOST_NAME} -P ${PORT} -u ${USER} --password=`echo ${PASSWORD}` -e 'show databases;'; do
    >&2 echo "MySQL is unavailable - sleeping..."
    sleep 10
  done

  >&2 echo "MySQL is up - continuing"
}

create_mysql_fi_database() {
  cd ./flyway-4.0.3
  echo "Creating DB schemas from known-fis"
  while read fi; do
    #Going to iterate over the output we just generated each loop will have a distinct fi
    COMMAND="CREATE DATABASE IF NOT EXISTS fi_${fi};"
    ${MYSQL} -h ${HOST_NAME} -P ${PORT} -u ${USER} \
      --password=`echo ${PASSWORD} | tr -d '"'` -e "${COMMAND}" || exit 1
  done < /src/known_fis/known_fis.txt
}

do_global_flyway_migration() {
  echo "Creating flywaydb"
  COMMAND="CREATE DATABASE IF NOT EXISTS flyway;"
    ${MYSQL} -h ${HOST_NAME} -P ${PORT} -u ${USER} \
      --password=`echo ${PASSWORD} | tr -d '"'` -e "${COMMAND}" || exit 1
	echo "Calling flyway...global"
	URL="jdbc:mysql://${HOST_NAME}:${PORT}/flyway"
	./flyway migrate -user=$USER -password=`echo ${PASSWORD} | tr -d '"'` -url=$URL -locations=filesystem:/src/s3files/sql
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
	  ./flyway migrate -user=$USER -password=`echo ${PASSWORD} | tr -d '"'` -url=$URL -locations=filesystem:/src/s3files/fi_specific_migrations
	done < fi_list.txt
}

grant_user_permissions() {
  echo
  echo "Granting permissions to admin user."
  COMMAND="GRANT ALL PRIVILEGES ON *.* TO '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';"
  ${MYSQL} -h ${HOST_NAME} -P ${PORT} -u ${USER} \
      --password=`echo ${PASSWORD} | tr -d '"'` -e "${COMMAND}" || exit 1
}

echo "start!"
wait_for_db_container || exit 1

# Step 1: Iterate through known_fis.txt file and create database schemas
create_mysql_fi_database || exit 1

# Step 2: Invoke flyway for map_config schema
do_global_flyway_migration || exit 1

# Step 3: Invoke flyway for fi specific schemas
do_fi_specific_migration || exit 1

# Step 4: Grant admin user permission
grant_user_permissions || exit 1

echo
echo "finis!"
