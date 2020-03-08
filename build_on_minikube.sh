#!/bin/bash

eval $(minikube docker-env)
docker build . -t api-example
eval $(minikube docker-env -u)