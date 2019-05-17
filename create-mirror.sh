#!/bin/bash
# Creates local mirror of a conda channel

display_usage() { 
    echo "Creates local mirror of a conda channel"
    echo "Usage: create-mirror.sh <channel>"
    echo "  channel: channel to be mirrored"
	} 

if [[ ( $# == "--help") ||  $# == "-h" ]] 
then 
    display_usage
    exit 0
fi

# activate conda
eval "$(conda shell.bash hook)"

# create local mirror
echo "creating conda env with conda-mirror installed"
conda create -y -n mirror-env -c conda-forge conda-mirror
conda activate mirror-env

echo "creating local mirror of $1 channel (linux-64, noarch)..."
conda mirror -vv --upstream-channel $1 --target-directory mirrors/$1 --platform linux-64
conda mirror -vv --upstream-channel $1 --target-directory mirrors/$1 --platform noarch
conda deactivate