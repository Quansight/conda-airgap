"""test full mirror of quansight-small-test"""
import sys
import subprocess
import json
import shutil

import pytest


CHANNEL = 'quansight-small-test'

@pytest.fixture(scope='module')
def setup_mirror():
    print('setting up mirrors')
    subprocess.run(['./create-mirror.sh', CHANNEL])
    print('finish setting up mirrors')
    yield setup_mirror
    print('delete mirror')
    shutil.rmtree(f'mirrors/{CHANNEL}')


@pytest.fixture(scope='module')
def setup_mirror_server(setup_mirror):
    print('starting up HTTP server')
    proc = subprocess.Popen([sys.executable, "-m", "http.server", "8000"],
                            cwd='mirrors')
    yield proc
    proc.terminate()
    proc.wait()
    print('HTTP server shutdown')


@pytest.mark.parametrize("pkg_list", [['python'], ['python', 'conda']])
def test_env_creation(setup_mirror, pkg_list):
    env_name = '_'.join(pkg_list)
    subprocess.run(['./create-env.sh', CHANNEL, env_name, *pkg_list])

    fweb = f'test-data/{env_name}-from-web.json'
    fmirror = f'test-data/{env_name}-from-mirror.json'
    foffline = f'test-data/{env_name}-from-mirror-offline.json'

    assert _clean_json(fweb) == _clean_json(fmirror)
    assert _clean_json(fmirror) == _clean_json(foffline)


@pytest.mark.parametrize("pkg_list", [['python'], ['python', 'conda']])
def test_env_creation_http(setup_mirror_server, pkg_list):
    env_name = '_'.join(pkg_list)
    subprocess.run(['./create-env.sh', f"http://localhost:8000/{CHANNEL}",
                   env_name, *pkg_list])

    fweb = f'test-data/{env_name}-from-web.json'
    fmirror = f'test-data/{env_name}-from-mirror.json'
    foffline = f'test-data/{env_name}-from-mirror-offline.json'

    assert _clean_json(fweb) == _clean_json(fmirror)
    assert _clean_json(fmirror) == _clean_json(foffline)


def _clean_json(fname):
    # read json, strip 'base_url' and 'channel' fields since they will differ
    with open(fname) as f:
        data = json.load(f)

    clean = []
    for rec in data:
        del rec['base_url']
        del rec['channel']
        clean.append(rec)

    return sorted(clean, key=lambda d: sorted(d.items()))