#!/usr/bin/env python

import smtplib
import sys,os,json,time
import env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
from disk.models import Host,Disk,Alert_User,Mail_Server

def SendMail(Mail_To='',Subject='',Contents=''):
    try:
        mail_server = Mail_Server.objects.get(Status='on')
        print mail_server
    except:
        return False
    Smtp_Server = mail_server.SMTP_HOST
    Mail_User = mail_server.SMTP_USER
    Mail_Pass = mail_server.SMTP_PASS
    Mail_From = mail_server.MAIL_FROM

    if not Mail_To:
        alert_user = Alert_User.objects.filter(Status='on')
        Bad_Disk = Disk.objects.filter(Alert='Email')
        Mail_To = [user.Email for user in alert_user if user.Status == 'on']
        print Mail_To
        Bad_Disk_dict = {}
        line = 0
        for disk in Bad_Disk:
            line += 1
            if disk.Disk_for_Host.Alert_Switch == 'True':
                disk_info = [disk.Disk_for_Host.HostName,disk.Disk_for_Host.Host_Serial,disk.Disk_for_Host.Pri_IP,disk.Disk_for_Host.Pub_IP,disk.Disk_Capactiy,disk.Disk_Serial,disk.FW_State]
                Bad_Disk_dict[line] = disk_info


        Subject = 'Disk Monitor'
        Contents = ''
        for key,value in Bad_Disk_dict.items():
            content = '%s %s %s %s %s %s %s %s \n' %(key,value[0],value[1],value[2],value[3],value[4],value[5],value[6])
            content = content.encode()
            Contents += content

        print Contents
        if Contents == '':
            return False

    Ct="plain"
    Charset="utf-8"
    msg = "From: %s\r\n" % Mail_From \
        + "To: %s\r\n" % Mail_To \
        + "Content-type:text/%s; charset=\"%s\"\r\n" % (Ct, Charset) \
        + "Content-Transfer-Encoding: 8bit\r\n" \
        + "Subject: %s\r\n" % Subject \
        + "\r\n" \
        + Contents
    try:
        server = smtplib.SMTP(Smtp_Server)
        server.set_debuglevel(1)
        print 'login'
        server.login(Mail_User, Mail_Pass)
        ex_code = server.sendmail(Mail_From, Mail_To, msg)
        server.quit()
        return True
    except Exception, ex:
        print ex
        return False

if __name__ == '__main__':
   print SendMail()
