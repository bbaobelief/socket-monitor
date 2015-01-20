import conf
from plugins import cpu,memory,upCheck 


a = '12300000000000000000000000'

class MonitorBase:
	interval = 300 
	plugin = None 
	
class upCheckMonitor(MonitorBase):
	interval = 30 
	plugin = upCheck

class memoryMonitor(MonitorBase):
	interval = 60
	plugin = memory  

class cpuMonitor(MonitorBase):
	interval = 120
	plugin = cpu