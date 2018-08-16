#!/usr/bin/env python
# coding: utf-8
from utils import *
import threading
class Mz(object):
	"""docstring for Mz"""
	def __init__(self):
		# super(Mz, self).__init__()
		self.__class__.__first_init = False
		self.host = config("run","host")
		self.port = int(config("run","port"))
		self.thread = bool(config("run","thread"))
		self.debug = bool(config("run","debug"))
		self.control = config("run","control")
		self.method = config("run","method")
		self.module = config("run","module")
		self.istimer=bool(config("setting","timer"))
		self.mzglobal = {}
		#之前回调[{"fnstr":"","fun":fun,"type":""}]
		self.beforecallback=[]
		#之后回调[{"fnstr":"","fun":fun,"type":""}]
		self.aftercallback=[]
		self.ws=object()
	def runtimer(self):
		if not self.istimer:
			return
		timers=timerlist()
		for v in timers:
			classname=v.split(".")[2].replace("_timer","").capitalize()
			try:
				c = __import__(v, fromlist=True)
			except:
				Log.error(traceback.format_exc())
				return
			if hasattr(c,classname):  # 判断在commons模块中是否存在inp这个字符串
				classname = getattr(c,classname)
				cla=classname()
				# self.timers_cla.append(cla)
				cla.run()
	def registCallBack(self,call,calltype="after"):
		if call:
			if calltype=="after":
				self.aftercallback.append(call)
			elif calltype=="before":
				self.beforecallback.append(call)
			else:
				return False
		else:
			return False

	def runCallBack(self,calldata,data,module,control,method,request):
		def call_fun():
			if isinstance(calldata,list):
				if len(calldata) > 0:
					for callkey,callvalue in calldata:
						ret_run(callvalue['fnstr'],callvalue['fun'],self,data,module,control,method,request)
		if len(calldata) > 0:
			replyThread = threading.Thread(target=call_fun)
			replyThread.setDaemon(True)
			replyThread.start()