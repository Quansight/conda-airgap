#!/bin/bash
# Creates 3 conda envs based on a package list: from-web, from-mirror and from-mirror with offline flag

display_usage() { 
    echo "Creates 3 conda envs based on a package list: from-web, from-mirror and from-mirror with offline flag"
    echo "Usage: $0 <channel> <env-name> <packages>"
    echo "  channel: name of conda channel & mirror"
    echo "  env-name: base name of conda environments being created"
    echo "  packages: list of packages to install"
	} 

if [[ $# == 0 || $1 == "--help" ||  $1 == "-h" ]] 
then
    display_usage
    exit 0
fi

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