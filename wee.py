#!/usr/bin/python3

import http.client
from time import sleep

class wemoClient():
	bodyTop = """
	<?xml version="1.0" encoding="utf-8"?>
	<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
	   <s:Body>
	"""

	bodyBot  = """
	   </s:Body>
	</s:Envelope>
	"""

	bodyStatus = bodyTop + """
	      <u:GetBinaryState xmlns:u="urn:Belkin:service:basicevent:1"></u:GetBinaryState>
	""" + bodyBot

	bodyOn = bodyTop + """
	      <u:SetBinaryState xmlns:u="urn:Belkin:service:basicevent:1">
	         <BinaryState>1</BinaryState>
	         <Duration></Duration>
	         <EndAction></EndAction>
	         <UDN></UDN>
	      </u:SetBinaryState>
	""" + bodyBot

	bodyOff = bodyTop + """
	      <u:SetBinaryState xmlns:u="urn:Belkin:service:basicevent:1">
	         <BinaryState>0</BinaryState>
	         <Duration></Duration>
	         <EndAction></EndAction>
	         <UDN></UDN>
	      </u:SetBinaryState>
	""" + bodyBot

	headersBot = { 
				"Content-Type": "text/xml; charset=\"utf-8\"",
				"Accept": "",
				"User-Agent": "",
				"Connection": "close"
				}

	headersGet = dict(list({ "SOAPAction": "\"urn:Belkin:service:basicevent:1#GetBinaryState\"" }.items())	+ list(headersBot.items()))	

	headersSet = dict(list({ "SOAPAction": "\"urn:Belkin:service:basicevent:1#SetBinaryState\"" }.items())	+ list(headersBot.items()))

	# Takes two arguments: a wemo switch's ip and port
	def __init__(self, server, port="49153"):
		self.server = server
		self.port = port
		print("Created wemo client for", self.server, self.port)

	def _request(self, body, headers):
		conn = http.client.HTTPConnection(self.server, self.port)
		conn.request("POST", "/upnp/control/basicevent1", body, headers)
		response = conn.getresponse()
		conn.close()
		print(response.status, response.reason)
		return response

	def getStatus(self):
		return self._request(wemoClient.bodyStatus, wemoClient.headersGet)

	def turnOn(self):
		return self._request(wemoClient.bodyOn, wemoClient.headersSet)

	def turnOff(self):
		return self._request(wemoClient.bodyOff, wemoClient.headersSet)

dest = "192.168.1.107"

client = wemoClient(dest)

client.getStatus()

client.turnOff()

sleep(2)

client.turnOn()
