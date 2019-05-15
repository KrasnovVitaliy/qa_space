#!/usr/bin/env bash

echo "Removing all containers"
docker rm $(docker ps -a -q)

echo "Removing all images"
docker rmi $(docker images -a -q)