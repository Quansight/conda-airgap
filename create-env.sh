#!/bin/bash
# Creates 3 conda envs based on a package list: from-web, from-mirror and from-mirror with offline flag

display_usage() {
    echo "Creates 3 conda envs based on a package list: from-web, from-mirror and from-mirror with offline flag"
    echo
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
if [[ $1 == http://* ]]; then
  # channel argument is URL
  echo "Using URL channel $1"
  web_uri=$(basename $1)
  local_uri=$1
else
  # channel argument is name
  echo "Using channel name $1"
  web_uri=$1
  local_uri=./mirrors/$1
fi
conda create -y -n $2-from-web -c $web_uri --override-channels "${@:3}"
conda create -y -n $2-from-mirror -c $local_uri --override-channels "${@:3}"
conda create -y --offline -n $2-from-mirror-offline -c $local_uri --override-channels "${@:3}"
conda clean -all -y

# save conda env package lists as json
echo 'saving env package lists as json ...'
mkdir -p test-data
conda list -n $2-from-web --json > test-data/$2-from-web.json
conda list -n $2-from-mirror --json > test-data/$2-from-mirror.json
conda list -n $2-from-mirror-offline --json > test-data/$2-from-mirror-offline.json