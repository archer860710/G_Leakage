# G_Leakage（Github代码泄露监测程序）



### 一、简介

G_Leakage是一款使用Python开发的Github代码泄露监测程序，它可以发现Github上存在的可疑泄露代码。

G_Leakage支持在Linux、Windows上使用。



### 二、原理

G_Leakage使用增量比较的方法。

假如你公司的应用系统代码中，有一个叫做"package xxx.com.cn"的关键字。那么，G_Leakage会自动计算出本次以"package xxx.com.cn"为关键字的搜索结果，和上一次以"package xxx.com.cn"为关键字的搜索结果之间的增量。

这里的“增量”包括两种情况：**1、新增的Github文件；2、上一次搜索时就存在的Github文件，但本次搜索时，其文件内容发生了改变。**

增量不意味着一定存在代码泄露，但它意味着一种可能性。

#### 1、PyGithub

PyGithub是一个使用Github API v3的Python第三方库。使用PyGithub，你可以通过Github API 来管理你的Github资源，也可以执行各种动作（比如代码搜索等）。

G_Leakage就使用了PyGithub，并以此调用Github API。

[PyGithub]: https://pygithub.readthedocs.io/en/latest/index.html

#### 2、Github API

你可以通过Github API 来管理你的Github资源，也可以执行各种动作（比如代码搜索等）。

**通过Github API执行的代码搜索，最多只能返回1000条结果。因此，G_Leakage仅适用于该关键字检索结果少于1000条的情况。**

[Github API]: https://docs.github.com/en/rest



### 三、安装

```bash
$ git clone 
$ cd G_Leakage
$ pip install -r requirements.txt
```



### 四、使用前

#### 1、Github Token

在使用G_Leakage前，确保您已经申请了一个Github Token。Github Token，相比起传统密码具有更高的安全性，使用Github Token来访问Github API，也会有更少的限制条件。

> 如何申请Github Token？

[点这里，申请Github Token]: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

> 配置mytoken.cfg

```
[token]
token = xxxx   # 将您的Github Token替换掉这里的xxxx即可。
```

#### 2、rules.cfg

rules.cfg配置了搜索规则。G_Leakage程序的运行，必须依赖于正确、合理的规则配置。

| 字段名    | 含义       | 说明                                                         |
| --------- | ---------- | ------------------------------------------------------------ |
| rule_name | 规则名称   | rule_name用于区分和标识不同的搜索规则。在执行搜索过程中，不会产生任何作用。**注：rule_name可以包含中文、英文，但不能包含空格等空字符。** |
| keyword   | 搜索关键字 | 关键字可以包含中文、英文、空格等，**建议使用双引号将关键字包括起来**，这样表示精确搜索。 |
| where     | 搜索位置   | **file：在文件内容中搜索关键字；**path：在文件路径中搜索关键字；file or path：在文件内容和文件路径中搜索关键字；默认为“file”。 |

> 配置rules.cfg

```
{
    # 规则名称test1。
    "test1": {
        "keyword": "package xxx.com.cn",   # 搜索关键字"package xxx.com.cn"
        "where": "file"   # 表示在文件内容中搜索关键字。
    },
    "test2": {
        "keyword": "package xxx.com",
        "where": "path"
    },
    "test3": {
        "keyword": "xxx corp",
        "where": "file,path"
    }
}
```



### 五、使用方法

#### 1、测试Github Token有效性

```bash
$ python g_leakage.py verify-token
```

#### 2、运行G_Leakage程序

```bash
$ python g_leakage.py start
```

如果存在增量内容的，会将结果以”规则名称+日期.csv"方式，保存到/results/目录下。

全量搜索结果，会备份到/backups/目录下。

程序详细日志，会写入到g_leakage.log中。

#### 3、白名单功能

G_Leakage还提供了白名单功能。白名单有两个过滤要素：repo名称和url，只要匹配其中任意一个，就不会再计入增量中。

| 字段名    | 含义     | 说明                                                         |
| --------- | -------- | ------------------------------------------------------------ |
| rule name | 规则名称 | rule name用于区分和标识不同的白名单规则。在过滤中，不会产生任何作用。 |
| repo      | repo名称 | 如设置了repo，则该repo下的所有文件都不会再计入增量中。       |
| url       | url      | 如设置了url，则该文件都不会再计入增量中。                    |

> 配置白名单

![image-20210414162513245](C:\Users\HUAWEI\AppData\Roaming\Typora\typora-user-images\image-20210414162513245.png)

```bash
# 打印出当前所有的白名单规则
$ python g_leakage.py show-white-list
```