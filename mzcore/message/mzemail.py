#!/usr/bin/env python
# coding: utf-8
from mzcore.config import Log
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from email.header import Header  
import os,time,re
import traceback
class Email(object):
	"""docstring for Email"""
	def __init__(self,config):
		super(Email, self).__init__()
		self.config = config
		self.smtp_server = config['smtp_server']
		self.smtp_username = config['smtp_username']
		self.smtp_password = config['smtp_password']
		self.smtp_port = int(config['smtp_port'])
		self.msg = MIMEMultipart()
	#收件人 一个 test@test.com ["123@dd.com","123@dd.com"]
	def receiver(self,data):
		self.receiver=data
		return self
	#发送内容可以是text或者html
	def text(self,mailtype="plain",code="utf-8",data=""):
		msgtxt=MIMEText(data,mailtype,code)
		self.msg.attach(msgtxt)
		return self
	def mailfile(self,code="utf-8",filename=""):
		att = MIMEText(open(filename, 'rb').read(), 'base64', code)  
		att["Content-Type"] = 'application/octet-stream'  
		att["Content-Disposition"] = 'attachment; filename="%s"' % filename
		self.msg.attach(att)
		return self
	def subject(self,code="utf-8",txt=""):
		self.msg['Subject']=Header(txt,code)
		return self
	def send(self):
		print 1
		self.msg['From'] = self.smtp_username  
		self.msg['To'] = ",".join(self.receiver)
		# self.msg['To'] = "liliang"
		self.msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
		
		self.smtp = smtplib.SMTP()  
		self.run("connect mail",self.smtp.connect,self.smtp_server,self.smtp_port)
		self.run("login mail",self.smtp.login,self.smtp_username, self.smtp_password)
		self.run("send mail",self.smtp.sendmail,self.smtp_username,self.receiver,self.msg.as_string())
		# self.smtp.sendmail(self.smtp_username,self.receiver,self.msg.as_string())
		self.msg = MIMEMultipart()
	def run(self,str, func, *args):
		t = time.time()
		# echo(str)
		r = False
		try:
			r = func(*args)
		except:
			Log.error(traceback.format_exc())
		if r:
			totalTime = int(time.time() - t)
			# echo(Constant.RUN_RESULT_SUCCESS % totalTime)
		else:
			pass
			# echo(Constant.RUN_RESULT_FAIL)
			# exit()
	def __del__(self):
		self.smtp.quit()
			