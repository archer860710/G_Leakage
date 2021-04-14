"""
    G_Leakage
    Github代码泄露监测程序
    Github Code Leakage Detection

    Name      : g_leakage.py
    Function  : G_Leakage主程序
                Main program of G_Leakage
    Author    : lvqing
    E-mail    : lvqing040756@sina.com
"""

import sys
from G_Leakage.core import clear_bak, verify_token, g_leakage
from G_Leakage.white_list import df_white_list
from G_Leakage.logger import logger_error

if __name__ == '__main__':
    try:
        if len(sys.argv) == 1:
            print('Usage Error: There is no arguments!')
            logger_error('Usage Error: There is no arguments!')
            exit(1)
        elif len(sys.argv) == 2:
            # 输入“python g_leakage.py start”时……
            # When type "python g_leakage.py start"……
            if sys.argv[1] == 'start':
                print('G_Leakage is running...')
                g_leakage()
                print('G_Leakage is completed.')
                exit(0)
            elif sys.argv[1] == 'clear-bak':
                print('Starting to clear all backup files……')
                clear_bak()
                print('Succeeded in clearing all backup files.')
            # 输入“python g_leakage.py verify-token”时……
            # When type "python g_leakage.py verify-token"……
            elif sys.argv[1] == 'verify-token':
                print('Token test is running...')
                ret = verify_token()
                if ret[0]:
                    print('Succeeded in token test.')
                else:
                    print('Token test is failed.')
            # 输入“python g_leakage.py show-white-list”时……
            # When type "python g_leakage.py show-white-list"……
            elif sys.argv[1] == 'show-white-list':
                print(df_white_list)
            else:
                print('Usage Error: Wrong usage!')
                logger_error('Usage Error: Wrong usage!')
                exit(1)
        elif len(sys.argv) == 4:
            if sys.argv[1] == 'add-white-list':
                if sys.argv[2] == '-r' or sys.argv[2] == '--repo':
                    pass
                if sys.argv[2] == '-f' or sys.argv[2] == '--file':
                    pass
        else:
            print('Usage Error: Wrong usage!')
            logger_error('Usage Error: Wrong usage!')
            exit(1)
    except:
        exit(1)
