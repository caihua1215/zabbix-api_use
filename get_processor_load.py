#!/usr/bin/env python
#coding:utf-8
#from sys import argv
#Group_name_Q="web_beike"
from pyzabbix import ZabbixAPI

#获取hostid
def group_id(groupname):
  Group_id = zapi.hostgroup.get(filter={'name' : groupname})[0]['groupid']
  return Group_id
#获取每个组的成员，根据组id赋值给一个字典
def group_host(groupid):
    host_dict={}
    #group_dict={}
    host = zapi.host.get(groupids=groupid)
    for i in host:
        host_dict[i['name']]=i['hostid']
    #group_dict[groupid]=host_dict
    return host_dict
def item_id(hostsname,itemname):
    Item_id = zapi.item.get(filter={'host':hostsname,'name': itemname})[0]['itemid']
    return Item_id
def trend(ITEMID,TIME_FROM,TIME_STILL):
    value_avg=[]
    for Trend in zapi.trend.get(itemids=ITEMID,time_from=TIME_FROM,time_still=TIME_STILL):
        value_avg.append(Trend['value_avg'])
    return value_avg
if __name__ == '__main__':
    Gid=group_id('api-bus_appstore')
    print Gid
    dict=group_host(group_id('lb'))
    print dict
    for i in dict.keys():
        print i,dict[i]
        Iid=item_id(i,'Processor load (1 min average)')
        #zapi.trend.get(itemids=71045,time_from=1490115600,time_still=1490155200)
        #print zapi.trend.get(itemids=Iid,time_from=1490115600,time_still=1490155200)
        qh=trend(Iid,1490115600,1490155200)
        print qh
        '''value_avg=[]
        for trend in  zapi.trend.get(itemids=Iid,time_from=1490115600,time_still=1490155200)
            value_avg.append(trend['value_avg'])
        print "value_avg_list: ",value_avg
'''
