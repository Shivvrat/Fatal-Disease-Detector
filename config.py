import os

INSTANCE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'instance/')
LOG_DIR = os.path.join(INSTANCE_DIR, 'logs')
DATABASE_NAME = 'medmap.sqlite'
DATABASE_PATH = os.path.join(INSTANCE_DIR, DATABASE_NAME)
