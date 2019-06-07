"""test full mirror of quansight-small-test"""
import os
import sys
import subprocess
import json
import shutil

import pytest


CHANNEL = "quansight-small-test"
CONDARC = os.path.join(os.path.dirname(__file__), 'condarc')
PROXY_SETTINGS = {
    "HTTP_PROXY": "http://fake.proxy.server/",
    "HTTPS_PROXY": "https://fake.proxy.server/",
    "NO_PROXY": "localhost,127.0.0.1,0.0.0.0",
    "http_proxy": "http://fake.proxy.server/",
    "https_proxy": "https://fake.proxy.server/",
    "no_proxy": "localhost,127.0.0.1,0.0.0.0",
}


@pytest.fixture(scope="module")
def setup_mirror():
    print("setting up mirrors")
    subprocess.run(["./create-mirror.sh", CHANNEL])
    print("finish setting up mirrors")
    yield setup_mirror
    print("delete mirror")
    shutil.rmtree(f"mirrors/{CHANNEL}")


@pytest.fixture(scope="module")
def setup_mirror_server(setup_mirror):
    print("starting up HTTP server")
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000"], cwd="mirrors"
    )
    yield proc
    proc.terminate()
    proc.wait()
    print("HTTP server shutdown")


@pytest.mark.parametrize("pkg_list", [["python"], ["python", "conda"]])
def test_env_creation(setup_mirror, pkg_list):
    env_name = "_".join(pkg_list)
    subprocess.run(["./create-env.sh", CHANNEL, env_name, *pkg_list])

    fweb = f"test-data/{env_name}-from-web.json"
    fmirror = f"test-data/{env_name}-from-mirror.json"
    foffline = f"test-data/{env_name}-from-mirror-offline.json"

    assert _clean_json(fweb) == _clean_json(fmirror)
    assert _clean_json(fmirror) == _clean_json(foffline)


@pytest.mark.parametrize("pkg_list", [["python"], ["python", "conda"]])
def test_env_creation_http(setup_mirror_server, pkg_list):
    env_name = "_".join(pkg_list)
    subprocess.run(
        ["./create-env.sh", f"http://localhost:8000/{CHANNEL}", env_name, *pkg_list]
    )

    fweb = f"test-data/{env_name}-from-web.json"
    fmirror = f"test-data/{env_name}-from-mirror.json"
    foffline = f"test-data/{env_name}-from-mirror-offline.json"

    assert _clean_json(fweb) == _clean_json(fmirror)
    assert _clean_json(fmirror) == _clean_json(foffline)


@pytest.mark.parametrize("pkg_list", [["python"], ["python", "conda"]])
def test_env_creation_http_no_proxy(setup_mirror_server, pkg_list):
    # add some bad proxy setting to make sure that we are really getting local
    # packages only.
    env_name = "_".join(pkg_list)
    env = dict(os.environ)
    env.update(PROXY_SETTINGS)

    subprocess.run(
        ["./create-env.sh", f"http://localhost:8000/{CHANNEL}", env_name, *pkg_list],
        env=env
    )

    fweb = f"test-data/{env_name}-from-web.json"
    fmirror = f"test-data/{env_name}-from-mirror.json"
    foffline = f"test-data/{env_name}-from-mirror-offline.json"

    assert _clean_json(fweb) == _clean_json(fmirror)
    assert _clean_json(fmirror) == _clean_json(foffline)


def check_only_offline(env, pkg_list):
    env_name = "_".join(pkg_list)
    print("-----------------------------------------------------------------")
    print(f"Creating new envs from web and offline mirrors using packages: {pkg_list}")
    print("-----------------------------------------------------------------")
    p = subprocess.run(["conda", "config", "--show"], env=env)
    p.check_returncode()
    p = subprocess.run(
        ["conda", "create", "-y", "-n", env_name + "-from-mirror-offline", *pkg_list],
        env=env,
    )
    p.check_returncode()
    p = subprocess.run(["conda", "clean", "--all", "-y"], env=env)
    p.check_returncode()

    print("saving env package lists as json ...")
    os.makedirs("test-data", exist_ok=True)
    foffline = f"test-data/{env_name}-from-mirror-offline.json"
    with open(foffline, "wb") as f:
        p = subprocess.run(
            ["conda", "list", "--json", "-n", env_name + "-from-mirror-offline"],
            env=env,
            stdout=f,
        )
        p.check_returncode()

    # check that we actually got the packages we expected to
    data = _clean_json(foffline)
    pkg_names = {rec["name"] for rec in data}
    assert set(pkg_list) <= pkg_names


@pytest.mark.parametrize("pkg_list", [["python"], ["python", "conda"]])
def test_env_creation_condarc(setup_mirror_server, pkg_list):
    env = dict(os.environ)
    env["CONDARC"] = CONDARC
    check_only_offline(env, pkg_list)


@pytest.mark.parametrize("pkg_list", [["python"], ["python", "conda"]])
def test_env_creation_condarc_no_proxy(setup_mirror_server, pkg_list):
    env = dict(os.environ)
    env["CONDARC"] = CONDARC
    env.update(PROXY_SETTINGS)
    check_only_offline(env, pkg_list)


def _clean_json(fname):
    # read json, strip 'base_url' and 'channel' fields since they will differ
    with open(fname) as f:
        data = json.load(f)

    clean = []
    for rec in data:
        del rec["base_url"]
        del rec["channel"]
        clean.append(rec)

    return sorted(clean, key=lambda d: sorted(d.items()))
