#!/usr/bin/env python
# coding: utf-8
from mzcore import *
import time
import json
class Clock(MzTimer):
	"""docstring for Clock"""
	def __init__(self):
		super(Clock, self).__init__()
		self.clock_run()
	def clock_run(self):
		@self.registerTimer(clock=1,unit="minute",name="sysinit")
		def sysinit():
			print "sysinit"
		@self.registerTimer(clock=10,name="forclock")
		def forclock():
			print "forclock"
			self.ticktock(name="forclock")
		@self.registerTimer(clock=1,unit="day",name="baseinfo")
		def baseinfo():
			print "baseinfo"
			# print time.localtime(time.time())
			today=time.strftime("%Y-%m-%d",time.localtime(time.time()))
			citylist=M("Out_CityList_Table").field("CityId").select()
			print today
			#SELECT `type`,city,`count` from (select t1.TypeId as type,t1.CityId as city,count(t1.Id) as count from Out_Station_Table t1 left join Out_CityList_Table t2 on t1.CityId = t2.CityId group by t1.TypeId,t1.CityId having t1.TypeId = 2 ) t8;
			#支撑单位数据type=2
			zcdw=M("").execute("SELECT `type`,city,`count` from (select t1.TypeId as type,t1.CityId as city,count(t1.Id) as count from Out_Station_Table t1 left join Out_CityList_Table t2 on t1.CityId = t2.CityId group by t1.TypeId,t1.CityId having t1.TypeId = 2 ) t8")
			dbzc=M("").execute('''SELECT
					'0' AS type,
					t3.CityId AS city,
					count(
						IF (t1.`Level` = 1, t1.`id`, NULL)
					) AS Levelcount1,
					count(
						IF (t1.`Level` = 2, t1.`id`, NULL)
					) AS Levelcount2,
					count(
						IF (t1.`Level` = 3, t1.`id`, NULL)
					) AS Levelcount3,
					count(
						IF (t1.`Level` = 4, t1.`id`, NULL)
					) AS Levelcount4,
					count(t1.`id`) AS count
				FROM
					t_Asset t1
				JOIN t_Unit t2 ON t1.UnitId = t2.Id
				JOIN Out_CityList_Table t3 ON t2.CityId = t3.CityId
				GROUP BY
				t3.CityId;''')
			gajg=M("").execute("select '1' as `type`,t1.CityId as city,count(t1.Id) as `count` from Out_Station_Table t1 left join Out_CityList_Table t2 on t1.CityId = t2.CityId group by t1.TypeId,t1.CityId having t1.TypeId = 3;")
			hmxf=M("").execute("select '7' as `type`,t2.CityId as city,count(t1.Id) as `count` from Out_StationCharger_Table t1 join Out_Station_Table t2 on t1.StationId = t2.StationId join Out_CityList_Table t3 on t2.CityId = t3.CityId where t1.TypeId = 4  group by t2.CityId;")
			nwzc=M("").execute('''select '4' as type,t3.CityId as city,count(t1.Id) as count 
					from t_Scandervice t1 join Out_Station_Table t2 on t1.unitId = t2.StationId 
					join Out_CityList_Table t3 on t2.CityId = t3.CityId group by t3.CityId;''')
			wj=M("").execute("select '8' as `type`,t2.CityId as city,count(t1.Id) as `count` from Out_StationCharger_Table t1 join Out_Station_Table t2 on t1.StationId = t2.StationId join Out_CityList_Table t3 on t2.CityId = t3.CityId where t1.TypeId = 2  group by t2.CityId;")
			xt=M("").execute('''select '5' as `type`,t3.CityId as city,count(t1.Id) as count
					from Out_Asset_Table t1 
					join Out_Station_Table t2 on t1.ProtectedId = t2.StationId 
					join Out_CityList_Table t3 on t2.CityId = t3.CityId group by t3.CityId;''')
			zbdw=M("").execute('''SELECT  t1.type,t1.city,t1.probcount as hardprobecount,t2.count as softprobecount,t3.count from (SELECT 3 as type,CityId as city,count(*) as probcount from Out_Station_Table where IsBar=1 GROUP BY CityId) t1 INNER JOIN  (SELECT
					'3' AS type,
					t3.CityId AS city,
					count(DISTINCT t1.`company`) AS count
				FROM
					domain_to_company t1
				JOIN Out_Station_Table t2 ON t1.company = t2.StationName
				JOIN Out_CityList_Table t3 ON t2.CityId = t3.CityId
				GROUP BY
					t3.CityId) t2 on t1.city=t2.city INNER JOIN

				(select type,city,count(distinct sname) as count from (
				select '3' as `type`,t1.CityId as city,t1.Id,t1.StationName as sname
				from Out_Station_Table t1 join Out_CityList_Table t3 on t1.CityId = t3.CityId  where t1.TypeId = 1 

				UNION ALL

				select '3' as `type`,t1.CityId as city,t1.Id,t1.UnitName as sname
				from t_Unit t1 join Out_CityList_Table t3 on t1.CityId = t3.CityId
				) t4 group by city) t3 on t1.city=t3.city;''')
			zcry=M("").execute("select '8' as `type`,t2.CityId as city,count(t1.Id) as `count` from Out_StationCharger_Table t1 join Out_Station_Table t2 on t1.StationId = t2.StationId join Out_CityList_Table t3 on t2.CityId = t3.CityId where t1.TypeId = 2  group by t2.CityId;")
			zcdwcount=0
			zbdwcount=0
			zcrycount=0
			xtcount=0
			wjcount=0
			dbzccount=0
			gajgcount=0
			hmxfcount=0
			nwzccount=0
			baseinfdata={}
			for cityv in citylist:
				key="baseinfo_%s_%s" % (str(today),cityv['CityId'])
				baseinfdata[key]={"message":{"base_result":{"data":{}}}}

			for zcdwv in zcdw:
				key="baseinfo_%s_%s" % (str(today),zcdwv['city'])
				zcdwcount+=int(zcdwv['count'])
				baseinfdata[key]["message"]["base_result"]["data"]["zcdw"]={"count":zcdwv['count'],"type":zcdwv['type']}
			for dbzcv in dbzc:
				key="baseinfo_%s_%s" % (str(today),dbzcv['city'])
				dbzccount+=int(dbzcv['count'])
				baseinfdata[key]["message"]["base_result"]["data"]["dbzc"]={"count":dbzcv['count'],"type":dbzcv['type']}
			for gajgv in gajg:
				key="baseinfo_%s_%s" % (str(today),gajgv['city'])
				gajgcount+=int(gajgv['count'])
				baseinfdata[key]["message"]["base_result"]["data"]["gajg"]={"count":gajgv['count'],"type":gajgv['type']}
			for hmxfv in hmxf:
				key="baseinfo_%s_%s" % (str(today),hmxfv['city'])
				hmxfcount+=int(hmxfv['count'])
				baseinfdata[key]["message"]["base_result"]["data"]["hmxf"]={"count":hmxfv['count'],"type":hmxfv['type']}
			for nwzcv in nwzc:
				key="baseinfo_%s_%s" % (str(today),nwzcv['city'])
				nwzccount+=int(nwzcv['count'])
				baseinfdata[key]["message"]["base_result"]["data"]["nwzc"]={"count":nwzcv['count'],"type":nwzcv['type']}
			for wjv in wj:
				key="baseinfo_%s_%s" % (str(today),wjv['city'])
				wjcount+=int(nwzcv['count'])
				baseinfdata[key]["message"]["base_result"]["data"]["wj"]={"count":wjv['count'],"type":wjv['type']}
			for xtv in xt:
				key="baseinfo_%s_%s" % (str(today),xtv['city'])
				xtcount+=int(xtv['count'])
				baseinfdata[key]["message"]["base_result"]["data"]["xt"]={"count":xtv['count'],"type":xtv['type']}
			for zbdwv in zbdw:
				key="baseinfo_%s_%s" % (str(today),zbdwv['city'])
				zbdwcount+=int(zbdwv['count'])
				baseinfdata[key]["message"]["base_result"]["data"]["zbdw"]={"count":zbdwv['count'],"type":zbdwv['type']}
			for zcryv in zcry:
				key="baseinfo_%s_%s" % (str(today),zcryv['city'])
				zcrycount+=int(zcryv['count'])
				baseinfdata[key]["message"]["base_result"]["data"]["zcry"]={"count":zcryv['count'],"type":zcryv['type']}
			key="baseinfo_%s" % str(today)
			baseinfdata[key]={"message":{"base_result":{"data":{"zcry":{"count":zcrycount},"zbdw":zbdwcount,"xt":xtcount,"wj":wjcount,"nwzc":nwzccount,"hmxf":hmxfcount,"gajg":gajgcount,"dbzc":dbzccount,"zcdw":zcdwcount}}}}
			print key
			r=R()
			r.set(key,json.dumps(baseinfdata))
			self.ticktock(name="baseinfo")
		# @self.registerTimer(clock=10,name="titck2")
		# def test1():
		# 	print "test Clock 1"
		# 	self.ticktock(name="titck2")
		