
from conf.templates import enabled_templates
from conf.hosts import group_dic 
monitor_host_dic = {}
for index,template in enumerate(enabled_templates):
	#print template.hosts, template.groups, template.service_dic
	for g in template.groups:
		for h,h_info in group_dic[g].items():
		   if monitor_host_dic.has_key(h): #exist already
			
		   	monitor_host_dic[h].append(index)
		   else:
			 monitor_host_dic[h] = [ index]
	
#print monitor_host_dic 



