#!/usr/bin/env python
#coding:utf-8
#from sys import argv
#Group_name_Q="web_beike"
import time
import commands
from pyzabbix import ZabbixAPI
zapi = ZabbixAPI("http://172.16.21.124/")
zapi.login("qihang","Qh0321.")
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
#根据keyname 获取item-id
def item_id(hostsname,keyname):
    Item_id = zapi.item.get(filter={'host':hostsname,'key_': keyname})[0]['itemid']
    return Item_id
#根据itemid，时间区间获取trend，并获取value_avg,value_min,value_max
def trend(ITEMID,TIME_FROM,TIME_STILL):
    value_avg={}
    #value_min=[]
    #value_max=[]
    for Trend in zapi.trend.get(itemids=ITEMID,time_from=TIME_FROM,time_still=TIME_STILL):
        value_avg.append(Trend['value_avg'])
        #value_min.append(Trend['value_min'])
        #value_max.append(Trend['value_max'])
    return value_avg
#通过计算返回一个trend最小值的一个字典
def tread_value_min(ITEMID,TIME_FROM,TIME_STILL):
    Value_min_all=zapi.trend.get(itemids=ITEMID,time_from=TIME_FROM,time_still=TIME_STILL)
    min=999
    for i in Value_min_all:
        if float(i['value_min']) < min:
            min = float(i['value_min'])
    value_min_q={}
    for i in Value_min_all:
        if float(i['value_min'])== min:
            #print i
            value_min_q=i
    return value_min_q['value_min'],value_min_q['clock']
#通过计算返回一个trend最大值的一个字典
def tread_value_max(ITEMID,TIME_FROM,TIME_STILL):
    Value_max_all=zapi.trend.get(itemids=ITEMID,time_from=TIME_FROM,time_still=TIME_STILL)
    max=0
    for i in Value_max_all:
        if float(i['value_max']) > max:
            max = float(i['value_max'])
    value_max_q={}
    for i in Value_max_all:
        if float(i['value_max'])== max:
            #print i
            value_max_q=i
    return value_max_q['value_max'],value_max_q['clock']
def tread_value_avg(ITEMID,TIME_FROM,TIME_STILL):
    Value_avg_all=zapi.trend.get(itemids=ITEMID,time_from=TIME_FROM,time_still=TIME_STILL)
    sum = 0
    for i in Value_avg_all:
        sum = sum + float(i['value_avg'])
    avg = sum/len(Value_avg_all)
    return avg

#解决时间问题：一周，每天时间转换时间戳。
def  date_week_to_timestamp():
    Week_from = time.mktime(time.strptime(commands.getoutput('date -d \'7 days ago\' +%Y%m%d'),"%Y%m%d"))
    Week_still = time.mktime(time.strptime(commands.getoutpu('date +%Y%m%d'),'%Y%m%d'))
    return Week_from,Week_still

if __name__ == '__main__':
    #Gid=group_id('api-bus_appstore')
    #print Gid
    dict=group_host(group_id('lb'))
    #print dict
    for i in dict.keys():
        print i,dict[i]
        Iid=item_id(i,'system.cpu.util[,idle]')
        #zapi.trend.get(itemids=71045,time_from=1490115600,time_still=1490155200)
        #print zapi.trend.get(itemids=Iid,time_from=1490115600,time_still=1490155200)
        #2017.3.13==1489334400
        #2017.3.19==1489852800
        qh_min_value,qh_min_clock=tread_value_min(Iid,1489334400,1489852800)
        qh_max_value,qh_max_clock=tread_value_max(Iid,1489334400,1489852800)
        qh_avg=tread_value_avg(Iid,1489334400,1489852800)
        print "cpu-idle_avg_value: %.4f" % qh_avg
        print "cpu-idle_min_value:[%s, %s]" %(qh_min_value,qh_min_clock)
        print "cpu-idle_max_value:[%s, %s]" %(qh_max_value,qh_max_clock)
        #print "trend-max-dict",qh_max
        #print "trend-min-list",qh_min
        #print "trend-max-list",qh_max
        '''value_avg=[]
        for trend in  zapi.trend.get(itemids=Iid,time_from=1490115600,time_still=1490155200)
            value_avg.append(trend['value_avg'])
        print "value_avg_list: ",value_avg
'''
