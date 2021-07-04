#!/bin/sh

docker exec -it -d restapi /bin/bash -c 'uvicorn main:app --reload --host 0.0.0.0 --port 80'