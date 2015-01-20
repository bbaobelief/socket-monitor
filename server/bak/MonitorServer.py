from conf.hosts import group_dic 
import SocketServer,time
import json,sys
import redis_connector as redis 
#pull out all the monitored hosts and create a empty dict
host_dic = { }
for group,host_list in group_dic.items():
	for h_name, h_info  in host_list.items():
		host_dic[h_name] = { }
		



#print host_dic

#sys.exit()

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print 'got a connection from:' , self.client_address[0]
	data_type = self.request.recv(1024)
	if data_type == "SendMonitorData":
		print data_type
		print '\033[42;1msend back confirmation signal\033[0m'
		self.request.send('ReadyToReceive')
		status_data = json.loads(self.request.recv(8192) ) 
		status_data['last_recevied'] = time.time()
		if host_dic.has_key( status_data['hostname'] ) :
			host_dic[ status_data['hostname'] ] = status_data 
		#print status_data
	elif data_type == "PushDataIntoRedis":
		print "---------going to save data into redis....---done!!!"	
		redis.r['STATUS_DATA'] = json.dumps(host_dic)
		self.request.send('PushedDataIntoRedis')

        #print self.request.recv(1024)
	
	for h_name, values in host_dic.items():
		print "\033[42;1mdata from %s\033[0m" % h_name
		print values


if __name__ == "__main__":
    HOST, PORT = "", 9998
    # Create the server, binding to localhost on port 9999
    server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()

