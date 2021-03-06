#!/usr/bin/env python3

import datetime
from datetime import timedelta
import os

import alembic.config
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
@click.option('--forever', is_flag=True)
def status(forever):
    """
    Shows the status, whether working or not? If working, how long has the
    current sessiono been.
    """
    pid, sid = db.get_currently_active() or (None, None)
    if pid:
        name, pid = db.get_project(pid)
        start, end, pid, sid, paid = db.get_session(sid)
        print(f'Working on project {pid} - "{name}"')
        while True:
            print(f'\rCurrent session duration: {datetime.datetime.now() - start}', end='')
            if not forever:
                break
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
    print('SID\tStart\t\t\t\tEnd\t\t\t\tPaid\tDuration')
    sessions = db.get_session(pid=idd)
    time = timedelta()
    for start, end, pid, sid, paid in sessions:
        curr_time = (end if end else datetime.datetime.now()) - start
        time += curr_time
        print(f'{sid}\t{start}\t{end}\t{paid}\t{curr_time}')
    print(f'Total time: {time}')

@command
def migrate():
    """
    Perform SQL migrations.
    """
    os.chdir(os.path.join(os.path.dirname(__file__)))
    args = [
        '--raiseerr',
        'upgrade', 'head',
    ]
    alembic.config.main(argv=args)

@command
@click.option('--sid', 'id', flag_value='sid', default=True)
@click.option('--pid', 'id', flag_value='pid')
@click.argument('idd')
@click.option('--paid/--unpaid', required=True)
def mark(id, idd, paid):
    """
    Mark a particular session as paid or unpaid.
    """
    if id == 'sid':
        db.set_session_paid_status(sid=idd, paid=paid)
    elif id == 'pid':
        db.set_session_paid_status(pid=idd, paid=paid)


if __name__ == '__main__':
    cli()
    db.close()
