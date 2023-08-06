#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import signal
import sys, time, subprocess
from typing import List

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import click
import jsonpickle

jsonpickle.set_encoder_options('json', sort_keys=True, indent=2)
jsonpickle.set_preferred_backend('json')


def log(s):
    print('[Monitor] %s' % s)


class MyFileSystemEventHander(FileSystemEventHandler):
    def __init__(self, fn, includes=None, excludes=None):
        super(MyFileSystemEventHander, self).__init__()

        self.includes = includes or ['.*?.py']
        self.excludes = excludes or ['.*?__pycache__.*?']
        self.restart = fn

    def on_any_event(self, event):
        if self._match_includes(event.src_path) and not self._match_excludes(event.src_path):
            log('Python source file changed: %s' % event.src_path)
            self.restart()

    def _match_includes(self, path):
        for item in self.includes:
            if re.match(item, path):
                return True
        return False

    def _match_excludes(self, path):
        for item in self.excludes:
            if re.match(item, path):
                return True
        return False


class HottingMonitor(object):
    filename = os.path.join(os.curdir, 'hottings.json')

    def __init__(self, version=1, includes=None, excludes=None):
        self.version = version
        self.tasks: List[HottingTask] = []

        self.includes = includes or ['.*?.py']
        self.excludes = excludes or ['.*?__pycache__.*?']

    @staticmethod
    def parse(base=None) -> 'HottingMonitor':
        HottingMonitor.filename = os.path.join(base, HottingMonitor.filename) if base else HottingMonitor.filename
        return jsonpickle.loads(open(HottingMonitor.filename, encoding='utf-8').read(),
                                classes=[HottingTask, HottingMonitor])

    def _start_tasks(self):
        for t in self.tasks:
            t.start()

    def start(self):
        try:
            self._start_tasks()
            self.watch()
        except FileNotFoundError as e:
            log(e)

    def watch(self):
        observer = Observer()
        log('Starting tasks :')
        for t in self.tasks:
            log('- {}'.format(t.name))
            if not t.reload:
                continue
            fs = MyFileSystemEventHander(t.restart, includes=self.includes, excludes=self.excludes)
            observer.schedule(fs, t.src, recursive=True)
            log('Watching directory %s...' % t.src)

        observer.start()

        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def save(self):
        js = jsonpickle.encode(self)
        open(self.filename, 'w').write(js)


class HottingTask(object):
    def __init__(self, name, cmd=None, src=None, reload=True, includes=None, excludes=None):
        """
        Define a task details.
        :param cmd: Command line to Execute
        :param src: Watching dir to reload
        :param reload:
        """
        self.name = name
        self.cmd = cmd
        self.src = src
        self.reload = reload

        self.includes = includes or ['.*?.py']
        self.excludes = excludes or ['.*?__pycache__.*?']

    def start(self):
        self.process = subprocess.Popen(self.cmd.split(' '), cwd=os.path.curdir, stdin=sys.stdin, stdout=sys.stdout,
                                        stderr=sys.stderr)

    def stop(self):
        self.process.send_signal(signal.SIGTERM)

    def kill(self):
        self.process.kill()

    def restart(self):
        self.kill()
        self.start()


@click.group()
def cli():
    """A command line tool to manage hot reload tasks"""
    from version import __version__

    log('Hottings version {version}'.format(version=__version__))
    pass


@cli.command(short_help='Init a hotting project')
@click.option('--force/--no-force', default=False)
def init(force):
    """Init a hotting project and generate a hottings.json file"""
    if os.path.exists(HottingMonitor.filename) and not force:
        log('Hottings.json file already exists')
        return
    HottingMonitor().save()


@cli.command()
@click.argument('name', metavar='<name>')
@click.argument('cmd', metavar='<cmd>')
@click.argument('src', metavar='<src>')
def add(name, cmd, src):
    """
    Add a new hotting task
    """
    monitor = HottingMonitor.parse()
    task = HottingTask(name, cmd=cmd, src=src)
    monitor.tasks.append(task)
    monitor.save()


@cli.command()
@click.argument('name')
def remove(name):
    """Remove a hotting task"""
    monitor = HottingMonitor.parse()
    monitor.tasks = [x for x in monitor.tasks if x.name != name]
    monitor.save()


@cli.command()
def list():
    """List all hotting task"""
    monitor = HottingMonitor.parse()
    for item in monitor.tasks:
        print('- {}'.format(item.name))


@cli.command()
def start():
    """Start all tasks"""
    monitor = HottingMonitor.parse()
    monitor.start()


if __name__ == '__main__':
    cli()
