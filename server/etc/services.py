#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DefaultService:
	name = None
	interval = 300
	warning_retry =  3
	critical_retry = 1
	threshold_cross_times = 3
	triggers = {} 
	graph_dic = {}
	data_from = 'agent'
	#if this sets to empty,all the status will be caculated in > mode , gt = > 
	lt_operator = []

# class UpCheck(DefaultService):
# 	name = 'upCheck'
# 	interval = 30
# 	triggers = {
# 		'host_status': [None]
# 	}

class Load(DefaultService):
	name = 'load'
	interval = 30
	triggers = {
		'uptime': {'type':'percentage','warning':0.1,'critical':0.2,'temp_dic':[],'last_item':0},
	}
	
class Cpu(DefaultService):
	name = 'cpu'
	interval = 60
	threshold_cross_times = 4
	plugin_name = 'cpu_info'
	triggers = {
		'cpu_used':{'type':'percentage','warning':10,'critical':60,'temp_dic':[],'last_item':0},
		#'system': ['percentage', 80, 90],
		'idle': {'type':'percentage','warning':10,'critical':5,'temp_dic':[],'last_item':0},
	}
	lt_operator = ['idle'] 

class Memory(DefaultService):
	name = 'memory'
	interval = 120
	triggers = {
		'mem_used': {'type':'percentage','warning':85,'critical':90,'temp_dic':[],'last_item':0},
		#'SwapUsage_p': ['percentage', 30, 40],
	}

class Windowscpu(DefaultService):
	name = 'windowscpu'
	interval = 80
	triggers = {
		'cpu_used': {'type':'percentage','warning':80,'critical':90,'temp_dic':[],'last_item':0},
	}

