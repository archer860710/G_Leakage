"""
    G_Leakage
    Github代码泄露监测程序
    Github Code Leakage Detection

    Name      : mytoken.py
    Function  : 日志器
                Logger
    Author    : lvqing
    E-mail    : lvqing040756@sina.com
"""

import os
import datetime

log_path = './g_leakage.log'

def logger_info(content):
    """
    info级别的日志器
    Logger of info level
    """
    try:
        time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        log = '{0}  [INFO]{1}\n'.format(time, content)
        with open(log_path, mode='a') as file:
            file.write(log)
    except Exception as e:
        print('Failed in logger: {}!'.format(e))
        exit(1)

def logger_error(content):
    """
    error级别的日志器
    Logger of error level
    """
    try:
        time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        log = '{0}  [ERROR]{1}\n'.format(time, content)
        with open(log_path, mode='a') as file:
            file.write(log)
    except Exception as e:
        print('Failed in logger: {}!'.format(e))
        exit(1)

def logger_warning(content):
    """
    warning级别的日志器
    Logger of warning level
    """
    try:
        time = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        log = '{0}  [WARNING]{1}\n'.format(time, content)
        with open(log_path, mode='a') as file:
            file.write(log)
    except Exception as e:
        print('Failed in logger: {}!'.format(e))
        exit(1)

if __name__ == '__main__':
    pass
else:
    try:
        # 如果g_leakage.log不存在，那么自动创建这个文件。
        # Create the log file if it doesn't exist.
        if not os.path.exists(log_path):
            try:
                with open(log_path, mode='w') as file:
                    pass
            except Exception as e:
                print('Failed in generating log file "{}": {}!'.format(log_path, e))
                exit(1)
    except:
        exit(1)