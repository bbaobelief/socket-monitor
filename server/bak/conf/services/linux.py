from generic import DefaultService



class upCheck(DefaultService):
	name = 'upCheck'
	interval = 30
	monitor_dic = {
		'host_status': [None]
	}


class memory(DefaultService):
	name = 'memory'
	interval = 60
	monitor_dic = {
		'MemUsage_p': ['percentage', 80, 90],
		'SwapUsage_p': ['percentage', 30, 40],
	}

class cpu(DefaultService):
	name = 'cpu'
	interval = 60
	monitor_dic = {
		'iowait': ['percentage', 40,60],
		'system': ['percentage', 80, 90],
		'idle': ['percentage', 20,5 ]
	}
	lt_operator = ['idle'] 



