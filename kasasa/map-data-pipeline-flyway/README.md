# All about Flyway and migrations  
This repo is a shameless copy of the Redshift migration pipeline. In the README is a lot of good stuff about how all that works. To learn more, go here:  
[Redshift Migration Pipeline](http://git.bvops.net/projects/DW/repos/dw-sql-migration-pipeline/browse)

If you are interested in how to write an "overlord" migration or something that needs to be copied to all FI specific databases, see this confluence page:  
[Confluence page on this tool](https://confluence.bancvue.com/display/DEV/The+MAP+RDS)


### Docker Compose

The `Dockerfile`, `docker-compose.yml`, and `flyway-docker-runner.sh` files exist purely for setting up a local db for development/testing.

`docker-compose up` should spin up a `map-data-pipeline-flyway_db_1` container with a MySQL 5.7 DB and then run `map-data-flyway_runner_1` to perform a migration. 
 
This will result in a database that has been migrated with 6 FIs specific DBs. The username/password can be located in the `docker-compose.yml` 