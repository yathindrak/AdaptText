import logging
import json_log_formatter


class Logger:
    def __init__(self):
        formatter = json_log_formatter.JSONFormatter()
        json_handler = logging.FileHandler(filename='/var/log/adapttext.json')
        json_handler.setFormatter(formatter)
        self.logger = logging.getLogger('adapttext')
        self.logger.addHandler(json_handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message):
        self.logger.info(message,
                         extra={
                             'logger.name': 'adapttext',
                         })
