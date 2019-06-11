# bth-py

Supposed to be like the upwork time tracker i.e. a time tracking application
for your freelance projects that are not on upwork but when you'd like to
produce some proof for your employer.

**Note: Install from source until we have continuous deployment to PyPI since
this is currently WIP and under development.**

## Installation

1. Install from source
    `pip install -e .`
<!--2. Install from PyPI-->
<!--`pip install bth`-->

## Usage

```
Usage: bth [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  ls       Shows the list of all current projects.
  mark     Mark a particular session as paid or unpaid.
  migrate  Perform SQL migrations.
  new      Creates a new project.
  show     Show work sessions of a particular project.
  start    Start a new work session on a given project.
  status   Shows the status, whether working or not? If working, how long...
  stop     Stop current work session.
```

| Use case | Command |
| -------- | ------- |
| Create a new project | `bth new "project name"` |
| List all the projects | `bth ls` |
| Start a work session for a given project | `bth start <pid>`. You can check pid of a project from the output of `bth ls`|
| Stop current work session | `bth stop` |
| See all the work sessions of a given project | `bth show <pid>`|
| See the current status, any active projects? how long? | `bth status` |
| Perform a SQL migration after update | `bth migrate` |
