#!/usr/bin/env python
#coding:utf-8
from pyzabbix import ZabbixAPI
from sys import argv
#Group_name_Q="web_beike"
Group_name_Q = argv[1]
zapi = ZabbixAPI("http://172.16.21.124/")
zapi.login("useer","passwd")
#根据输入groupname 获取groupid
def get_group_id(group_name):
    group=zapi.hostgroup.get(filter={'name' : group_name})
    group_id = group[0]['groupid']
    return group_id
#获取对应分组的主机的ip 即name。
def get_host_ip(Group_id):
  host = zapi.host.get(groupids=[Group_id])
  host_list=[]
  for i in host:
      host_list.append(i['name'])
  return host_list
#获取对应分组的主机在zabbix中的id。
def get_host_id(Group_id):
  host = zapi.host.get(groupids=[Group_id])
  host_id_list=[]
  for i in host:
      host_id_list.append(i['hostid'])
  return host_id_list
#获取对应分组的主机名字，和对应的id放入字典中。
def  get_host_ip_id(Group_id):
    host = zapi.host.get(groupids=[Group_id])
    host_ip_id_dict={}
    for i in host:
        host_ip_id_dict[i['name']]=i['hostid']
    return host_ip_id_dict
#获取对应item的id
def get_item_id(host_ID,item_name):
    item_id = zapi.item.get(filter={'hostids': host_ID,'name' : item_name})[0]['itemid']
    return item_id

def get_history(hostids,itemids,timefrom,timestill):
    history = zapi.history.get(hostids=hostids,itemids=itemids,timefrom=timefrom,timestill=timestill)
    return history
def calt_history():
  pass
G_ID=get_group_id(Group_name_Q)
IP_List=get_host_ip(G_ID)
host_DICT = get_host_ip_id(G_ID)
HOST_ID_LIST=host_DICT.values()
HOST_IP_LIST=host_DICT.keys()
IP_ITEMID_DICT={}
for i in HOST_IP_LIST:
  IP_ITEMID_DICT[i]=[host_DICT[i],zapi.item.get(filter={'host': i,'name' : "Available memory"})[0]['itemid']]
sum_list=[]
for i in IP_ITEMID_DICT:
    print i,IP_ITEMID_DICT[i][0],IP_ITEMID_DICT[i][1]
    #history = zapi.history.get(hostids=[IP_ITEMID_DICT[i][0]],itemids=[IP_ITEMID_DICT[i][1]],timefrom=1489647500,timestill=1489647566)
    history = zapi.history.get(hostids=[IP_ITEMID_DICT[i][0]],itemids=[IP_ITEMID_DICT[i][1]],limit=100)
    sum = 0
    for i in history:
        sum +=float(i['value'])
    sum_list.append(sum/len(history)/1024.00/1024.00/1024.00)
sum_avg=0
for i in sum_list:
    sum_avg +=float(i)
ava_m = sum_avg/len(sum_list)
print "Group_name: %s,avg_avaliable_memory: %.2f G" %(Group_name_Q,ava_m)
