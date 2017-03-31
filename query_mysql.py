#!/usr/bin/env python
#coding:utf-8
#create_time: 2017/3/29
#author:sailq
import ast
from pyzabbix import ZabbixAPI
zapi = ZabbixAPI("http://domain")
zapi.login("user","passwd")
import MySQLdb
#建立一个连接
conn=MySQLdb.connect(host='host',user='user',passwd='passwd',db='dbname',port=3306)
#建立一个游标
cur =conn.cursor()
#根据group_name创建分组
def create_new_group(group_name):
    try:
        new=zapi.hostgroup.create(name=group_name)
        return new
    except Exception as e:
        pass
    #return new
#获取标准的host_name(ip)
def get_host():
    list = []
    remove_host_list=['192.168.100.1-H3C-5500','192.168.100.10-H3C-5500','192.168.100.3-H3C-5500','192.168.100.4-H3C-5500','192.168.100.2-H3C-5500','192.168.100.250-H3C-5800-Cluster','192.168.100.5-H3C-5500','192.168.100.6-H3C-5500','192.168.100.8-H3C-5500','172.16.21.45-H3C-5500','windows-WIN-2DKKICHMD6H']
    host = zapi.host.get()
    for i in host:
        list.append(i['name'])
    for d_host in remove_host_list:
        if d_host in list:
            list.remove(d_host)
    return list
#获取grains_id
def select_ip_id(id_ipinfo,ip):
    for i in id_ipinfo:
        if i[1] == None:
            continue
        for cc in ast.literal_eval(i[1]).values():
            if ip in cc:
                return i[0]
#grains_id = select_ip_id(group_name,"10.0.1.13")
#print grains_id
#根据grains_id 获取groupname
def select_groupname(grains_id):
    #cur.execute('select name from Grains_grains_groupname where grains_id=%d'%grains_id)
    cur.execute('select name from Grains_grains_groupname,Grains_group where grains_id=%d and Grains_group.id=Grains_grains_groupname.group_id'%grains_id)
    group_name_tuple = cur.fetchall()
    list_qh = []
    for  gname_tuple in group_name_tuple:
        for i in gname_tuple:
          list_qh.append(i)
    #print list_qh
    return list_qh
    #print(13,group_name)
#select_groupname(93)
# 根据groupname 那么获取group id
def get_group_id(group_name):
    Group_id = zapi.hostgroup.get(filter={'name':group_name})[0]['groupid']
    return Group_id
# 根据host_name 获取hostid
def get_host_id(host_name):
    Host_id=zapi.host.get(filter={'name':host_name})[0]['hostid']
    return Host_id
#更新hostgroup的分组
def update_host_group(host_id,group_id):
    #print host_id,group_id
    zapi.host.massadd(hosts=[{"hostid":host_id}],groups=[{'groupid':group_id}])

if __name__ == '__main__':

    #创建group
    cur.execute('select name from Grains_group')
    group_name = cur.fetchall()
    group_all_name_list = []
    for i in group_name:
        group_all_name_list.append(i[0])
    for i in group_all_name_list:
        create_new_group(i)

    zabbix_ip_list = get_host()
    cur.execute('select id,ipinfo from Grains_grains')
    Id_ipinfo =cur.fetchall()
    #grains_id = select_ip_id(Id_ipinfo,"10.0.1.13")
    #print grains_id
    for i in zabbix_ip_list:
        grains_id_qh = select_ip_id(Id_ipinfo,i)
        #print i,grains_id_qh
        if grains_id_qh ==None:
            continue
        group_list_name = select_groupname(grains_id_qh)
        if i.startswith("172.16.21"):
            group_list_name.append("test_envrionment")
        #last_list=[]
        for g in group_list_name:
            #print g,get_host_id(i),get_group_id(g)
            update_host_group(get_host_id(i),get_group_id(g))
            #last_list.append(get_group_id(g))
        #print i,group_list_name
    cur.close
    conn.close
