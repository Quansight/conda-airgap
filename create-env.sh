#!/bin/bash
# usage:
#   create-env.sh <channel> <env-name> <list of packages>

# create web and offline mirrors
echo "-----------------------------------------------------------------"
echo "Creating new envs from web and offline mirrors using packages: ${@:3}"
echo "-----------------------------------------------------------------"
conda create -y -n $2-from-web -c $1 --override-channels "${@:3}"
conda create -y -n $2-from-mirror -c ./mirrors/$1 --override-channels "${@:3}"
conda create -y --offline -n $2-from-mirror-offline -c ./mirrors/$1 --override-channels "${@:3}"

# save conda env package lists as json 
echo 'saving env package lists as json ...'
mkdir -p test-data
conda list -n $2-from-web --json > test-data/$2-from-web.json
conda list -n $2-from-mirror --json > test-data/$2-from-mirror.json
conda list -n $2-from-mirror-offline --json > test-data/$2-from-mirror-offline.json