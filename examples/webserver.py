import cherrypy
import os
from rfid import ten_digit_to_comma_format, RFIDClient

ip_address = '192.168.1.20'
controller_serial = 123106461
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

if __name__ == '__main__':
	server_config={
                'global': {'server.socket_host': '0.0.0.0',
		'server.socket_port':443,
		'server.ssl_module':'pyopenssl',
		'server.ssl_certificate':'server.crt',
		'server.ssl_private_key':'server.key',
		'log.access_file' : os.path.join("access.log")}
	}

	cherrypy.quickstart(RootServer(), '/accessControlApi', server_config)
