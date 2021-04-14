"""
    G_Leakage
    Github代码泄露监测程序
    Github Code Leakage Detection

    Name      : mytoken.py
    Function  : 读取白名单
                Get white-list from white_list.csv
    Author    : lvqing
    E-mail    : lvqing040756@sina.com
"""

import os
import platform
import pandas as pd
from G_Leakage.logger import logger_info, logger_error

white_list_path = './white_list.csv'
df_white_list = None
white_repos = []
white_urls = []

def get_white_list():
    """
    读取白名单
    Get repos and urls of white list
    """
    try:
        global df_white_list
        if platform.system() == 'Windows':
            df_white_list = pd.read_csv(white_list_path, encoding='ansi')
        elif platform.system() == 'Linux':
            df_white_list = pd.read_csv(white_list_path, encoding='gbk')
        logger_info('Succeeded in getting white_list.')
        return df_white_list['repo'], df_white_list['url']
    except Exception as e:
        logger_error('Failed in getting white_list: {}'.format(e))
        print('Failed in getting white_list: {}'.format(e))
        exit(1)

if __name__ == '__main__':
    pass
else:
    try:
        # 如果不存在white_list.csv，那么自动创建这个文件。
        # Create the white-list file if it doesn't exist.
        if not os.path.exists(white_list_path):
            try:
                df_white_list = pd.DataFrame(columns=['rule name', 'repo', 'url'])
                with open(white_list_path, mode='w') as csvfile:
                    df_white_list.to_csv(csvfile, index=False)
                logger_info('Succeeded in generating white-list file.')
            except Exception as e:
                logger_error('Failed in generating white-list file: {}!'.format(e))
                print('Failed in generating white-list file: {}!'.format(e))
                exit(1)
        white_repos = get_white_list()[0]   # 读取repos
                                            # get repos of white list
        white_urls = get_white_list()[1]   # 读取urls
                                           # get urls of white list
    except:
        exit(1)