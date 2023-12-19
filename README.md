## Link to project source code

<https://github.com/kea-semester-1/Semester-Project>

## Project setup

### Run the following commands from the root of the project if you have AWK installed

* `make run`

### Run the command in docker-compose if you dont have AWK installed

* `docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build`

This will create the docker containers, with the project and databases running, this will also load the test data into the databases.

The project backend is deployed with Azure and can be viewed: <https://rpg-project.azurewebsites.net/api/docs>

The project frontend is deployed with Vercel and can be viewed: <https://semester-project-rd6f6hfc2-m-n-ms.vercel.app/login>

## Test data scripts

### Relation database scripts

<https://github.com/kea-semester-1/Semester-Project/tree/main/db-scripts>

Test data created on start up:
<https://github.com/kea-semester-1/Semester-Project/blob/main/rpg_api/web/startup_data_pg.py>

### Document and Graph Database scripts

We don't have any scripts for the Document or Graph databases as the test data for these implementations are handled by the backend application on start up.
For MongoDB: <https://github.com/kea-semester-1/Semester-Project/blob/main/rpg_api/web/startup_data_mongo.py>
For Neo4j: <https://github.com/kea-semester-1/Semester-Project/blob/main/rpg_api/web/startup_data_neo4j.py>
