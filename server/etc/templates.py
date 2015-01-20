#!/usr/bin/env python
# -*- coding: utf-8 -*-
from services import *

class BaseTemplate:
        name = None
        groups = []
        hostname = [] 
        ip_address = None
        port = 22
        os = 'linux'
        services = {}

class LinuxGenericServices(BaseTemplate):
        name = 'Linux Generic services'
        groups = ['BJ', 'HK']
        hostname = ['zheng']

        #LinuxGenericServices.services['cpu'].triggers        
        services = {
        	'cpu': Cpu(),
             'memory': Memory(),
             'load':Load()
               #'upCheck': UpCheck()()
        }

class WindowsGenericServices(BaseTemplate):
        name = 'Windows Generic services'
        groups = [ 'HK']

        services = {
                'cpu': Windowscpu,
               #'upCheck': UpCheck()()
        }

enabled_templates = (
	LinuxGenericServices(),
	WindowsGenericServices(),
)
