import logging, json
from datetime import datetime
from tzlocal import get_localzone

TRANSLATION_TABLE = {
    'threadName': 'thread',
    'levelname': 'severity',
    'process': 'pid',
    'module': 'module',
    'pathname': 'source_file',
}


class JSONFormatter(logging.Formatter):
    timezone = get_localzone()

    def format(self, record):
        return self.to_json(record)

    def to_json(self, record):
        log_message = {'description': record.getMessage(),
                       'log_type': 'application_log'}
        for key, item in record.__dict__.items():
            if key in TRANSLATION_TABLE:
                log_message[TRANSLATION_TABLE[key]] = item
        if record.exc_info:
            log_message['stacktrace'] = self.formatException(record.exc_info)
        log_message['@timestamp'] = self._get_localized_date().isoformat()
        return json.dumps(log_message)

    def _get_localized_date(self):
        return self.timezone.localize(datetime.now())
