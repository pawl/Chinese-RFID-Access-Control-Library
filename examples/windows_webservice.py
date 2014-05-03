"""
The most basic (working) CherryPy 3.1 Windows service possible.
Requires Mark Hammond's pywin32 package.
"""

import win32serviceutil
import win32service

import cherrypy
import os
from rfid import ten_digit_to_comma_format, RFIDClient

ip_address = '192.168.1.20'
controller_serial = 11111111
client = RFIDClient(ip_address, controller_serial)   

class RootServer:
	@cherrypy.expose
	def index(self, apiKey=None, action=None, badge=None):
		if (apiKey == "secret"):
			if badge:
				badge = ten_digit_to_comma_format(int(badge)) 
				if (action == "remove"):
					try:
						client.remove_user(badge)
						return "User Removed Successfully"
					except:
						return "Failed To Remove User"
				elif (action == "add"):
					try:
						client.add_user(badge, [1,2])
						return "User Added Successfully"
					except:
						return "Failed To Add User"
				else:
					return "must specify an action"
			else:
				return "no badge number entered"
		else:
			return "" #return nothing when no API key is entered
	

class MyService(win32serviceutil.ServiceFramework):
	"""NT Service."""
	
	_svc_name_ = "CherryPyService"
	_svc_display_name_ = "CherryPy Service"

	def SvcDoRun(self):
		cherrypy.tree.mount(RootServer(), '/accessControlApi')
		
		# in practice, you will want to specify a value for
		# log.error_file below or in your config file.  If you
		# use a config file, be sure to use an absolute path to
		# it, as you can't be assured what path your service
		# will run in.
		cherrypy.config.update({
			'global': {'server.socket_host': '0.0.0.0',
			'server.socket_port':443,
			'server.ssl_module':'pyopenssl',
			'server.ssl_certificate':'server.crt',
			'server.ssl_private_key':'server.key',
			'log.access_file' : os.path.join("access.log")}
		})
		
		cherrypy.engine.start()
		cherrypy.engine.block()
		
	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		cherrypy.engine.exit()
		
		self.ReportServiceStatus(win32service.SERVICE_STOPPED) 
		# very important for use with py2exe
		# otherwise the Service Controller never knows that it is stopped !
		
if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(MyService)
