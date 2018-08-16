#!/usr/bin/env python
# coding: utf-8
from mzcore import *
from mzcore.utils import *
from flask import Flask,request,url_for,abort, redirect,render_template,jsonify
# from flask_sockets import Sockets
# from gevent import pywsgi
# from geventwebsocket.handler import WebSocketHandler
from flask_uwsgi_websocket import WebSocket
import threading
import json
app = Flask(__name__)
sockets = WebSocket(app)
mz=Mz()
if __name__ == '__main__':
	# config={
	# 		"smtp_server":"smtp.163.com",
	# 		"smtp_username":"15118034654@163.com",
	# 		"smtp_password":"admin@yxzc!@",
	# 		"smtp_port":25
	# }
	# em=Email(config)
	# em.receiver(["424251913@qq.com","a18233000235@2980.com"]).subject(txt="玄武项目").text(data="项目进度").send()
	# run()

    # app.run(host='0.0.0.0')
	mz.runtimer()
	app.run(host=mz.host,port=mz.port,debug=mz.debug,threaded=mz.thread,threads=16)
@app.route('/',methods=['GET', 'POST','PUT','DELETE'])
def index():
	# return redirect('admin/admin/index')
	return render_template('index.html')
@app.route('/<control>/<method>',methods=['GET', 'POST','PUT','DELETE'])
def route(control,method="index"):
	classname=control.capitalize()
	try:
		c = __import__("app.control.%s_control" % control, fromlist=True)
	except:
		Log.error(traceback.format_exc())
		abort(404)
			
	if hasattr(c,classname):  # 判断在commons模块中是否存在inp这个字符串
		classname = getattr(c,classname)
		cla=classname(mz,request)
		if hasattr(cla,method):
			target_func = getattr(cla,method)  # 获取inp的引用
			ret_run("run beforcallback",mz.runCallBack,mz.beforecallback,False,False,control,method,request)
			ret=ret_run("control:%s" % method,target_func)
			if ret:
				# self.runCallBack(ret,False,control,method,request)
				ret_run("run aftercallback",mz.runCallBack,mz.aftercallback,ret,False,control,method,request)
				Log.info("control:%s->%s\n%s" %(method,time.strftime('%a, %d %b %Y %H:%M:%S %z'),ret))
				return ret
			else:
				abort(404)
		else:
			abort(404)
	else:
		abort(404)
@app.route('/<module>/<control>/<method>',methods=['GET', 'POST','PUT','DELETE'])
def fileroute(module,control,method="index"):
	global mz
	classname=control.capitalize()
	try:
		c = __import__("app.control.%s.%s_control" % (module,control), fromlist=True)
	except:
		Log.error(traceback.format_exc())
		abort(404)
	if hasattr(c,classname):  # 判断在commons模块中是否存在inp这个字符串
		classname = getattr(c,classname)
		cla=classname(mz,request)
		if hasattr(cla,method):
			target_func = getattr(cla,method)  # 获取inp的引用
			ret_run("run beforcallback",mz.runCallBack,mz.beforecallback,False,module,control,method,request)
			ret=ret_run("control:%s" % method,target_func)
			if ret:
				# self.runCallBack(ret,module,control,method,request)
				ret_run("run aftercallback",mz.runCallBack,mz.aftercallback,ret,module,control,method,request)
				Log.info("control:%s->%s\n%s" %(method,time.strftime('%a, %d %b %Y %H:%M:%S %z'),ret))
				return ret
			else:
				abort(404)
		else:
			abort(404)
	else:
		abort(404)
			# return "test"
@sockets.route('/<module>/<control>/<method>')
def wsroute(ws,module,control,method):
	global mz
	mz.ws=ws
	classname=control.capitalize()
	try:
		c = __import__("app.control.%s.%s_websocket" % (module,control), fromlist=True)
	except:
		Log.error(traceback.format_exc())
		return
	if hasattr(c,classname):  # 判断在commons模块中是否存在inp这个字符串
		classname = getattr(c,classname)
		cla=classname(mz,request)
		if hasattr(cla,method):
			target_func = getattr(cla,method)  # 获取inp的引用
			ret_run("run beforcallback",mz.runCallBack,mz.beforecallback,False,module,control,method,request)
			ret=ret_run("control:%s" % method,target_func)
			if ret:
				# self.runCallBack(ret,module,control,method,request)
				ret_run("run aftercallback",mz.runCallBack,mz.aftercallback,ret,module,control,method,request)
				Log.info("control:%s->%s\n%s" %(method,time.strftime('%a, %d %b %Y %H:%M:%S %z'),ret))
				return ret
			else:
				return
		else:
			return
	else:
		return

