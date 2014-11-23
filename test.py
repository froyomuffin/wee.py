#!/usr/bin/python3

import http.client
from time import sleep

class wemoClient():
	queryGet = """
	<?xml version="1.0" encoding="utf-8"?>
	<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
	   <s:Body>
	      <u:GetBinaryState xmlns:u="urn:Belkin:service:basicevent:1"></u:GetBinaryState>
	   </s:Body>
	</s:Envelope>
	"""
	queryOn = """
	<?xml version="1.0" encoding="utf-8"?>
	<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
	   <s:Body>
	      <u:SetBinaryState xmlns:u="urn:Belkin:service:basicevent:1">
	         <BinaryState>1</BinaryState>
	         <Duration></Duration>
	         <EndAction></EndAction>
	         <UDN></UDN>
	      </u:SetBinaryState>
	   </s:Body>
	</s:Envelope>
	"""
	queryOff = """
	<?xml version="1.0" encoding="utf-8"?>
	<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
	   <s:Body>
	      <u:SetBinaryState xmlns:u="urn:Belkin:service:basicevent:1">
	         <BinaryState>0</BinaryState>
	         <Duration></Duration>
	         <EndAction></EndAction>
	         <UDN></UDN>
	      </u:SetBinaryState>
	   </s:Body>
	</s:Envelope>
	"""

	headersGet = { "SOAPAction": "\"urn:Belkin:service:basicevent:1#GetBinaryState\"",	
				"Content-Type": "text/xml; charset=\"utf-8\"",
				"Accept": "",
				"User-Agent": "",
				"Connection": "close"}

	headersSet = { "SOAPAction": "\"urn:Belkin:service:basicevent:1#SetBinaryState\"",	
				"Content-Type": "text/xml",
				"Accept": "",
				"User-Agent": "",
				"Connection": "close"}

	# Takes two arguments: a wemo switch's ip and port
	def __init__(self, server, port="49153"):
		self.server = server
		self.port = port
		print("Created wemo client for", self.server, self.port)

	def status(self):
		conn = http.client.HTTPConnection(self.server, self.port)
		conn.request("POST", "/upnp/control/basicevent1", wemoClient.queryGet, wemoClient.headersGet)
		response = conn.getresponse()
		conn.close()
		return response

	def turnOn(self):
		conn = http.client.HTTPConnection(self.server, self.port)
		conn.request("POST", "/upnp/control/basicevent1", wemoClient.queryOn, wemoClient.headersSet)
		response = conn.getresponse()
		conn.close()
		return response

	def turnOff(self):
		conn = http.client.HTTPConnection(self.server, self.port)
		conn.request("POST", "/upnp/control/basicevent1", wemoClient.queryOff, wemoClient.headersSet)
		response = conn.getresponse()
		conn.close()
		return response

dest = "192.168.1.107"

client = wemoClient(dest)
response = client.status()
print(response.status, response.reason)

response = client.turnOn()
print(response.status, response.reason)

sleep(2)

response = client.turnOff()
print(response.status, response.reason)

# conn = http.client.HTTPConnection(dest,port)


# conn.request("POST", "/upnp/control/basicevent1", queryGet, headersGet)
# conn = http.client.HTTPConnection(dest,port)
# conn.request("POST", "/upnp/control/basicevent1", queryOn, headersSet)
# sleep(2)
# conn = http.client.HTTPConnection(dest,port)
# conn.request("POST", "/upnp/control/basicevent1", queryOff, headersSet)
# response = conn.getresponse()
# print(response.status, response.reason)