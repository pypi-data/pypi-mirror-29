# MisingLink SDK

## Setup

### Install Dependencies

- Install `virtualenv` which is used to created a sandboxed Python environment for individual project
```bash
pip install virtualenv
```

- Install dependencies
```bash 
make dev-requirements  # install libraries used in development and testing
```

- If you are using zsh, you might want to install `virtualenvwrapper` plugin which will auto activate the virtual environment when you `cd` to the directory.

### Configure Pycharm

- Open the root directory `<missinglink-callback-root>` in PyCharm
- Open `Pycharm -> Preferences -> Project Interpreter`.
  - Click the Gear Wheel icon on the top right and choose `Add Local`
  - Navigate to the virtualenv python executable `<repo-root>/.venv/bin/python`
  - Click `Choose`

In order to get the tests to run in PyCharm, go under `Run -> Edit Configurations -> Python Tests -> Nosetests`
  - Give it name
  - select "Path" option
  - add "./tests"
  - In `Working Directory`, click `...` and change the directory to `<repo-root>`
  - Python interpreter: select your .venv related.
  - select "add content roots to PYTHONPATH"
  - select "add source roots to PYTHONPATH"

## Linting

We use [pycodestyle](https://pycodestyle.readthedocs.io/en/latest/index.html) for linting. If you haven't, please read the [PEP 8 style guide for Python](https://www.python.org/dev/peps/pep-0008/#introduction).

Quick notes:
- We are not dogmatic regarding line width (E501 is ignored) but be reasonable!
- To disable the linter for a specific line, postfix the line with `# nopep8`. For example,
```python
import os  # nopep8
```

### In terminal

To lint, run the following command
```bash
make lint
```

### In PyCharm

PyCharm supports code style and inspections using PEP 8 so you can reformat by selecting `Code > Reformat Code` (or `Alt + Cmd + L`) for a specific file or a directory. 

Please note that PyCharm enforces line width by default so you might want to disable that.

## Tests

Because different libraries have different settings (e.g. Caffe needs to be run on Docker), we have a few test directories:
- `tests_caffe`: for testing Caffe.
- `tests_keras`: for testing Keras. This test suite will be run with both Theano and Tensorflow backends.
- `tests`: the rest of tests.

In order to run `tests_caffe`, we need to first install Docker in order to run Caffe library. Please follow instructions [here](https://docs.docker.com/docker-for-mac/install/).

### In terminal
```bash
make test  # Run tests in `tests` suite
make test-keras-tensorflow  # Run tests in `tests_keras` using Tensorflow backend
make test-keras-theano  # Run tests in `tests_keras` using Theano backend
make test-keras  # Run tests in `tests_keras` with both backends
make test-caffe  # Run tests in `tests_caffe`
make test-all  # Run every tests and configurations
```

### In PyCharm
Right click on the test file (e.g. `TestKerasCallback.py`), the test class (e.g. `TestKerasCallback`) or simply a single test method (e.g. `test_calls`), and click `Run 'Unnittests ...'` in the dropdown menu.
