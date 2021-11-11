# Python: Asynchronous Python client for the Openmotics API

[![GitHub Release][releases-shield]][releases]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE.md)

[![Build Status][build-shield]][build]
[![Code Coverage][codecov-shield]][codecov]
[![Code Quality][code-quality-shield]][code-quality]

Asynchronous Python client for the OpenMotics API.

## About

An asynchronous python client for the OpenMotics API to control the outputs.

This library is created to support the integration in
[Home Assistant](https://www.home-assistant.io).

## Installation

```bash
cd python-openmotics
pip install .
```

## Usage

```python
import pyopenmotics

om_cloud = BackendClient("client_id", "client_secret")
om_cloud.get_token()

installs = om_cloud.base.installations.all()
for install in installs:
    print("- {}".format(install))
print(install["id"])

outputs = om_cloud.base.installations.status_by_id(install["id"])
print(outputs)
```

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality. The format of the log is based on
[Keep a Changelog][keepchangelog].

Releases are based on [Semantic Versioning][semver], and use the format
of `MAJOR.MINOR.PATCH`. In a nutshell, the version will be incremented
based on the following:

- `MAJOR`: Incompatible or major changes.
- `MINOR`: Backwards-compatible new features and enhancements.
- `PATCH`: Backwards-compatible bugfixes and package updates.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

In case you'd like to contribute, a `Makefile` has been included to ensure a
quick start.

```bash
make venv
source ./venv/bin/activate
make dev
```

Now you can start developing, run `make` without arguments to get an overview
of all make goals that are available (including description):

```bash
$ make
Asynchronous Python client for the OpenMotics API.

Usage:
  make help                            Shows this message.
  make dev                             Set up a development environment.
  make lint                            Run all linters.
  make lint-black                      Run linting using black & blacken-docs.
  make lint-flake8                     Run linting using flake8 (pycodestyle/pydocstyle).
  make lint-pylint                     Run linting using PyLint.
  make lint-mypy                       Run linting using MyPy.
  make test                            Run tests quickly with the default Python.
  make coverage                        Check code coverage quickly with the default Python.
  make install                         Install the package to the active Python's site-packages.
  make clean                           Removes build, test, coverage and Python artifacts.
  make clean-all                       Removes all venv, build, test, coverage and Python artifacts.
  make clean-build                     Removes build artifacts.
  make clean-pyc                       Removes Python file artifacts.
  make clean-test                      Removes test and coverage artifacts.
  make clean-venv                      Removes Python virtual environment artifacts.
  make dist                            Builds source and wheel package.
  make release                         Release build on PyP
  make venv                            Create Python venv environment.
```

## Authors & contributors

The original setup of this repository is by [Wouter Coppens][woutercoppens].

For a full list of all authors and contributors,
check [the contributor's page][contributors].

## License

This project is licensed under the AGPLv3 License - see the LICENSE.md file for details

[build-shield]: https://github.com/woutercoppens/python-openmotics/workflows/Continuous%20Integration/badge.svg
[build]: https://github.com/woutercoppens/python-openmotics/actions
[contributors]: https://github.com/woutercoppens/python-openmotics/graphs/contributors
[woutercoppens]: https://github.com/woutercoppens/python-openmotics
[keepchangelog]: http://keepachangelog.com/en/1.0.0/
[maintenance-shield]: https://img.shields.io/maintenance/yes/2021.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[releases]: https://github.com/woutercoppens/python-openmotics/releases
[semver]: http://semver.org/spec/v2.0.0.html
