
import os

import flask

from . import dbm
from ..client import RecordInfo

__cur_dir = os.path.dirname(os.path.abspath(__file__))
__static_dir = os.path.join(__cur_dir, 'static')

log_server = flask.Flask('mplog-server', static_folder=__static_dir)

def teardown_close_db(exception):
    db = getattr(flask.g, 'db', None)
    if db is not None:
        dbm.close_db(db)
        delattr(flask.g, 'db')

log_server.teardown_request(teardown_close_db)


def gen_json_response(status='OK', info='', data=None):
    resp = {'status':status,
            'info':info,
            'data':data}
    return flask.jsonify(resp)


@log_server.route('/')
def root():
    return flask.redirect('/static/panel.html')


@log_server.route('/records', methods=['GET', 'POST'])
def records():
    if flask.request.method=='POST':
        r_info = flask.request.get_json()
        try:
            record_dict = dict(r_info)
        except:
            return gen_json_response('ERROR', 'cannot convert posted data to dict.')
            
        db = dbm.get_db()
        dbm.insert_record(db, RecordInfo.from_dict(record_dict))
        # print('task:{},time:{},message:{}'.format(record_dict['task'],
        #                                           record_dict['time'],
        #                                           record_dict['message']))
        return gen_json_response()

    elif flask.request.method=='GET':
        task = flask.request.args.get('task', '')
        if task == '':
            return gen_json_response('ERROR', 'Task name empty.')
        since = flask.request.args.get('since', None)
        until = flask.request.args.get('until', None)
        level_no = flask.request.args.get('level_no', 0)
        offset = flask.request.args.get('offset', 0)
        db = dbm.get_db()
        records = dbm.select_records(db, task, since, until, level_no, offset)
        data = {
            'records': records,
            'offset': offset,
            'since':since,
            'until':until,
        }
        return gen_json_response(data=data)



