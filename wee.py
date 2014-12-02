#!/usr/bin/python3

from http.client import HTTPConnection
from time import sleep
from time import time
from sys import argv
import subprocess
import socket
import errno

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

	def __request(self, body, headers):
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
		return self.__request(wemoSwitch.bodyStatus, wemoSwitch.headersGet)

	def turnOn(self):
		return self.__request(wemoSwitch.bodyOn, wemoSwitch.headersSet)

	def turnOff(self):
		return self.__request(wemoSwitch.bodyOff, wemoSwitch.headersSet)

class watcher():
	def __init__(self, server, switch, watchInterval=10):
		self.server = server
		self.switch = switch
		self.watchInterval = watchInterval
		self.lastServerState = 1
		print("Created watcher for", self.server)

	def __connectionChecker(self):
		print("Conn check", self.server)
		conn = HTTPConnection(self.server, timeout=2)
		status = 1
		try:
			conn.connect()
		except socket.error as e:
			if e.errno != errno.ECONNREFUSED:
				status = 0 

		conn.close()
		return status

	def __pingChecker(self):
		print("Ping check", self.server)
		return not subprocess.call("ping -c 1 -w 1 {} > /dev/null".format(self.server), shell=True)

	def checkServer(self):
		startTime = time()
		stopTime = startTime + self.watchInterval

		total = 0
		count = 0

		while time() <= stopTime and count < 3:
			#total += self.__connectionChecker()
			total += self.__pingChecker()
			count += 1
			sleep(1)

		sleep(stopTime - time())

		state = round(total / count)

		if state:
			print("The server is present in the network")
		else:
			print("The server is not in the network")

		return state

	def start(self):
		while True:
			currentState = self.checkServer()

			edge = currentState - self.lastServerState

			if edge > 0:
				self.switch.turnOn()
			elif edge < 0:
				self.switch.turnOff()

			self.lastServerState = currentState

def test(wemo, phone):
	switch = wemoSwitch(wemo)
	switch.getStatus()
	switch.turnOff()
	sleep(1)
	switch.turnOn()
	watch = watcher(phone, switch)
	watch.start()

test("192.168.1.107", "192.168.1.128")