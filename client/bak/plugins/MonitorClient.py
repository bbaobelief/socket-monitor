from conf.conf import *
import socket,json
import time
monitor_dic = {}
hostname = 'localhost'

HOST = '192.168.2.139'    # The remote host
PORT = 9998    # The same port as used by the server

def send_status_data(action,status_data):

        # send monitor data to  server side 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
	if action == 'SendMonitorData':
		print '----SendMonitorData----'
		s.send('SendMonitorData')
		server_confirmation = s.recv(1024)
		if server_confirmation == "ReadyToReceive":
        		s.sendall( status_data)

        data = s.recv(1024)
        print  data
        s.close()


for k,v in  enabled_services.items():
	if k == 'service':
		for (s_name, service_api) in v:
			monitor_dic[s_name] = {'last_check': 0 ,
						 'interval':service_api.interval,
						'plugin' : service_api #.plugin.monitor()
						}
			#print s_name, service_api.interval
			#print service_api.plugin.monitor()


#print monitor_dic
while True:
	status_dic = {'hostname': hostname }
	for service_name,value_dic in monitor_dic.items():
		print service_name, 
		print value_dic['last_check'] + value_dic['interval'] - time.time(),'sec to start next round'

		
		if time.time() - value_dic['last_check'] >= value_dic['interval']:
			#means you need to trigger the next round.
			print "\033[42;1mnext round for:\033[0m", service_name
			status_dic[service_name] = value_dic['plugin'].plugin.monitor()
			#put the latest time stamp into monitor dic
			value_dic['last_check'] = time.time() 
	if len(status_dic) >1:
	  print '----------sending status data to monitor server ----------'
	  send_status_data( 'SendMonitorData',json.dumps(status_dic) ) 
	  """
	  for k,v in  status_dic.items():
		print k
		if k != 'hostname':
			for index,value in v.items():
				print '\t',index,value
	  """
	time.sleep(2)
				
