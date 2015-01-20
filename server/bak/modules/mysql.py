#!/usr/bin/env python

import os,sys
import json
import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")

from disk.models import Host,Disk

def InsertData(Monitor_data):
	#host data format
	print Monitor_data
	HostName = Monitor_data['HostName']
	Pri_IP = Monitor_data['IpInfo']['Lan']
	Pub_IP = Monitor_data['IpInfo']['Wlan']
	Model_Name = Monitor_data['HardWareInfo']['Model']
	Cpu_Core = json.dumps(Monitor_data['HardWareInfo']['CPUInfo']['Cpu_Core'])
	Cpu_Model = Monitor_data['HardWareInfo']['CPUInfo']['Cpu_model']
	MemTotal = Monitor_data['HardWareInfo']['MEMInfo']['MemTotal']
	Mem_solt = 'None'
	#Mem_solt = json.dumps(Monitor_data['HardWareInfo']['MEMInfo']['Mem_Solt'])
	Product_Name = Monitor_data['HardWareInfo']['Product']
	Host_Serial = Monitor_data['HardWareInfo']['Serial']
	Release_Time = Monitor_data['HardWareInfo']['Release_Date']
	Uptime = Monitor_data['Uptime']
	print Host_Serial


	try:
		Host.objects.create(HostName=HostName,
						Pri_IP=Pri_IP,
						Pub_IP=Pub_IP,
						Model_Name=Model_Name,
						Cpu_Core=Cpu_Core,
						Cpu_Model=Cpu_Model,
						MemTotal=MemTotal,
						Mem_solt='None',
						Product_Name=Product_Name,
						Host_Serial=Host_Serial,
						Release_Time=Release_Time,
						Uptime=Uptime
						)
	except:
		Host.objects.filter(Host_Serial=Host_Serial).update(
						HostName=HostName,
						Pri_IP=Pri_IP,
						Pub_IP=Pub_IP,
						Model_Name=Model_Name,
						Cpu_Core=Cpu_Core,
						Cpu_Model=Cpu_Model,
						MemTotal=MemTotal,
						Mem_solt=Mem_solt,
						Product_Name=Product_Name,
						Release_Time=Release_Time,
						Uptime=Uptime)

	#disk data fromat
	HostId = Host.objects.get(Host_Serial=Host_Serial)
	DISK_ID = Monitor_data['DiskInfo'].keys()
	disk_err_total = 0
	for ID in DISK_ID:
		DiskID = ID
		Physical_ID = Monitor_data['DiskInfo'][ID][0]
		Disk_Serial = Monitor_data['DiskInfo'][ID][1]
		FW_State = Monitor_data['DiskInfo'][ID][2]
		Disk_Capactiy = Monitor_data['DiskInfo'][ID][3]
		Media_Error_Count = Monitor_data['DiskInfo'][ID][4]
		Other_Error_Count = Monitor_data['DiskInfo'][ID][5]
		Disk_defect = Monitor_data['DiskInfo'][ID][6]
		Disk_Score =  Monitor_data['DiskInfo'][ID][7]
		Alert = Monitor_data['DiskInfo'][ID][8]
		disk_err_total += int(Disk_defect)
		print disk_err_total
	


		try:
			Disk.objects.create(Disk_for_Host=HostId,
							DiskID=DiskID,
							Physical_ID=Physical_ID,
							Disk_Serial=Disk_Serial,
							FW_State=FW_State,
							Disk_Capactiy=Disk_Capactiy,
							Media_Error_Count=Media_Error_Count,
							Other_Error_Count=Other_Error_Count,
							Disk_defect=Disk_defect,
							Disk_Score=Disk_Score,
							Alert=Alert,
							)
		except:
			Disk.objects.filter(Disk_Serial=Disk_Serial).update(
							Disk_for_Host=HostId,
							DiskID=DiskID,
							Physical_ID=Physical_ID,
							FW_State=FW_State,
							Disk_Capactiy=Disk_Capactiy,
							Media_Error_Count=Media_Error_Count,
							Other_Error_Count=Other_Error_Count,
							Disk_defect=Disk_defect,
							Disk_Score=Disk_Score,
							Alert=Alert,
				)

	Host.objects.filter(Host_Serial=Host_Serial).update(Disk_Err_Total=disk_err_total)
	print disk_err_total

def UpdateData(Monitor_data):
	print Monitor_data
	Host_Serial = Monitor_data['Host_Serial']
	Uptime = Monitor_data['Uptime']
	print Host_Serial,Uptime
	host_update = Host.objects.filter(Host_Serial=Host_Serial).update(Uptime=Uptime)
