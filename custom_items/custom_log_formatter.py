import logging
import pytz
from logging.handlers import RotatingFileHandler
import datetime


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.datetime.utcfromtimestamp(record.created)
        dt = pytz.utc.localize(dt).astimezone(pytz.timezone('Europe/Moscow'))  # устанавливаем нужную временную зону
        return dt.strftime(datefmt)
