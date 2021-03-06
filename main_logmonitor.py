import configparser
import os
import re
import subprocess
import sys
import time
from tkinter import *

import pymysql

from monitor import logMonitor
from utils import execSQL, getConfig


def main():
    # global db
    db = getConfig()
    data = execSQL(db, "SELECT VERSION()")
    print(time.strftime('[%H:%M:%S]') + "The version of database: %s " % data)
    time.sleep(1)
    data = execSQL(db, "show variables like '%general_log%';")[1]
    print(time.strftime('[%H:%M:%S]') + 'The status of log:' + data)
    if data == "OFF":
        try:
            print(time.strftime('[%H:%M:%S]') + 'Starting log mode...')
            time.sleep(1)
            try:
                # logPath = r'D:\\github\\MySQL_Monitor\\'
                logPath = os.getcwd()
                #print(logPath)
                global log
                logName = str(time.strftime('%Y_%m_%d')) + "_log.txt"
                log = logPath + "/" + logName
                log = log.replace("\\", "/")  # for windows not support to use \ in log file path
                data = execSQL(db, "set global general_log_file='" + log + "';")
            except:
                pass

            data = execSQL(db, "set global general_log=on;")
            data = execSQL(db, "show variables like '%general_log%';")[1]
            if data == "ON":
                print(time.strftime('[%H:%M:%S]') + 'Log is started.')
                print(time.strftime('[%H:%M:%S]') + 'Log monitor running...')
                log = str(execSQL(db, "show variables like 'general_log_file';")[-1])
                logMonitor(log, db)
        except:
            print(time.strftime('[%H:%M:%S]') + 'Log starting failed.')
            exit()
    else:
        print(time.strftime('[%H:%M:%S]') + 'Log monitor running...')
    log = str(execSQL(db, "show variables like 'general_log_file';")[-1])
    db.close()
    logMonitor(log, db)


if __name__ == '__main__':
    main()
