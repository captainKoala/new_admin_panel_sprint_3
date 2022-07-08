#!make
include .env

# Docker container names
CONT_DB		= $(CONTAINER_PREFIX)db
CONT_APP	= $(CONTAINER_PREFIX)backend
CONT_NGINX	= $(CONTAINER_PREFIX)nginx
CONT_ES		= $(CONTAINER_PREFIX)es
CONT_ETL	= $(CONTAINER_PREFIX)etl
CONT__ALL	= $(CONT_DB) $(CONT_APP) $(CONT_NGINX) $(CONT_ES) $(CONT_ETL)

# Docker volumes
VOL_DB		= $(CONTAINER_PREFIX)postgres_data
VOL_ST		= $(CONTAINER_PREFIX)static_value
VOL_MD		= $(CONTAINER_PREFIX)media_value
VOL_ES		= $(CONTAINER_PREFIX)es
VOL_ETL		= $(CONTAINER_PREFIX)etl
VOL__ALL	= $(VOL_DB) \
			$(VOL_ST) \
			$(VOL_MD) \
			$(VOL_ES) \
			$(VOL_ETL) \


all:		up

init:		migrate collectstatic createsuperuser

up:
			docker-compose up -d

build:
			docker-compose up --build -d nginx es

migrate:
			docker exec -it ${CONT_APP} python manage.py migrate

collectstatic:
			docker exec -i ${CONT_APP} python manage.py collectstatic --noinput

createsuperuser:
			docker exec -i ${CONT_APP} python manage.py createsuperuser --noinput

restore:
			docker cp data/data.dump ${CONT_DB}:data.dump
			docker exec -i -e PGPASSWORD=${POSTGRES_PASSWORD} ${CONT_DB} pg_restore -d ${POSTGRES_DB} -h ${POSTGRES_HOST} -U ${POSTGRES_USER} data.dump

init_restore: init restore


etl:
			docker-compose up --build -d etl

stop:
			docker stop ${CONT__ALL}

rm_containers:
			$(foreach cn, $(CONT__ALL), docker rm $(cn);)

rm_volumes:
			$(foreach vol, $(VOL__ALL), docker volume rm $(vol);)

clean:		stop rm_containers

fclean:		clean rm_volumes

re:			clean all

.PHONY:		all clean fclean re up build migrate collectstatic createsuperuser stop rm_containers rm_volumes init init_restore es etl