#!/usr/bin/env python
# coding: utf-8
from mzcore import *
import json
from urlparse import *
import re
class Test(Control):
	"""docstring for test"""
	# def __init__(self,request):
	# 	super(Test, self).__init__(request)
	def userin(self):
		print self.request.args.get("id","")
		singlem=M("t_waf_list")
		userlist=singlem.field().limit(10).select()
		return json.dumps(userlist,cls=JsonExtendEncoder)
	def descurl(self):
		assetm=M("Out_Asset_Table");
		
	
		ret=assetm.field("id,AreaName").select()
		addr_regex = re.compile(r'[a-zA-z]+://[^\s.]*', re.IGNORECASE)#匹配网址，
		for rt in ret:
			where={}
			data={}
			
			try:
				k=rt["AreaName"]
				# print k
			except:
				k=""
			if k!= "" and k != None:
				# print k
				# print addr_regex.findall(k)
				
				# print k
				urlk= k.replace("`","").split(";")
				url=""
				if len(urlk)>1:
					if len(urlk)>3:
						url= urlk[2].split(":")[2]
				else:
					url=urlk[0]
				# print urlk[0]
				where['Id']=int(rt["id"])
				# result = urlparse(r["AreaName"])
				data['AreaName']=url
				assetm.where(where).save(data)
		return json.dumps(ret,cls=JsonExtendEncoder)