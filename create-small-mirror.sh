#!/bin/bash
# usage:
#   create-mirror.sh <channel> 

# activate conda
eval "$(conda shell.bash hook)"

# create local mirror
conda create -y -n mirror-env -c conda-forge conda-mirror pytest
conda activate mirror-env

echo "creating local mirror of $1 channel (linux-64, noarch)..."
conda mirror -vv --upstream-channel $1 --target-directory mirrors/$1 --platform linux-64
conda mirror -vv --upstream-channel $1 --target-directory mirrors/$1 --platform noarch
conda deactivate mirror-env