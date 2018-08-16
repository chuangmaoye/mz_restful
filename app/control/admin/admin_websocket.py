#!/usr/bin/env python
# coding: utf-8
from mzcore import *
import json
import redis
import threading
import time
import uuid
class Admin(Control):
	def wsindex(self):
		while True:
			msginfo = self.mz.ws.receive()
			if msginfo is not None:
				print msginfo
				self.mz.ws.send(msginfo)
			else: return
	def pushweb(self):
		pool=redis.ConnectionPool(host=config("redis","host"),password=config("redis","password"),port= int(config("redis","port")),db=0)
		popread = redis.StrictRedis(connection_pool=pool)
		isws=True
		uukey=str(uuid.uuid1())
		print self.mz
		if self.mz.mzglobal.has_key("uukey"):
			self.mz.mzglobal["uukey"].append(uukey)
			print self.mz.mzglobal["uukey"]
		else:
			self.mz.mzglobal["uukey"]=[]
			self.mz.mzglobal["uukey"].append(uukey)
			print self.mz.mzglobal["uukey"]
		# def call_fun():
		# 	print self.mz.ws
		# 	while True:
		# 		print self.mz.ws.receive()
		# replyThread = threading.Thread(target=call_fun)
		# replyThread.setDaemon(True)
		# replyThread.start()
		while isws:
			time.sleep(0.1)
			try:
				info=popread.brpop(uukey,0)
			except:
				pool=redis.ConnectionPool(host=config("redis","host"),password=config("redis","password"),port= int(config("redis","port")),db=0)
				popread = redis.StrictRedis(connection_pool=pool)
				if popread.ping():
					isws=True
				else:
					isws=False
			try:
				self.mz.ws.send(info[1])
			except:
				isws=False
				break
				print traceback.format_exc()
				Log.error(traceback.format_exc())
		self.mz.mzglobal["uukey"].remove(uukey)
		print "close"

