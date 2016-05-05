#!/usr/bin/env python

from time import sleep
import iothub_client
from iothub_client import *
from sense_hat import SenseHat

connectionString = "HostName=IOTSuiteHub2.azure-devices.net;DeviceId=new-device;SharedAccessKey=GMU7nWQpY7/niQlKhKv2GofMvWfhiUcmmJqXzc3CQ6w="
Protocol = IoTHubTransportProvider.AMQP

sense = SenseHat()

msgTxt = "{\"deviceId\": \"myAMQPDevice\",\"temperature(C)\": %.1f, \"humidity(rh)\": %.1f, \"pressure(mbar)\": %.1f}"

def send_confirmation_callback(message, result, userContext):
	print ("Confirmation [%d] received result = %s" % (userContext, result))
	sense.set_rotation(270)
	sense.show_message(":)")

def iothub_client_init():
	print "Creating IoTHub Connection"
	iotHubClient = IoTHubClient(connectionString, Protocol)
	return iotHubClient

def iothub_client_run():
	# this function connects to iotHub and sends event
	print "Starting iothub_client_run routine"

	try:

		iotHubClient = iothub_client_init()

		while True:
			humidity = (round(sense.get_humidity(), 1))
			temp = (round(sense.get_temperature(), 1))
			barometer = (round(sense.get_pressure(), 1))
			msgTxtFormatted = msgTxt % (temp,humidity,barometer)
			print  "messageToHub = " + msgTxtFormatted
			message = IoTHubMessage(bytearray(msgTxtFormatted,'utf8'))
			iotHubClient.send_event_async(message, send_confirmation_callback, 1)
			sleep(12)

	except KeyboardInterrupt:
		print("IotHubCLient stopped by keyboard input")

print ("Starting device message send to IOTHub using %s " % Protocol)

iothub_client_run()
	
	
