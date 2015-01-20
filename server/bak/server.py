#!/usr/bin/env python
import os,sys,time
from modules.socket_server import MyTCPHandler
import multiprocessing
import SocketServer
from modules import SendMail
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
from disk.models import Timer


HOST,PORT = "",9000

def timer():
	while True:
		alert_time = []
		try:
			date = Timer.objects.filter(Status='on')
		except:
			date = ''
			pass
		for d in date:
			alert_time.append('%s-%s:%s:%s' %(d.week.encode(),d.hour.encode(),d.minute.encode(),d.second.encode()))
		time.sleep(1)
		now = time.strftime('%u-%R:%S')
		if now in alert_time:
			print now
			counter = 0
			while True:
				if counter <= 3:
					if SendMail.SendMail() is True:
						print 'send done'
						break
					else:
						counter += 1
				else:
					break


if __name__ == '__main__':
	server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
	server_thread = multiprocessing.Process(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()
	timer_thread = multiprocessing.Process(target=timer())
	timer_thread.start()
	print 'done'
