
import os


class ServerCfg(object):
    HOST = '127.0.0.1'
    PORT = 41054

class DatabaseCfg(object):

    ROOT_DIR = os.getcwd()
    DATABASE_NAME = 'mplog-server.sqlite'

    MAX_FETCH = 1000





