import json, logging


def get_app_log(record):
    if record.levelname == "ERROR":
        res = json.loads(record.message)
        json_obj = {'log': {
            'level': record.levelname,
            'type': 'app',
            'timestamp': record.asctime,
            #'filename': record.filename,
            #'pathname': record.pathname,
            #'line': record.lineno,
            #'threadId': record.thread,
            'path': res['path'],
            'status_code': res['status_code'],
            'error_msg': res['error_msg']
        }}
    else:
        json_obj = {'log': {
            'level': record.levelname,
            'type': 'app',
            'timestamp': record.asctime,
            #'filename': record.filename,
            #'pathname': record.pathname,
            #'line': record.lineno,
            #'threadId': record.thread,
            'message': record.message
            }}

    return json_obj


def get_access_log(record):
    json_obj = {'log': {
        'level': record.levelname,
        'type': 'access',
        'timestamp': record.asctime,
        'message': record.message},
        'req': record.extra_info['req'],
        'res': record.extra_info['res']}

    return json_obj


class CustomFormatter(logging.Formatter):

    def __init__(self, formatter):
        logging.Formatter.__init__(self, formatter)
    
    def format(self, record):
        logging.Formatter.format(self, record)
        if not hasattr(record, 'extra_info'):
            return json.dumps(get_app_log(record), indent=2)
        else:
            return json.dumps(get_access_log(record), indent=2)