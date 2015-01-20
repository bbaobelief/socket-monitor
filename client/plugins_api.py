#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import commands

def cpu_info():
    used_status = commands.getstatusoutput(""" top -b -n 1 | grep Cpu| awk '{print $2}'| cut -f 1 -d "." """)
    idle = commands.getstatusoutput(""" top -b -n 1 | grep Cpu| awk '{print $5}'| cut -f 1 -d "." """)
    return { 'status':0,'cpu_used':used_status[1],'idle':idle[1] }

def memory_info():
    mem = commands.getstatusoutput(""" free -m|grep Mem: """)
    meminfo = mem[1].split()
    
    return { 'status':0,'mem_used':int(int(meminfo[2])/int(meminfo[1])*100) }

def load_info():
    load_status = commands.getstatusoutput(""" uptime|awk -F'average:' '{print $2}'|awk -F',' '{print $1}' """)
    return { 'status':0,'uptime':load_status[1] }

if __name__ == '__main__':
    print cpu_info()
    print memory_info()
    print load_info()
