#!/usr/bin/python3

from http.client import HTTPConnection
from time import sleep
from sys import argv

class wemoSwitch():
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
		print("Created wemo switch on {}:{}".format(self.server, self.port))

	def _request(self, body, headers):
		conn = HTTPConnection(self.server, self.port)
		conn.request("POST", "/upnp/control/basicevent1", body, headers)
		response = conn.getresponse()
		state = -1
		if response.status == 200:
			state = response.read().decode("utf-8")[216:217] # Slice the returned binary state in the body
		conn.close()
		print("The switch's state is now:", state) # 0 = off, 1 = on, -1 = error
		return state

	def getStatus(self):
		return self._request(wemoSwitch.bodyStatus, wemoSwitch.headersGet)

	def turnOn(self):
		return self._request(wemoSwitch.bodyOn, wemoSwitch.headersSet)

	def turnOff(self):
		return self._request(wemoSwitch.bodyOff, wemoSwitch.headersSet)

def test(dest):
	switch = wemoSwitch(dest)
	switch.getStatus()
	switch.turnOff()
	sleep(1)
	switch.turnOn()

