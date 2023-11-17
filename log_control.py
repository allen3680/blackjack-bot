import time
import logging
import os
from logging import handlers
import sys


def _logging(**kwargs):
    level = kwargs.pop('level', None)
    filename = kwargs.pop('filename', None)
    datefmt = kwargs.pop('datefmt', None)
    format = kwargs.pop('format', None)
    if level is None:
        level = logging.INFO
    if filename is None:
        filename = 'default.log'
    if datefmt is None:
        datefmt = '%Y-%m-%d %H:%M:%S'
    if format is None:
        # format = '%(asctime)s [%(module)s] %(levelname)s [%(lineno)d] %(message)s'
        format = "%(asctime)s [%(levelname)s] %(message)s"
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    log = logging.getLogger(filename)

    format_str = logging.Formatter(format, datefmt)
    # backupCount 儲存日誌的數量，過期自動刪除
    # when 按什麼日期格式切分(這裡方便測試使用的秒)
    th = handlers.TimedRotatingFileHandler(
        filename=filename, when='midnight', backupCount=0, encoding='utf-8')
    th.setFormatter(format_str)
    th.setLevel(logging.INFO)
    th.suffix = "%Y-%m-%d.log"
    log.addHandler(th)
    log.setLevel(level)
    return log


os.makedirs("./logs", exist_ok=True)
logger = _logging(filename='./logs/default.log')


def log_info(msg):
    logger.info(msg)


def log_warning(msg):
    logger.warning(msg)
