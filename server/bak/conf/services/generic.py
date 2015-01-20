

class DefaultService:
	name = None
	interval = 300
	warning_retry =  3
	critical_retry = 1
	monitor_dic = {} 
	graph_dic = {}
	data_from = 'agent'
	#if this sets to empty,all the status will be caculated in > mode , gt = > 
	
	lt_operator = []



