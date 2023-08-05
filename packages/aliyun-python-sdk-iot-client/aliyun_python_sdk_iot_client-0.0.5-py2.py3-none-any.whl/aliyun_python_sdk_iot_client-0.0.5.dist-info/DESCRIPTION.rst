aliyun-python-sdk-iot
This is the iot module of Aliyun Python SDK.

Aliyun Python SDK is the official software development kit. It makes things easy to integrate your Python application, library, or script with Aliyun services.

This module works on Python versions:

2.6.5 and greater
Documentation:

Please visit http://develop.aliyun.com/sdk/python

* python demo

import aliyunsdkiotclient.AliyunIotMqttClient as iot
import ConfigParser
import json

config = ConfigParser.ConfigParser()
config.read('mqtt.cfg')

productKey = config.get('device', 'productKey')
deviceName = config.get('device', 'deviceName')
deviceSecret = config.get('device', 'deviceSecret')
clientId = config.get('device', 'clientId')

certPath = config.get('server', 'tslCertPath')
host = productKey + '.' + config.get('server', 'host')
port = config.getint('server', 'port')


def on_connect(client, userdata, flags_dict, rc):
	print("Connected with result code " + str(rc))
	# Subscribing in on_connect() means that if we lose the connection
	topic = '/' + productKey + '/' + deviceName + '/data'
	client.subscribe(topic, 0)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # publish an air condition data here
	topic = '/' + productKey + '/' + deviceName + '/update'
	print(msg.payload)
	data = {'pm25': 10, 'pm10': 30, 'deviceName': deviceName}
	client.publish(topic, payload=json.dumps(data))


if __name__ == '__main__':
	client = iot.getAliyunIotMqttClient(productKey, deviceName, deviceSecret, secure_mode=3)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host=host, port=port, keepalive=60)
	client.loop_forever()



.. :changelog:

Release History
---------------

0.0.1 (2018-02-13)
++++++++++++++++++

* Frustration
*


