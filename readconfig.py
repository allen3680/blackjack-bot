import configparser
import os
from mysql import *


def readMysqlConfig():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cf = configparser.ConfigParser()
    cf.read(root_dir + '/config.ini')

    return {
        "host": cf.get('database', 'host'),
        "port": cf.get('database', 'port'),
        "user": cf.get('database', 'user'),
        "password": cf.get('database', 'password'),
        "db": cf.get('database', 'db')
    }


def readBotConfig():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cf = configparser.ConfigParser()
    cf.read(root_dir + '/config.ini')

    return {
        "no": cf.get('bot', 'no')
    }


def readComputerConfig():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cf = configparser.ConfigParser()
    cf.read(root_dir + '/config.ini')

    return {
        "w_offset": cf.get('computer', 'w_offset'),
        "h_offset": cf.get('computer', 'h_offset')
    }