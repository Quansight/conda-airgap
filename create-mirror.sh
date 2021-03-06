#!/bin/bash
# Creates local mirror of a conda channel
shopt -s globstar

display_usage() {
    echo "Creates local mirror of a conda channel"
    echo
    echo "Usage: create-mirror.sh <channel> [--clean-repodata] [flags]"
    echo "  channel: channel to be mirrored"
    echo "  --clean-repodata: ensure updated repodata.json files"
    echo "  flags: flags to pass to conda mirror"
	}

if [[ $# == 0 || $1 == "--help" ||  $1 == "-h" ]]
then
    display_usage
    exit 0
fi

if [[ $1 == "main" || $1 == "r" || $1 == "free" ]]; then
    url="https://repo.anaconda.com/pkgs/$1"
else
    url=$1
fi

if [[ $2 == "--clean-repodata" ]]; then
    echo Cleaning mirrors/$1/**/*repodata.json*
    rm -rf mirrors/$1/**/*repodata.json*
    flags_start=3
else
    flags_start=2
fi


# activate conda
eval "$(conda shell.bash hook)"

# create local mirror
echo "creating conda env with conda-mirror installed"
conda create -y -n mirror-env -c quansight -c conda-forge conda-mirror
conda activate mirror-env

echo "creating local mirror of $1 channel (linux-64, noarch)..."
export PYTHONWARNINGS=ignore
mkdir -p mirrors
mkdir -p tmp
conda mirror -vv --insecure --upstream-channel $url --target-directory mirrors/$1 \
    --temp-directory ./tmp --platform linux-64 "${@:$flags_start}"
echo "local mirror of linux-64 complete, starting noarch"
conda mirror -vv --insecure --upstream-channel $url --target-directory mirrors/$1 \
    --temp-directory ./tmp --platform noarch "${@:$flags_start}"
echo "local mirror of noarch complete"
rm -rf tmp
conda deactivate
