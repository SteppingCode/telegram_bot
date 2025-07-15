from datetime import datetime
from logging import info, error, basicConfig, INFO
from sqlite3 import Error
from os import listdir, path, getcwd, makedirs
from shutil import rmtree

from database.connection import db_manager

def clear_logs() -> bool | None:
    if len(listdir(logs_dir)) >= 5:
        rmtree(logs_dir)
        return True
    else:
        return None

logs_dir = path.join(getcwd(), 'logs')

def on_start() -> bool:
    clear_logs()
    makedirs(logs_dir, exist_ok=True)
    basicConfig(
        level=INFO,
        filename=r'logs/{}.log'.format(str(datetime.now().replace(microsecond=0)).translate(str.maketrans({' ': '_', ':': '_'}))),
        encoding='utf-8',
        filemode='w'
    )
    info("Start")
    return True


def sql_start() -> bool:
    try:
        if db_manager.logs and db_manager.requests and db_manager.questions:
            info("CONNECTION TO DATABASES IS SUCCESSFUL")
            return True
        else:
            info("CONNECTION TO DATABASES IS NOT SUCCESSFUL")
            return False
    except Error as e:
        error(e)
        return False