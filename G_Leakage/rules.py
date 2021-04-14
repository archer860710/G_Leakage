"""
    G_Leakage
    Github代码泄露监测程序
    Github Code Leakage Detection

    Name      : mytoken.py
    Function  : 读取搜索规则
                Get rules from rules.cfg
    Author    : lvqing
    E-mail    : lvqing040756@sina.com
"""

import os
import json
from G_Leakage.logger import logger_info, logger_error

rules_path = './rules.cfg'
rules_dict = {}
rules_objects = []

class Rule(object):
    """
    规则类
    G_Leakage rule
    """
    def __init__(self, name, keyword, where, tag):
        self.name = name   # 规则名称
                           # rule name
        self.keyword = keyword   # 搜索关键字
                                 # search keyword
        self.where = where   # 搜索位置
                             # search place: file or path
        self.tag = tag   # 是否已执行过搜索的标志位
                         # if ever executed code search

def get_rules():
    """
    读取搜索规则
    Get rules from rules.cfg
    """
    try:
        if not os.path.exists(rules_path):
            print('Can\'t find file "{}"!'.format(rules_path))
            logger_error('Can\'t find file "{}"!'.format(rules_path))
            exit(1)
        else:
            for rule_name, rule_value in rules_dict.items():
                rule_keyword = rule_value['keyword']
                # 检查规则名称中是否包含有空格。
                # Check if there is a blank character in rule name.
                if ' ' in rule_name:
                    logger_error('There is a blank character in rule name!')
                    print('There is a blank character in rule name!')
                    exit(1)
                if rule_value['where'] == None:
                    rule_where = 'file'
                else:
                    rule_where = rule_value['where']
                r = Rule(rule_name, rule_keyword, rule_where, None)
                rules_objects.append(r)
            logger_info('Succeeded in getting rules.')
    except Exception as e:
        logger_error('Failed in getting rules: {}!'.format(e))
        print('Failed in getting rules!')
        exit(1)

try:
    with open(rules_path, mode='r', encoding='UTF-8') as file:
        rules_dict = json.loads(file.read())
        get_rules()
except:
    exit(1)
