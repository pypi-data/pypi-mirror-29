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
        self.excludes = excludes or []
        self.restart = fn

    def on_any_event(self, event):
        log('Python source file changed: %s' % event.src_path)

        for item in self.includes:
            print(item, event.src_path)
            if re.match(item, event.src_path):
                self.restart()


class HottingMonitor(object):
    filename = 'hottings.json'

    def __init__(self, version=1, includes=None, excludes=None):
        self.version = version
        self.tasks: List[HottingTask] = []

        self.includes = includes
        self.excludes = excludes

    @staticmethod
    def parse() -> 'HottingMonitor':
        return jsonpickle.loads(open(HottingMonitor.filename, encoding='utf-8').read(),
                                classes=[HottingTask, HottingMonitor])

    def start(self):
        for t in self.tasks:
            t.start()

    def start_and_watch(self):
        try:
            self.start()
            self.watch()
        except FileNotFoundError as e:
            log(e)

    def watch(self):
        observer = Observer()
        for t in self.tasks:
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

        self.includes = includes or []
        self.excludes = excludes or []

    def start(self):
        self.process = subprocess.Popen(self.cmd.split(' '), stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

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
def start():
    """Start all tasks"""
    monitor = HottingMonitor.parse()
    monitor.start_and_watch()


if __name__ == '__main__':
    cli()
