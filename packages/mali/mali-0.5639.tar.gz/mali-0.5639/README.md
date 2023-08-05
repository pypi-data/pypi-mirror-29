# MALI Command-Line Tool

## Setup

### Install Dependencies

- Install `virtualenv` which is used to created a sandboxed Python environment for individual project
```bash
pip install virtualenv
```

- Install dependencies
```bash 
make dev-requirements  # install libraries required for development and testing
```

- If you are using zsh, you might want to install `virtualenvwrapper` plugin which will auto activate the virtual environment when you `cd` to the directory.

### Configure Pycharm

- Open the root directory `<repo-root>` in PyCharm
- Open `Pycharm -> Preferences -> Project Interpreter`.
  - Click the Gear Wheel icon on the top right and choose `Add Local`
  - Navigate to the virtualenv python executable `<repo-root>/.venv/bin/python`
  - Click `Choose`
- In order to run tests in PyCharm, open `Run → Edit Configurations`. Then open `Defaults → Python Test  → Unittests`, fill in the parameters:
  - Working Directory: `<repo-root>`

## Running

### In terminal
At the project's root directory, run
```bash
pip install --editable .  
```

This would install `mali` command and run it with the latest local code. You don't need to reinstall the package after editing code.

### Quick start
You can start running mali by first authenticate yourself.
```bash
mali auth init  # authenticate
mali auth whoami  # display current authenticated user
mali projects list  # list all projects
mali --help  # show help page

# Add `--configPrefix staging` option to run against the GAE staging environment
mali --configPrefix staging auth init  # you only need to authenticate once
mali --configPrefix staging projects list  # list projects on staging
```

### In PyCharm
`mali.py` is the starting point script. In order to run and, more importantly, debug in PyCharm, 
- Open `Run → Edit Configurations`. 
- Click `+ → Python`, fill in the parameters:
  - Name: "Any thing you like, preferably the command you're testing e.g. `mali auth init`"
  - Script: `<repo-root>/mali.py`
  - Params: `--configPrefix staging auth init` (The options and arguments you would type in after `mali` in terminal)
  - Working directory: `<repo-root>`
- Click OK
- Press the Run/Debug icon.

The above is equivalent to running the following command in the terminal.
```bash
mali --configPrefix staging auth init
```

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

### In terminal
```bash
make test  # run tests under `tests` directory
```

To run tests under `tests_caffe` directory, we need to first install Docker in order to run Caffe library. Please follow instructions [here](https://docs.docker.com/docker-for-mac/install/).

```bash
make test-caffe  # run tests under `tests_caffe` directory
make test-all  # run all the tests
```

### In PyCharm
Right click on the test file (e.g. `test_auth.py`), the test class (e.g. `TestAuth`) or simply a single test method (e.g. `test_init_auth`), and click `Run 'Unnittests ...'` in the dropdown menu.
