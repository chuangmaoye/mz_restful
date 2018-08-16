#!/usr/bin/env python
# coding: utf-8
import threading
import signal
import time
class MzTimer(object):
	"""docstring for MzTimer"""
	def __init__(self):
		self.fun=[]
		self.timers=[]
		signal.signal(signal.SIGINT, self.sigint_handler)
		signal.signal(signal.SIGTERM, self.sigint_handler)
	def sigint_handler(self,signum, frame):
		for v in self.timers:
			v.cancel()
		exit()
	def registerTimer(self,clock=1,unit="second",name="ticktock"):
		'''
			clock is step
			unit second | minute | hour | day  
			name timer name 
		'''
		if unit=="second" or unit=="minute" or unit=="hour" or unit=="day":
			pass
		else:
			return False
		if not name:
			return False
		def register(fn):
			self.fun.append({"name":name,"fun":fn,"clock":clock,"unit":unit})
			return fn
		return register
	def runTimer(self,name=None):
		if not name:
			for v in self.fun:
				clock=self.convertclock(v["unit"],v["clock"])
				timer = threading.Timer(clock, v['fun'])
				timer.setDaemon(True)
				timer.start()
				self.timers.append(timer)
		else:
			for v in self.fun:
				if name==v["name"]:
					clock=self.convertclock(v["unit"],v["clock"])
					timer = threading.Timer(clock, v['fun'])
					timer.setDaemon(True)
					timer.start()
					self.timers.append(timer)
	def ticktock(self,name="ticktock"):
		self.runTimer(name)
	def convertclock(self,unit,clock):
		if unit=="minute":
			retclock=clock*60
			return retclock
		elif unit=="hour":
			retclock=clock*60*60
			return retclock
		elif unit=="day":
			localtime = time.localtime(time.time())
			retclock=(24*60*60)-((localtime.tm_hour*60*60)+(localtime.tm_min*60)+localtime.tm_sec)
			return retclock
		else:
			return clock
	def run(self):
		self.runTimer()




