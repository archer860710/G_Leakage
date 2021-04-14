"""
    G_Leakage
    Github代码泄露监测程序
    Github Code Leakage Detection

    Name      : mytoken.py
    Function  : 程序引擎
                Engine of G_Leakage
    Author    : lvqing
    E-mail    : lvqing040756@sina.com
"""

import os
import shutil
import platform
import datetime, time
import github
import pandas as pd
from G_Leakage.mytoken import token
from G_Leakage.rules import rules_objects
from G_Leakage.white_list import white_repos, white_urls
from G_Leakage.logger import logger_info, logger_error, logger_warning

tmp_directory = './temp/'
tmp_path = None
tmp_cmp_path = None
bak_directory = './backups/'
bak_path = None
ret_directory = './results/'
ret_path = None
col = ['repo', 'name', 'url', 'sha']

def code_search(rule):
    """
    执行搜索
    Execute code search
    """
    # 如果/temp/不存在，那么自动创建这个文件夹。
    # Generate tmp directory if it doesn't exist.
    if not os.path.exists(tmp_directory):
        try:
            os.mkdir(tmp_directory)
        except Exception as e:
            logger_error('Failed in generating directory "{}": {}!'.format(tmp_directory, e))
            print('Failed in generating directory "{}": {}!'.format(tmp_directory, e))
            exit(1)
    # 判断是否是首次执行对本次关键字的搜索。
    # Check if ever executed code search
    if os.path.exists(tmp_cmp_path):
        rule.tag = True
    else:
        rule.tag = False
    g = github.Github(token)
    try:
        query = '{0} in:{1}'.format(rule.keyword, rule.where)
        ret = g.search_code(query, sort='indexed', order='desc')   # 执行搜索，返回结果的类型为Github.PaginatedList。
                                                                   # Execute code search of the rule, and return type is Github.PaginatedList.
        logger_info('Succeeded in code search of "{}".'.format(rule.name))
    except Exception as e:
        logger_error('Failed in code search of "{}": {}!'.format(rule.name, e))
        print('Failed in code search of "{}"!'.format(rule.name))
        exit(1)
    into_tmp(rule.name, ret)   # 将本次搜索结果保存到/temp/中。
                               # Save the result into tmp_directory.
    into_bak(rule)   # 将本次搜索结果保存到/backups/中。
                     # Save the result into bak_directory.

def into_tmp(rn, ret):
    """
    将搜索结果保存到/temp/中
    Save the result into tmp_directory
    """
    df_ret = pd.DataFrame(columns=col)
    try:
        for cf in ret:
            l = []
            l.append(str(cf.repository).replace('Repository(full_name="', '').replace('")', ''))
            l.append(str(cf.name))
            l.append(str(cf.html_url))
            l.append(str(cf.sha))
            df = pd.DataFrame([l], columns=col)
            df_ret = df_ret.append(df, ignore_index=True)
        with open(tmp_path, 'w') as csvwriter:
            df_ret.to_csv(csvwriter, index=False)
        logger_info('Succeeded in saving the result of {}.'.format(rn))
    except Exception as e:
        logger_error('Failed in saving the result of {0}: {1}!'.format(rn, e))
        print('Failed in saving the result of {}!'.format(rn))
        exit(1)

def compare(rule):
    """
    将本次搜索结果和上次结果进行比较
    Execute compare
    """
    # 如果/results/不存在，那么自动创建这个文件夹。
    # Generate ret directory if it doesn't exist.
    if not os.path.exists(ret_directory):
        try:
            os.mkdir(ret_directory)
        except Exception as e:
            logger_error('Failed in generating directory "{}": {}!'.format(ret_directory, e))
            print('Failed in generating directory "{}": {}!'.format(ret_directory, e))
            exit(1)
    # 不是首次进行比较的情况
    # Not first time to do the compare
    if rule.tag == True:
        try:
            if platform.system() == 'Windows':
                df_tmp = pd.read_csv(tmp_path, encoding='ansi').dropna()
                df_tmp_cmp = pd.read_csv(tmp_cmp_path, encoding='ansi').dropna()
            elif platform.system() == 'Linux':
                df_tmp = pd.read_csv(tmp_path).dropna()
                df_tmp_cmp = pd.read_csv(tmp_cmp_path).dropna()
            df_ret = pd.DataFrame(columns=col)
            for i in range(len(df_tmp)):
                if df_tmp.loc[i, 'sha'] not in list(df_tmp_cmp['sha']):   # 和上次结果进行比较，如果'sha'字段存在新增内容，那么可能存在着新增Github文件。
                                                                          # Compare df_tmp with df_tmp_cmp,
                                                                          # if there exists new 'sha' content,
                                                                          # that means there exists new Github content.
                    # 白名单过滤
                    # Compare df_tmp with white list
                    if df_tmp.loc[i, 'repo'] in list(white_repos):
                        pass
                    else:
                        if df_tmp.loc[i, 'url'] in list(white_urls):
                            pass
                        else:
                            df_ret = df_ret.append(df_tmp.loc[[i]])
            # 经过白名单过滤后，依然存在新增文件的，保存到/results/中。
            # Save into ret_path if there exists new Github content.
            if len(df_ret) > 0:
                with open(ret_path, 'w') as writer:
                    df_ret.to_csv(writer, index=False)
                logger_warning('There exists new Github content of "{}", '
                               'see more details in directory {}!'.format(rule.name, ret_directory))
                print('There exists new Github content of "{}", '
                      'see more details in directory {}!'.format(rule.name, ret_directory))
            else:
                logger_info('"{}" is OK.'.format(rule.name))
                print('"{}" is OK.'.format(rule.name))
            logger_info('Succeeded in executing compare of "{}".'.format(rule.name))
        except Exception as e:
            logger_error('Failed in executing compare of "{}": {}!'.format(rule.name, e))
            print('Failed in executing compare of "{}"!'.format(rule.name))
            exit(1)
    # 首次执行比较的情况
    # First time to do the compare
    else:
        if platform.system() == 'Windows':
            shutil.copy(tmp_path, ret_path)
        elif platform.system() == 'Linux':
            os.system('/bin/cp -f {0} {1}'.format(tmp_path, ret_path))
        logger_warning('It\'s your first time to search "{}", '
                       'see more details in directory {}.'.format(rule.name, ret_directory))
        print('It\'s your first time to search "{}", '
              'see more details in directory {}.'.format(rule.name, ret_directory))

def into_tmp_cmp(rule):
    """
    将本次搜索结果保存到tmp_cmp_path
    Save the result into tmp_cmp_path
    """
    try:
        if platform.system() == 'Windows':
            shutil.copy(tmp_path, tmp_cmp_path)
        elif platform.system() == 'Linux':
            os.system('/bin/cp -f {0} {1}'.format(tmp_path, tmp_cmp_path))
        logger_info('Succeeded in generating {}_cmp.csv.'.format(rule.name))
    except Exception as e:
        logger_error('Failed in generating {0}_cmp.csv: {1}!'.format(rule.name, e))
        print('Failed in generating {0}_cmp.csv!'.format(rule.name))
        exit(1)

def into_bak(rule):
    """
    将本次搜索结果保存到/backups/中
    Save the result into bak_path
    """
    # 如果/backups/不存在，那么自动创建这个文件夹。
    # Generate bak directory if it doesn't exist.
    if not os.path.exists(bak_directory):
        try:
            os.mkdir(bak_directory)
        except Exception as e:
            logger_error('Failed in generating directory "{}": {}!'.format(bak_directory, e))
            print('Failed in generating directory "{}": {}!'.format(bak_directory, e))
            exit(1)
    try:
        if platform.system() == 'Windows':
            shutil.copy(tmp_path, bak_path)
        elif platform.system() == 'Linux':
            os.system('/bin/cp -f {0} {1}'.format(tmp_path, bak_path))
        logger_info('Succeeded in backuping the result of "{}".'.format(rule.name))
    except Exception as e:
        logger_error('Failed in backuping the result of "{0}": {1}!'.format(rule.name, e))
        print('Failed in backuping the result of "{0}"!'.format(rule.name))
        exit(1)

def clear_bak():
    """
    清空/backups/
    Clear all files in bak_directory
    """
    try:
        if not os.path.exists(bak_directory):
            logger_error('Directory "{}" does not exist!'.format(bak_directory))
            print('Directory "{}" does not exist!'.format(bak_directory))
            exit(1)
        else:
            pass
    except Exception as e:
        logger_error('Failed in clearing all files in directory "{}": {}'.format(bak_directory, e))
        print('Failed in clearing all files in directory "{}": {}'.format(bak_directory, e))
        exit(1)

def verify_token():
    """
    检查Github Token
    Verify token
    """
    try:
        g = github.Github(token)
        value = g.rate_limiting[0]
        return True, value
    except:
        return False, None

def g_leakage():
    """
    主程序
    Main program of G_Leakage
    """
    try:
        logger_info('G_Leakage is running...')
        for rule in rules_objects:
            day = datetime.date.today().strftime('%Y-%m-%d')
            global tmp_path, tmp_cmp_path, ret_path, bak_path
            tmp_path = '{0}{1}.csv'.format(tmp_directory, rule.name)
            tmp_cmp_path = '{0}{1}_cmp.csv'.format(tmp_directory, rule.name)
            ret_path = '{0}{1}_{2}.csv'.format(ret_directory, rule.name, day)
            bak_path = '{0}{1}_{2}.csv'.format(bak_directory, rule.name, day)
            code_search(rule)
            compare(rule)
            into_tmp_cmp(rule)
            time.sleep(60)   # 考虑到Github API限制，在每执行一次搜索后，等待60秒。
                             # Considering the rate-limit of Github API, wait for 60s between each two code searches.
        logger_info('G_Leakage is completed.')
    except:
        logger_error('G_Leakage is failed!')
        print('G_Leakage is failed!')
        exit(1)