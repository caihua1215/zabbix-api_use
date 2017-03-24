#!/usr/bin/env python
#coding:utf-8
import time
import commands
from pyzabbix import ZabbixAPI
zapi = ZabbixAPI("url")
zapi.login("user","passwd")
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
    Item= zapi.item.get(filter={'host':hostsname,'key_': keyname})
    if Item:
        Item_id = Item[0]['itemid']
    else:
        Item_id = 0
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
    if Value_min_all:
        min=999
        #print Value_min_all
        for i in Value_min_all:
            #print i
            if not  i['value_min']:
                print "no value_min"
                continue
            else:
                if float(i['value_min']) < min:
                    min = float(i['value_min'])
        value_min_q={}
        for i in Value_min_all:
            if float(i['value_min'])== min:
                #print i
                value_min_q=i
        return value_min_q['value_min'],value_min_q['clock']
    else:
        print "Value_min_all do not have value"
    return 0,0
    #return 0
#通过计算返回一个trend最大值的一个字典
def tread_value_max(ITEMID,TIME_FROM,TIME_STILL):
    Value_max_all=zapi.trend.get(itemids=ITEMID,time_from=TIME_FROM,time_still=TIME_STILL)
    if Value_max_all:
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
    else:
        print "Value_max_all do not have value"
    return 0,0
#通过计算返回一个trend平均值avg
def tread_value_avg(ITEMID,TIME_FROM,TIME_STILL):
    Value_avg_all=zapi.trend.get(itemids=ITEMID,time_from=TIME_FROM,time_still=TIME_STILL)
    if Value_avg_all:
        sum = 0
        for i in Value_avg_all:
            sum = sum + float(i['value_avg'])
        avg = sum/len(Value_avg_all)
        return avg
    else:
        print "####no value"
        return 0
#解决时间问题：一周，每天时间转换时间戳。
def  date_week_to_timestamp():
    Week_from = time.mktime(time.strptime(commands.getoutput('date -d \'7 days ago\' +%Y%m%d'),"%Y%m%d"))
    Week_still = time.mktime(time.strptime(commands.getoutput('date +%Y%m%d'),'%Y%m%d'))
    return Week_from,Week_still
if __name__ == '__main__':
    #获取所有分组
    group_name_list = []
    delete_group_name_list = [u'H3C-SWITCH',u'Network',u'Templates',u'Zabbix servers', u'Discovered hosts', u'Virtual machines', u'Hypervisors',u'\u4e16\u7eaa\u4e92\u8054\u673a\u623f', u'\u5168\u90e8\u4e3b\u673a',u'test_envrionment',u'Mikoomi Templates',u'\u7eff\u5730\u673a\u623f', u'Linux servers']
    for j in zapi.hostgroup.get():
        group_name_list.append(j['name'])
    #print len(group_name_list)
    for de_name in delete_group_name_list:
        if de_name in group_name_list:
            group_name_list.remove(de_name)
        else:
            print "dename not in list",type(de_name),de_name
    for group_name in group_name_list:
        dict=group_host(group_id(group_name))
        #print group_name,dict
        if len(dict) == 0:
            print group_name,"do not have host"
        else:
            Time_from,Time_still = date_week_to_timestamp()
            print 'Group_name:'+group_name +" "+commands.getoutput('date -d \'7 days ago\' +%Y%m%d')+" - "+commands.getoutput('date +%Y%m%d')
            for i in dict.keys():
                print i,dict[i]
                Iid=item_id(i,'system.cpu.util[,idle]')
                qh_min_value,qh_min_clock=tread_value_min(Iid,Time_from,Time_still)
                qh_max_value,qh_max_clock=tread_value_max(Iid,Time_from,Time_still)
                qh_avg=tread_value_avg(Iid,Time_from,Time_still)
                print "cpu-idle_avg_value: %.4f" % qh_avg
                print "cpu-idle_min_value:[%s, %s]" %(qh_min_value,qh_min_clock)
                print "cpu-idle_max_value:[%s, %s]" %(qh_max_value,qh_max_clock)
