from datetime import datetime
from logging import info, error, basicConfig, INFO
from sqlite3 import Error
from os import listdir, path, getcwd, makedirs
from shutil import rmtree

from database.connection import logs_db, requests_db, questions_db

def clear_logs() -> bool | None:
    if len(listdir(logs_dir)) >= 5:
        rmtree(logs_dir)
        return True
    else:
        return None

logs_dir = path.join(getcwd(), 'logs')

def on_start() -> None:
    clear_logs()
    makedirs(logs_dir, exist_ok=True)
    basicConfig(
        level=INFO,
        filename=r'logs/{}.log'.format(str(datetime.now().replace(microsecond=0)).translate(str.maketrans({' ': '_', ':': '_'}))),
        encoding='utf-8',
        filemode='w'
    )
    info("Start")


def sql_start() -> None:
    try:
        logs_db()
    except Error as e:
        info('LOGGING DATABASE CONNECTION STATE: -ERROR-')
        error(e)
    try:
        requests_db()
    except Error as e:
        info('REQUEST DATABASE CONNECTION STATE: -ERROR-')
        error(e)
    try:
        questions_db()
    except Error as e:
        info('QUESTIONS DATABASE CONNECTION STATE: -ERROR-')
        error(e)