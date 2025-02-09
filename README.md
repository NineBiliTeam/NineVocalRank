# NineVocalRank


![GitHub License](https://img.shields.io/github/license/NineBiliTeam/NineBiliRank) 
![Python Version](https://badgen.net/pypi/python/black)



## 1. 简介

基于[NineBiliRank](https://github.com/NineBiliTeam/NineBiliRank)与`asyncio`的**开箱即用**的中文虚拟歌手数据平台

提供用于查询中文虚拟歌手曲目的API，以及计划任务

API文档：[NineBiliRank Basic API](https://apifox.com/apidoc/shared-a554e842-b1a6-4727-aa4e-66ed2454f95c) | [NineVocalRank Vocaloid API](https://apifox.com/apidoc/shared-1732993d-5ad1-4aee-ae17-aa68e388d101)

数据库支持，请参阅：[SQLAlchemy支持的方言](https://docs.sqlalchemy.org.cn/en/20/dialects/index.html)

P.S：**由于B站用户会用奇奇怪怪的emoji投稿，mysql用户一定要设置字符集`utf8mb4`一定要设置字符集`utf8mb4`一定要设置字符集`utf8mb4`**

公共搭建：[NineBiliDataBaseAPI](https://api.ninevocalrank.top/redoc)

## 2. 功能

1. [周刊中文虚拟歌手](https://evocalrank.com)分数计算
2. 曲目成就监测
3. 曲目查询

## 3. 使用
1. clone本仓库
2. 新建虚拟环境并`pip install -r requirements.txt`
3. `cd NineVocalRank`并修改`BasicConfig.yml`以及`config.dev.yml`，配置数据库
4. 从`data`文件夹内找到一个最近日期的txt文件（如`2025-02-06.txt`），这个文件包含`NineSpyder`获取的中V曲目BV号数据，将其的路径填写到`config.dev.yml`对应的配置项内
5. `python nbrank.py`


## 4. 收录规则

你可以选择使用`VocaloidChinaFilter`过滤器，他会过滤符合[周刊中文虚拟歌手](https://evocalrank.com)定义的视频

如果需要更严格的标准，请使用`NBVCDatabaseFilter`，这是NineVocaloidDataBase（平台建设中）的收录规则

你也可以实现自己的过滤器，达到特定收录

## 5. 定制

你可以根据[NineBiliRank](https://github.com/NineBiliTeam/NineBiliRank)二次开发NineVocalRank

## 6. 相关项目

1. `NineVocalRankData` 此项目的静态前端：2099 coming soon
2. `nonebot_plugin_ninevocalrank`：2099 coming soon
