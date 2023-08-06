import py
import click
import json

import os
HOME_DIR = os.getcwd()

class Config(dict):
    def __init__(self, *args, **kwargs):
        self.config = py.path.local(
            click.get_app_dir('clusterone')).join('config.json')

        self.home = HOME_DIR

        # retry behaviour, used when aquiring tport remote repo

        self.retry_count = 60 # times
        self.retry_interval = 1 # seconds

        super(Config, self).__init__(*args, **kwargs)

    def load(self):
        """load the JSON config file from disk"""
        try:
            self.update(json.loads(self.config.read()))
            # logger.info('Config file loaded.')
        except py.error.ENOENT:
            # logger.error('Cannot Load Config File')
            pass

    def save(self):
        self.config.ensure()
        with self.config.open('w') as f:
            f.write(json.dumps(self))
            # logger.info('Saving Clusterone Config File')

    def delete(self):
        self.config.ensure()
        self.config.remove()

