#!/usr/bin/env python
# coding: utf-8
from mzcore import *
import json
import redis
import threading
import time
import uuid
class Web3d(Control):
	def turn(self):
		turncont=0
		turndata=[
			{
				"lon":116.4072154982,
				"lat":39.9047253699,
				"title":"“寄生推”SDK云控作恶，300多款应用不幸躺枪",
				"des":"“寄生推”SDK开发商可以通过云端控制的方式对目标用户下发包含恶意功能的代码包，进行Root提权，静默应用安装等隐秘操作。",
				"region":"国内",
				"link":"http://www.freebuf.com/articles/terminal/168984.html",
				"time":"2018-04-18"
			},
			{
				"lon":139.7319925000,
				"lat":35.7090259000,
				"title":"黑客劫持路由器DNS分发银行木马，目标瞄准中日韩等国智能手机用户",
				"des":"“一场由网络黑客导演的恶意活动正在上演。其目的在于通过劫持路由器DNS来分发Android银行恶意软件，以窃取受害者的敏感信息、登录凭证和双重身份验证码。",
				"region":"亚洲",
				"link":"https://www.easyaq.com/news/1050540756.shtml",
				"time":"2018-04-18"
			},
			
			
			{
				"lon":-3.4359730000,
				"lat":55.3780510000,
				"title":"Ledger Nano S加密钱包再爆严重漏洞",
				"des":"硬件钱包允许用户在计算机设备上通过USB端口来完成加密货币的交易活动，但是它们并不会跟主机设备共享钱包私钥，因此恶意软件就无法获取硬件钱包的密钥了。但是Saleem Rashid却发现，当Ledger Nano S硬件钱包跟目标设备完成物理连接之后，他竟然可以获取到Ledger设备中的私钥。",
				"region":"英国",
				"link":"http://www.freebuf.com/vuls/166292.html",
				"time":"2018-04-18"
			},
			{
				"lon":-119.4179324000,
				"lat":36.7782610000,
				"title":"英特尔SPI Flash Flaw允许攻击者篡改或删除BIOS/UEFI固件",
				"des":"英特尔公司内部发现其旗下多个 CPU 产品家族的设计存在缺陷 CVE-2017-5703，该项安全漏洞在CVSSv3（用安全漏洞评分系统3.0版本）中评分7.9（满分10分）。此项缺陷允许攻击者篡改芯片中的 SPI Flash 存储器活动，而 SPI Flash 存储器属于启动过程当中的必要组件。",
				"region":"全球",
				"link":"https://www.easyaq.com/news/1901201220.shtml",
				"time":"2018-04-18"
			},
			{
				"lon":-95.7128910000,
				"lat":37.0902400000,
				"title":"weblogic远程代码执行漏洞",
				"des":"该漏洞为Oracle融合中间件（子组件：WLS核心组件）的Oracle WebLogic Server组件中的漏洞。易受攻击的weblogic服务允许未经身份验证的攻击者通过T3网络访问及破坏Oracle WebLogic Server。此漏洞的成功攻击可能导致攻击者接管Oracle WebLogic Server，造成远程代码执行。",
				"region":"美国",
				"link":"https://www.anquanke.com/post/id/105265",
				"time":"2018-04-18"
			},
			{
				"lon":104.1953970000,
				"lat":35.8616600000,
				"title":"Bondat蠕虫再度来袭！控制PC构建挖矿僵尸网络",
				"des":"近日，360互联网安全中心监测到流行蠕虫家族Bondat的感染量出现一轮小爆发。在这次爆发中，Bondat利用受害机器资源进行门罗币挖矿，并组建一个攻击WordPress站点的僵尸网络。",
				"region":"中国",
				"link":"https://www.anquanke.com/post/id/105282",
				"time":"2018-04-18"
			},
			{
				"lon":-120.7401385000,
				"lat":47.7510741000,
				"title":"Microsoft Word和Office 信息泄露漏洞",
				"des":"Microsoft Word和Office中存在信息泄露漏洞。远程攻击者可通过发送带有特制OLE对象的Rich Text Format邮件消息利用该漏洞获取敏感信息。以下产品和版本受到影响：Microsoft Office 2010 SP2，Microsoft Office 2016 Click-to-Run，Microsoft Office Compatibility Pack SP3；Microsoft Word 2007 SP3，Microsoft Word 2010 SP2，Microsoft Word 2013 RT SP1，Microsoft Word 2016。",
				"region":"全球",
				"link":"http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD=CNNVD-201804-678",
				"time":"2018-04-18"
			},
			

		]
		isws=True
		while isws:
			if turncont>6:
				turncont=0
			try:
				self.mz.ws.send(json.dumps(turndata[turncont]))
			except:
				isws=False
				break
				print traceback.format_exc()
				Log.error(traceback.format_exc())
			turncont+=1
			time.sleep(5)