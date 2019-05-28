#!/usr/bin/env python3

import datetime

import click

from .db import db


@click.group()
def cli():
    pass


def command(fn):
    fn = click.command()(fn)
    cli.add_command(fn)
    return fn

@command
@click.argument('name')
def new(name):
    """
    Creates a new project.
    """
    db.add_project(name)
    print(f'Project {name} created successfully')

@command
def ls():
    """
    Shows the list of all current projects.
    """
    print('ID\tName')
    for name, idd in db.get_projects():
        print(f'{idd}\t{name}')

@command
def status():
    """
    Shows the status, whether working or not? If working, how long has the
    current sessiono been.
    """
    pid, sid = db.get_currently_active() or (None, None)
    if pid:
        name, pid = db.get_project(pid)
        start, end, pid, sid = db.get_session(sid)
        print(f'Working on project {pid} - "{name}"')
        print(f'Current session duration: {datetime.datetime.now() - start}')
    else:
        print('Not working on anything as of now.')

@command
@click.argument('idd')
def start(idd):
    """
    Start a new work session on a given project.
    """
    status = db.start(idd)
    if status:
        print(f'Project {idd} started successfully')
    else:
        print('Another project is running, stop it before you can start working on another')

@command
def stop():
    """
    Stop current work session.
    """
    pid, sid = db.stop()
    print(f'Session {sid} of project {pid} stopped successfully')

@command
@click.argument('idd')
def show(idd):
    """
    Show work sessions of a particular project.
    """
    print('SID\tStart\t\t\t\tEnd')
    sessions = db.get_session(pid=idd)
    for start, end, pid, sid in sessions:
        print(f'{sid}\t{start}\t{end}')


if __name__ == '__main__':
    cli()
