## Project setup

### Run the following commands from the root of the project if you have AWK installed

* `make run`

### Run the command in docker-compose if you dont have AWK installed

* `docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build`

This will create the docker containers, with the project and databases running.

The project backend is deployed with Azure and can be viewed: <https://rpg-project.azurewebsites.net/api/docs>

The project frontend is deployed with Vercel and can be viewed: <https://semester-project-rd6f6hfc2-m-n-ms.vercel.app/login>
