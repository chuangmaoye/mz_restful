#!/usr/bin/env python
# coding: utf-8
from mzcore import *
import json
import redis
from flask import jsonify
class Probe(Control):
	"""docstring for Admin"""
	def pushdata(self):
		if not self.request.json:
			retmsg={"status":204,"msg":"no data"}
			return jsonify(retmsg)
		data=self.request.json
		if not data.has_key("type"):
			retmsg={"status":204,"msg":"no data key"}
			return jsonify(retmsg)
		if not data.has_key("datalist"):
			retmsg={"status":204,"msg":"no data key"}
			return jsonify(retmsg)
		pushm=None
		if int(data['type'])==1:
			pushm=M("network_detection")
		elif int(data['type'])==2:
			pushm=M("file_detection")
		elif int(data['type'])==3:
			pushm=M("threat_detection")
		else:
			retmsg={"status":204,"msg":"no data type"}
			return jsonify(retmsg)
		for v in data['datalist']:
			self.pushweb(v,data['type'],True)
			pushm.add(v)
		retmsg={"status":200,"msg":"success"}
		return jsonify(retmsg)
	def pushweb(self,data=False,datatype=False,cil=False):
		print cil
		if cil:
			r=redis.Redis(host=config("redis","host"),password=config("redis","password"),port= int(config("redis","port")),db=0)
			print self.mz.mzglobal.has_key("uukey")
			data={"type":datatype,"data":data}
			if self.mz.mzglobal.has_key("uukey"):
				print self.mz.mzglobal["uukey"]
				for v in self.mz.mzglobal["uukey"]:
					r.lpush(v,jsonify(data))
		else:
			return False