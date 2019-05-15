#!/bin/bash

# activate conda
eval "$(conda shell.bash hook)"

# create local mirror
conda create -y -n mirror-env -c conda-forge conda-mirror pytest
conda activate mirror-env

echo 'creating local mirror of quansight-small-test channel ...'
conda mirror -vv --upstream-channel quansight-small-test --target-directory mirror --platform linux-64
conda mirror -vv --upstream-channel quansight-small-test --target-directory mirror --platform noarch
conda deactivate mirror-env

# create web and offline mirror
echo 'creating new envs ...'
conda create -y -n small-from-web -c quansight-small-test --override-channels python=3.7 conda
conda create -y -n small-from-mirror -c ./mirror --override-channels python=3.7 conda
conda create -y --offline -n small-from-mirror-offline -c ./mirror --override-channels python=3.7 conda

# create conda env package lists as json 
echo 'saving env package lists as json ...'
conda list -n small-from-web --json > small-from-web.json
conda list -n small-from-mirror --json > small-from-mirror.json
conda list -n small-from-mirror-offline --json > small-from-mirror-offline.json

echo '-------------------------------'
cat small-from-web.json
echo '-------------------------------'
cat small-from-mirror.json
echo '-------------------------------'
cat small-from-mirror-offline.json