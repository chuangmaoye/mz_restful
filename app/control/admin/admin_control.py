#!/usr/bin/env python
# coding: utf-8
from mzcore import *
import json
import redis
import random
class Admin(Control):
	"""docstring for Admin"""
	def index(self):
		print appPath
		print timerlist()
		return "hell world"
	def rlt(self):
		rltdata=M("Out_Station_Table").field("Latitude,Longitude").select()
		for v in range(len(rltdata)):
			rltdata[v]['value']=int(random.random()*100)
		return json.dumps(rltdata)

	def baseinfo(self):
		return R().get("baseinfo_2018-04-12")
	def baseinfo1(self):
		return R().get("baseinfo_2018-04-12")
	def popredis(self):
		data=self.request.args.get("data","")
		r=redis.Redis(host=config("redis","host"),password=config("redis","password"),port= int(config("redis","port")),db=0)
		print self.mz.mzglobal.has_key("uukey")
		if self.mz.mzglobal.has_key("uukey"):
			print self.mz.mzglobal["uukey"]
			for v in self.mz.mzglobal["uukey"]:
				r.lpush(v,v+data)
		return "success"
	def getcompany(self):
		companylist=M("a_Company").field("id,CompanyName").select()
		return json.dumps(companylist)
	def setcompany(self):
		companyid=self.request.args.get("id","")
		lonlat=self.request.args.get("lonlat","")
		company=M("a_Company")
		where={}
		data={}
		lonlat=lonlat.split(" ")[0]
		where['ID']=int(companyid)
		data['Latitude']=lonlat.split(",")[0]
		data['Longitude']=lonlat.split(",")[1]
		company.where(where).save(data)
		return json.dumps({"succes":1})
