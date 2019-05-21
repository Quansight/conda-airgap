# test full mirror of quansight-small-test

import pytest
import subprocess
import json
import shutil

CHANNEL = 'quansight-small-test'

@pytest.fixture(scope='module')
def repo():
    print('setting up mirrors')
    subprocess.run(['./create-mirror.sh', CHANNEL, '--config', 'test-data/test_blacklist.yml'])
    print('finish setting up mirrors')
    with open(f'mirrors/{CHANNEL}/linux-64/repodata.json', 'r') as f:
        repo = json.load(f)
    yield repo
    print('delete mirror')
    shutil.rmtree(f'mirrors/{CHANNEL}')

@pytest.mark.parametrize("pattern", ['py27', 'py35', 'py36'])
def test_blacklist_build(repo, pattern):
    builds = [v['build'] for v in repo['packages'].values()]
    assert not any(pattern in s for s in builds)
    

@pytest.mark.parametrize("build_number", [1003, 1004])
def test_blacklist_build_number(repo, build_number):
    build_numbers = [v['build_number'] for v in repo['packages'].values()]
    assert build_number not in build_numbers