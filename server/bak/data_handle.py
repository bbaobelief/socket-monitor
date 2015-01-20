#coding:utf-8
import socket,time,json
from conf.templates import enabled_templates
import redis_connector as redis
from get_monitor_index_dic import monitor_host_dic 


HOST = '192.168.2.139'    # The remote host
PORT = 9998    # The same port as used by the server

def send_status_data(action,status_data):

        # send monitor data to  server side 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
	status_dic = None
	if action == 'PushDataIntoRedis':
		s.send( 'PushDataIntoRedis')
		server_confirmation = s.recv(1024)
		if server_confirmation == "PushedDataIntoRedis":
        		print '---connecting redis to pull out data---' 
			status_dic = redis.r.get('STATUS_DATA')
			
        s.close()
	return status_dic 
	
while True:

	latest_status_dic =send_status_data('PushDataIntoRedis','' )
	if latest_status_dic is not None:
		latest_status_dic = json.loads(latest_status_dic)
		for h,t_list in monitor_host_dic.items():
			print h, t_list
			if latest_status_dic.has_key(h):
			  #if latest_status_dic[h]['last_received'] 
			  #print latest_status_dic[h]
			else:
				print "no valid data from %s in DB" %h
		
	else:
		print '----err: 出事啦, xiao jian---'	
	time.sleep(10)
