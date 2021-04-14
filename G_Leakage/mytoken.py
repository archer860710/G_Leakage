"""
    G_Leakage
    Github代码泄露监测程序
    Github Code Leakage Detection

    Name      : mytoken.py
    Function  : 读取Github Token
                Get token from mytoken.cfg
    Author    : lvqing
    E-mail    : lvqing040756@sina.com
"""

import os
import configparser
from G_Leakage.logger import logger_info, logger_error

token_path = './mytoken.cfg'
token = None

def get_token():
    """
    读取Github Token
    Get token from mytoken.cfg
    """
    if not os.path.exists(token_path):
        print('Can\'t find file "{}"!'.format(token_path))
        logger_error('Can\'t find file "{}"!'.format(token_path))
        exit(1)
    else:
        try:
            config = configparser.ConfigParser()
            config.read(token_path)
            value = config.get('token', 'token')
            logger_info('Succeeded in getting token.')
        except Exception as e:
            logger_error('Failed in getting token: {}!'.format(e))
            print('Failed in getting token!')
            exit(1)
        return value

try:
    token = get_token()
except:
    exit(1)