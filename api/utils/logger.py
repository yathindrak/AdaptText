import logging
import json_log_formatter


class Logger:
    """Logging Module"""
    def __init__(self):
        formatter = json_log_formatter.JSONFormatter()
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] - %(message)s')
        json_handler = logging.FileHandler(filename='/var/log/adapttext.json')
        json_handler.setFormatter(formatter)
        self.logger = logging.getLogger('adapttext')
        self.logger.addHandler(json_handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message):
        """
        Log info level logs
        """
        self.logger.info(message,
                         extra={
                             'logger.name': 'adapttext',
                         })
