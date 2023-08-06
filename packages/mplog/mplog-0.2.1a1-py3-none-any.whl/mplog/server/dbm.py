
import os
import sqlite3

import flask

from ..client import RecordInfo
from ..config import DatabaseCfg
from . import _sql_scripts 


def get_db():
    db = getattr(flask.g, 'db', None)
    if db is None:
        db_path = os.path.join(DatabaseCfg.ROOT_DIR, DatabaseCfg.DATABASE_NAME)
        if not os.path.isfile(db_path):
            __init_db()
        db = flask.g.db = sqlite3.connect(db_path)
    
    return db


def __init_db():
    db_path = os.path.join(DatabaseCfg.ROOT_DIR, DatabaseCfg.DATABASE_NAME)
    db = sqlite3.connect(db_path)
    db.execute(_sql_scripts.create_tab)
    db.execute(_sql_scripts.create_index)
    db.close()
    return


def close_db(db):
    db.close()
    return


def insert_record(db, record_info):
    assert isinstance(record_info, RecordInfo)
    db.execute(_sql_scripts.insert_record, record_info.to_tuple())
    db.commit()
    return 


def select_records(db, task, since=None, until=None, level_no=0 ,offset=0):
    cur = db.cursor()
    if since is None and until is None:
        cur.execute(_sql_scripts.select_records, (task, level_no, DatabaseCfg.MAX_FETCH, offset))
    elif since is not None and until is None:
        cur.execute(_sql_scripts.select_records_since, (task, level_no, since, DatabaseCfg.MAX_FETCH, offset))
    elif since is None and until is not None:
        cur.execute(_sql_scripts.select_records_until, (task, level_no, until, DatabaseCfg.MAX_FETCH, offset))
    else:
        cur.execute(_sql_scripts.select_records_since_until, (task, level_no, since, until, DatabaseCfg.MAX_FETCH, offset))
    res = cur.fetchall()
    cur.close()
    return res


