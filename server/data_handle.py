#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
from etc import redis_connector as redis
from etc.hosts import *

#hosts = ['192.168.10.22','192.168.8.187']
#services = {'load':[120,'load_info',0],'cpu':[30,'cpu_info',0],'memory':[60,'memory_info',0]}
#leastinterval = []
def getredisdata(hostkey):
    # for h in hosts:
    #     print h
        service_data = redis.r.get(hostkey)
        if service_data:
            return json.loads(service_data)
        else:
            return None

def hoststatus():
    for h in host_list:
        for service_name,v in h.services.items():
            #print h,service_name,v.interval
            hostdata = getredisdata(h.ip_address)
            #print hostdata
            if hostdata:
                last_check =time.time() - hostdata['host_check']
                #判断主机是否存活
                if last_check <=30 + 10:  
                    #print "\033[32m %s--->%s\033[0m"%(host,last_check)
                    #判断服务状态
                    service_data = hostdata["result"]
                    last_time = time.time() - service_data[service_name]['check_time']
                    if last_time <= v.interval + 10:
                        #print s,last_time,interval
                        if service_data[service_name]['status'] == 0:
                            for index,val in v.triggers.items():
                                #print index,val
                                data_type = val['type']
                                warning = val['warning']
                                critical = val['critical']
                                temp_list = val['temp_dic']
                                index_val = service_data[service_name][index]
                                if index_val:
                                    if data_type == 'percentage' or data_type is int:
                                        index_val = float(index_val)

                                #如果最后检查时间和保存时间不相等
                                if service_data[service_name]['check_time'] != val['last_item']:
                                    #添加服务阀值列表10次
                                    temp_list.append(index_val)
                                    if  len(temp_list) > 10:
                                        del temp_list[0]
                                    val['last_item'] = service_data[service_name]['check_time']
                                    # temp_list.sort()

                                cross_warning_count = 0
                                cross_critical_count = 0

                                #print index,'----->',temp_list,'<-----'
                                #print val
                                #统计汇总报警次数
                                for item in temp_list:
                                    #先按照小于判断
                                    if index in v.lt_operator:
                                        if item < critical:
                                            #print "\033[41;37m %s__[%s]__%s \033[0m"%(index,critical,item)
                                            cross_critical_count +=1
                                        elif item < warning:
                                            #print "\033[43;30m %s__[%s]__%s \033[0m"%(index,warning,item)
                                            cross_warning_count +=1
                                    else:
                                        #compare part
                                        if item > critical:
                                            #print "\033[41;37m %s__[%s]__%s \033[0m"%(index,critical,item)
                                            cross_critical_count +=1
                                        elif item > warning:
                                            #print "\033[43;30m %s__[%s]__%s \033[0m"%(index,warning,item)
                                            cross_warning_count +=1

                                print index,"\033[33m %s \033[0m"%cross_warning_count,">"*5,"\033[31m %s \033[0m"%cross_critical_count

                                #超过3次报警
                                if cross_warning_count >=3:
                                    print "\033[43;30m %s::%s__[%s]__%s \033[0m"%(h.ip_address,index,warning,item)
                                elif cross_critical_count >=3:
                                    print "\033[41;37m %s::%s__[%s]__%s \033[0m"%(h.ip_address,index,critical,item)


                                # for item in temp_list:
                                #     #先按照小于判断
                                #     if index in v.lt_operator:
                                #         if index_val < critical:
                                #             print "\033[41;37m %s__[%s]__%s \033[0m"%(index,critical,index_val)
                                #             cross_critical_count +=1
                                #         elif index_val < warning:
                                #             print "\033[43;30m %s__[%s]__%s \033[0m"%(index,warning,index_val)
                                #             cross_warning_count +=1
                                #     else:
                                #         #compare part
                                #         if index_val > critical:
                                #             print "\033[41;37m %s__[%s]__%s \033[0m"%(index,critical,index_val)
                                #             cross_critical_count +=1
                                #         elif index_val > warning:
                                #             print "\033[43;30m %s__[%s]__%s \033[0m"%(index,warning,index_val)
                                #             cross_warning_count +=1
                                # print index,cross_warning_count,">"*5,cross_critical_count

                    else:
                        print "\033[41;37m %s--->%s \033[0m"%(service_name,last_time)
                else:
                    print "\033[41;37m %s--->%s \033[0m"%(h.ip_address,last_check)

while 1:
    hoststatus()
    time.sleep(5)