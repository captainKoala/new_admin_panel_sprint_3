# How to

## Run project
1. First define the environment variables as described in the ```.env.example``` file.
2. If you run project in first time execute next (it prepare database and resore test data):
```commandline
make build
make init_restore
```
3. Run ETL-service
```commandline
make etl
```

If the project was run before, you can execute the next simple command:
```commandline
make
```

## Make usage
Use the ```make``` command for everything you need:
- ```make``` (without any parameter) - build and run in the background necessary docker containers, make database 
migrations, create superuser and finally fill your database with test data.
- ```make init``` - prepare project: make migrations, collect static files and create superuser
- ```make init_restore``` - expand ```make init``` command with restoring test data
- ```make etl``` - build and run ETL service
- ```make up``` - run project
- ```make build``` - run project and build containers before starting
- ```make stop``` - stop all project containers
- ```make clean``` - remove project docker containers (and stop them beforehand, if necessary)
- ```make fclean``` - remove project docker containers and volumes
- ```make re``` - remove project docker containers and rebuild project
- ```make migrate``` - make database migrations
- ```make collectstatic``` - collect static files
- ```make createsuperuser``` - create superuser (user data are defined in the ```.env```-file)
- ```make init_restore``` - restore test data
- ```make rm_containers``` - remove project docker containers
- ```make rm_volumes``` - remove project docker volumes
