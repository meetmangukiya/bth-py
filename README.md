# bth-py

Supposed to be like the upwork time tracker i.e. a time tracking application
for your freelance projects that are not on upwork but when you'd like to
produce some proof for your employer.

## Installation

1. Install from source
    `pip install -e .`
2. Install from PyPI
    `pip install bth`

## Usage

```
Usage: bth [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  ls      Shows the list of all current projects.
  new     Creates a new project.
  show    Show work sessions of a particular project.
  start   Start a new work session on a given project.
  status  Shows the status, whether working or not? If working, how long
          has...
  stop    Stop current work session.
```
