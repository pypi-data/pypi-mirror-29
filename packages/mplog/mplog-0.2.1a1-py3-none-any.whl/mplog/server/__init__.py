
from gevent import monkey
monkey.patch_all()
from gevent.wsgi import WSGIServer
import urllib.parse

from .app import log_server
from ..config import ServerCfg


def start_server():
    from mplog import init_mplog_client
    
    server = WSGIServer((ServerCfg.HOST, ServerCfg.PORT), log_server)
    netloc = '{:s}:{}'.format(ServerCfg.HOST, ServerCfg.PORT)
    url = urllib.parse.urlunsplit(('http', netloc, '/', '', ''))
    print('mplog server is started. Listening at {:s}:{} '.format(ServerCfg.HOST, ServerCfg.PORT))
    print('The log records are available at {:s}'.format(url))

    init_mplog_client('mplog-server', ServerCfg.HOST, ServerCfg.PORT)
    server.serve_forever()

