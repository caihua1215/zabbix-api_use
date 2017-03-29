#!/usr/bin/env python
#coding:utf-8
#create_time: 2017/3/29
#author:sailq
from pyzabbix import ZabbixAPI
zapi = ZabbixAPI("*")
zapi.login("*")

import MySQLdb
#根据group_name创建分组
def create_new_group(group_name):
    new=zapi.hostgroup.create(name=group_name)
    print new
    return new
#建立一个连接
conn=MySQLdb.connect(host='*',user='*',passwd='*',db='*',port=3306)
#建立一个游标
cur =conn.cursor()

cur.execute('select * from Grains_grains limit 1')
group_name = cur.fetchall()
print group_name
for i in  group_name:
    try:
      create_new_group(i[1]
    except Exception as e:
      print e
      continue
