# test full mirror of quansight-small-test

import pytest
import subprocess
import json
import shutil

CHANNEL = 'quansight-small-test'

@pytest.fixture(scope='module')
def repo():
    print('setting up mirrors')
    subprocess.run(['./create-mirror.sh', CHANNEL, '--config', 'test-data/test_whitelist.yml'])
    print('finish setting up mirrors')
    with open(f'mirrors/{CHANNEL}/linux-64/repodata.json', 'r') as f:
        repo = json.load(f)
    yield repo
    print('delete mirror')
    shutil.rmtree(f'mirrors/{CHANNEL}')    

@pytest.mark.parametrize("build_number", [1003, 1004])
def test_whitelist_zlib_build_number(repo, build_number):
    builds = [v['build_number'] for v in repo['packages'].values() if 'zlib' in v['name']]
    assert build_number in builds