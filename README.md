# conda-airgap

[![Build Status](https://dev.azure.com/quansight/conda-airgap/_apis/build/status/Quansight.conda-airgap?branchName=master)](https://dev.azure.com/quansight/conda-airgap/_build/latest?definitionId=2&branchName=master)

Conda-airgap provides tools for creating mirrors of conda channels locally.
These are suitable to be transported to airgap systems.

## Usage

The main entrypoint for these tools is the `create-mirror.sh` script.

In its simplest usage, you pass the name of the channel you would like to
clone and it will pull down all linux-64 and noarch artifacts on the channel.
The following will create a mirror for the main channel (which is big):

```bash
$ ./conda-mirror.sh main
```

If you want to test this on a very small channel, feel free to use
`quansight-small-test`:

```bash
$ ./conda-mirror.sh quansight-small-test
```

`conda-mirror.sh` will create a directory structure of
`./mirrors/<channel-name>/<platform>/<artifacts>`, where:

* `channel-name` is the name of the channel you passed (e.g. `main` or `conda-forge`)
* `platform` is the target  architechture (e.g. `linux-64` or `noarch`)
* `artifacts` are the artifact tarball files (`.tar.bz2`) as well as `repodata.json`

### Using  the channel

To use this channel locally via your filesystem, you can modify your `condarc` file
to point to the correct directory.

```yaml
channels:
  - /path/to/mirrors/main
```

You can also host these file via a simple webserver in the mirrors directory:

```bash
$ cd mirrors
$ python -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

and then modify your `condarc` file to have the following:

```yaml
channels:
  - http://0.0.0.0:8000/main
```

### Updating the mirror

In certain situations, you may already have most of the channel downloaded and
available. However, the channel has been updated upstream and you do not
want to have to re-clone the entire channel. In order to avoid this overhead
and only grab the new packages, pass the `--clean-repodata` flag in after the
channel name. For example,

```bash
$ ./conda-mirror.sh main --clean-repodata
```

This downloads the latest copy of `repodata.json` for the channel. Mirroring
will see that most of the artifacts are already present, and skip those.

## Testing

conda-airgap is well tested, and most of the files in this repository
are there in support of the test suite. To execute the tests, run `pytest -sv`
in the root directory.

## Other Notes

The `create-mirror.sh` file uses a slightly modified version of the `conda-mirror`
project to support airgap scenarios.  Development releases are available on the
`quansight` channel on anaconda.org.  The `create-mirror.sh` script installs this
version of conda-mirror for you, so normally you do not need to worry about this.
The tracking branch for these changes is available
[here](https://github.com/Quansight/conda-mirror/tree/0.8.1.dev).
