#!/usr/bin/env python
import os,sys
import SocketServer,time
import pickle
from modules import env
from modules import mysql,SendMail


class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		print 'got a connection from:',self.client_address[0]
		while True:
			self.data = self.request.recv(1024).strip()
			if not self.data:
				print 'Client is disconnected...',self.client_address[0]
				break
			if self.data == 'InsertData':
				print self.data
				print "going to receive date",self.data
				self.request.send('ReadyToReceiveFile')
				while True:
					data = self.request.recv(4096)
					if data == 'DataSendDone':
						#print 'Transfer is done.'
						break
					else:
						Monitor_data = data
				Monitor_data = pickle.loads(Monitor_data)
				mysql.InsertData(Monitor_data)
			if self.data == 'UpdateData':
				print "going to receive date",self.data
				self.request.send('ReadyToReceiveFile')
				while True:
					data = self.request.recv(4096)
					print data
					if data == 'DataSendDone':
						#print 'Transfer is done.'
						break
					else:
						Monitor_data = data
				Monitor_data = pickle.loads(Monitor_data)
				mysql.UpdateData(Monitor_data)


#if __name__ == "__main__":
    #HOST,PORT = "",9000
    #server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
#server.serve_forever()
