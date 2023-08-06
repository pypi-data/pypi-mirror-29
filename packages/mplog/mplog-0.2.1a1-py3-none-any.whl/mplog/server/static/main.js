

const g_record_map={
    rowid:['rowid', 0, 'The row id of this log record in the database.'],
    task:['task', 1, 'The task name of this log record.'],
    datetime:['datetime', 2, 'The datatime when the record is emitted.'],
    file_name: ['file_name', 3, 'The name of the file in which the record is emitted.'],
    func_name: ['func_name', 4, 'The name of the function in which the record is emitted.'],
    level_no: ['level_no', 5, 'The logging level number of this record.'],
    level_name: ['level_name', 6, 'The logging level name of this record.'],
    line_no: ['line_no', 7 , 'The line number where this record is emitted.'],
    module: ['module', 8, 'The module name in which this record is emitted.'],
    message: ['message', 9, 'The message included in this record.'],
    logger_name: ['logger_name', 10, 'The name of the logger that handle this record.'],
    path_name: ['path_name', 11, 'The path name of the file in which this record is emitted.'],
    process_id: ['process_id', 12, 'The id of the process that emits this record.'],
    process_name: ['process_name', 13, 'The name of the process that emits this record.'],
    relative_msec: ['relative_msec', 14, 'Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded.'],
    thread_id: ['thread_id', 15, 'The id of the thread that emits this record.'],
    thread_name: ['thread_name', 16, 'The name of the thread that emits this record.']
};

const g_record_index = new Array(17);
for(let prop in g_record_map){
    g_record_index[g_record_map[prop][1]]=prop;
}



$(function(){
    $.getJSON('/records',{task:'DEFAULT', since:'2018-03-13 19:36:43.847'}, function(resp){
        $('#records1').text(resp.data.records)
    });
    $.getJSON('/records',{task:'DEFAULT', until:'2018-03-13 19:36:43.847'}, function(resp){
        $('#records2').text(resp.data.records)
    });
    $.getJSON('/records',{task:'DEFAULT', since:'2018-03-13 19:36:43.847', until:'2018-03-13 19:40:43.847',}, function(resp){
        $('#records3').text(resp.data.records)
    })
});