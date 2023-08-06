from .monitors import cli, HottingMonitor, HottingTask


def main():
    cli()


__all__ = ['HottingTask', 'HottingMonitor', 'cli']
