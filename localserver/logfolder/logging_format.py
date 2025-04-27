import logging
import json
from typing import override
import datetime as dt

LOG_RECORD_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


# create a formatter to convert output to json lines and set timezone to utc
class JSONFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        """format the record to json

        Args:
            record (logging.LogRecord):

        Returns:
            str: return json formatted record
        """
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        """ include message and timestmap for all logs

        Args:
            record (logging.LogRecord): _description_

        Returns:
            _type_: _description_
        """
        always_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc
            ).isoformat(),
        }
        # get error details for error log
        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)
        
        # include stack if available
        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_ATTRS:
                message[key] = val

        return message


class NonErrorFilter(logging.Filter):
    @override
    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        """Filter the error to only send error to standard error

        Args:
            record (logging.LogRecord): takes in logging record

        Returns:
            bool | logging.LogRecord: errors with numeric level of logging.info (20) and below is returned
        """
        return record.levelno <= logging.INFO
