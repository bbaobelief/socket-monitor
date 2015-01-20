#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta,abstractmethod

class MessageSender:
    __metaclass__ = ABCMeta

    @abstractmethod
    def Send(self):pass


class EmailSender(MessageSender):
    def __init__(self,email,content):
        self.Email = email
        self.Content = content

    def Send(self):
        #调用接口发送邮件
        print u' 邮件发送成功--->Email:%s;Content:%s'%(self.Email,self.Content)


class MsgSender(MessageSender):
    def __init__(self,telphone,content):
        self.Telphone = telphone
        self.Content = content

    def Send(self):
        #调用接口发送短信
        print u' 短信发送成功--->Telphone:%s;Content:%s'%(self.Telphone,self.Content)


# class WeChatSender(MessageSender):

class ResetPasswordHelper:
    def __init__(self,arg):
        self.MessageSender = arg

    def ResetPassword(self):
        self.MessageSender.Send()

def Main():
    messageSender = MsgSender('18611110000',u'监控信息')
    resetpwd = ResetPasswordHelper(messageSender)
    resetpwd.ResetPassword()

if __name__ == "__main__":
    Main()