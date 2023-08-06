

create_tab = \
"""
    CREATE TABLE IF NOT EXISTS records (
        task TEXT NOT NULL,
        datetime TEXT,
        file_name TEXT,
        func_name TEXT,
        level_no INT,
        level_name TEXT,
        line_no INT,
        module TEXT,
        message TEXT,
        logger_name TEXT,
        path_name TEXT,
        process_id INT,
        process_name TEXT,
        relative_msec INT,
        thread_id INT,
        thread_name TEXT);
"""


create_index = \
"""
    CREATE INDEX IF NOT EXISTS datetime_index ON records (datetime);
"""


insert_record = \
"""
    INSERT INTO records (task, datetime, file_name, func_name,
                         level_no, level_name, line_no, module,
                         message, logger_name, path_name, process_id,
                         process_name, relative_msec, thread_id, thread_name)
                VALUES (?,?,?,?,
                        ?,?,?,?,
                        ?,?,?,?,
                        ?,?,?,?);
"""


select_records = \
"""
    SELECT rowid, * FROM records WHERE task=? AND level_no >= ? 
                ORDER BY datetime DESC, rowid DESC LIMIT ? OFFSET ?;
"""

select_records_since = \
"""
    SELECT rowid, * FROM records WHERE task=? AND level_no >= ? AND datetime >= ? 
                ORDER BY datetime DESC, rowid DESC LIMIT ? OFFSET ?;
"""

select_records_until = \
"""
    SELECT rowid, * FROM records WHERE task=? AND level_no >= ? AND datetime <= ? 
                ORDER BY datetime DESC, rowid DESC LIMIT ? OFFSET ?;
"""

select_records_since_until = \
"""
    SELECT rowid, * FROM records WHERE task=? AND level_no >= ? AND datetime >= ? AND datetime <= ?
                ORDER BY datetime DESC, rowid DESC LIMIT ? OFFSET ?;
"""





