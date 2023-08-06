import time
import sys
import logging
import urllib.request
import urllib.parse
import urllib.error
import json


from .config import ServerCfg

TIME_FORMATTER = '%Y-%m-%d %H:%M:%S'
MSEC_FORMATTER = '.%03d'

LEVEL_DICT ={
    0:'NOTSET',
    10:'DEBUG',
    20:'INFO',
    30:'WARNING',
    40:'ERROR',
    50:'CRITICAL'
}

__TASK_NAME = 'DEFAULT'

__CLIENT_INITED = False

def get_task_name():
    return __TASK_NAME

def init_mplog_client(task=None, host=ServerCfg.HOST, 
                port=ServerCfg.PORT, level=logging.INFO):
    root_logger = logging.getLogger()
    global __CLIENT_INITED
    global __TASK_NAME

    if __CLIENT_INITED == False:
        if task is not None:
            __TASK_NAME = task
        root_logger.setLevel(level)
        root_logger.addHandler(WebHandler(host, port))
        __CLIENT_INITED = True
    else:
        logging.warning('Repeated initialization of mplog client!')

class RecordInfo():

    def __init__(self, task='', message='', time='', file_name='', func_name='', level_no=-1, level_name='',
                    line_no=-1, module='', logger_name='', path_name='', process_id='', process_name='',
                    relative_msec=-1, thread_id=-1, thread_name=''):
        self.task = task
        self.time = time
        self.file_name = file_name
        self.func_name = func_name
        self.level_no = level_no
        self.level_name = level_name
        self.line_no = line_no
        self.module = module
        self.message = message
        self.logger_name = logger_name
        self.path_name = path_name
        self.process_id = process_id
        self.process_name = process_name
        self.relative_msec = relative_msec
        self.thread_id = thread_id
        self.thread_name = thread_name
    
    
    @classmethod
    def from_dict(cls, rec_dict):
        record_info = RecordInfo(**rec_dict)
        return record_info
    
    @classmethod
    def from_log_record(cls, log_record):
        r_info = RecordInfo()
        r_info.task = get_task_name()
        time_s = time_to_str(log_record.created)
        msec_s = MSEC_FORMATTER % (log_record.msecs)
        r_info.time = time_s + msec_s
        r_info.file_name = log_record.filename
        r_info.func_name = log_record.funcName
        r_info.level_no = log_record.levelno
        r_info.level_name = log_record.levelname
        r_info.line_no = log_record.lineno
        r_info.message = log_record.getMessage()
        r_info.module = log_record.module
        r_info.logger_name = log_record.name
        r_info.path_name = log_record.pathname
        r_info.process_id = log_record.process
        r_info.process_name = log_record.processName
        r_info.relative_msec = log_record.relativeCreated
        r_info.thread_id = log_record.thread
        r_info.thread_name = log_record.threadName
        return r_info

    def to_dict(self):
        return self.__dict__
    
    def to_tuple(self):
        """
        for efficient sql insertion
        """
        return self.task, self.time, self.file_name, self.func_name, \
                self.level_no, self.level_name, self.line_no, self.module, \
                self.message, self.logger_name, self.path_name, self.process_id,\
                self.process_name, self.relative_msec, self.thread_id, self.thread_name

def time_to_str(floating_time):
    """
    param: time: floating point number since the time epoch.
    """
    struct_time = time.localtime(floating_time)
    time_s = time.strftime(TIME_FORMATTER, struct_time)
    # msec_s = MSEC_FORMATTER%(time-int(time))
    # precise_time_s = time_s + msec_s
    return time_s


class WebHandler(logging.Handler):

    WEB_PATH='/records'
    DEFAULT_SCHEME='http'
    TIMEOUT = 2.0

    def __init__(self, host, port):
        super().__init__()
        self._host = host
        self._port = port


    def emit(self, record):
        scheme = self.DEFAULT_SCHEME
        netloc = '{:s}:{}'.format(self._host, self._port)
        path = self.WEB_PATH
        url = urllib.parse.urlunsplit((scheme, netloc, path, '', ''))
        # print('request: {:s}'.format(url))
        # myurl = "http://www.testmycode.com"
        # req = urllib.request.Request(myurl)
        # req.add_header('Content-Type', 'application/json; charset=utf-8')
        # jsondata = json.dumps(body)
        # jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
        # req.add_header('Content-Length', len(jsondataasbytes))
        # print (jsondataasbytes)
        # response = urllib.request.urlopen(req, jsondataasbytes) 
        record_info = RecordInfo.from_log_record(record)
        _info = record_info.to_dict()
        json_bytes = json.dumps(_info).encode('utf-8')
        # data = urllib.parse.urlencode(_info).encode('ascii')
        req = urllib.request.Request(url, data=json_bytes, method='POST')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Content-Length', len(json_bytes))
        try:
            resp = urllib.request.urlopen(req, timeout=self.TIMEOUT)
            if resp.status == 200:
                try:
                    raw_json = resp.read()
                    json_resp = json.loads(raw_json.decode('utf-8'))
                except json.JSONDecodeError:
                    print('ERROR! Cannot convert response to json.')
                    return 
                if json_resp['status'] != 'OK':
                    print('ERROR! Posting failure. Status:{:s}, info:{:s}'.format(json_resp['status'], json_resp['info']))
        except urllib.error.URLError:
            print('ERROR! Cannot connect to the mplog-server.')
        except Exception:
            print('Exception when post log record.')
        
        return 








