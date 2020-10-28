#!/usr/bin/python


import paho.mqtt.client as paho
import os
import socket
import ssl
import pygame, sys
from pygame.locals import *

from time import sleep
from random import uniform


connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

awshost = "data.iot.us-east-1.amazonaws.com"
awsport = 8883
clientId = "LabSeat"
thingName = "LabSeat"
caPath = "aws-iot-rootCA.crt"
certPath = "cert.pem"
keyPath = "private.pem"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

pygame.init()
myfont = pygame.font.SysFont("Arial", 60)
label = myfont.render("No Person Detected", 1, (225, 225, 0))
BLACK = (0,0,0)
WIDTH = 800
HEIGHT = 600
appDisplay = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
appDisplay.fill(BLACK)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            key = event.key
            if key == pygame.K_d:
                sensor = "Person Detected"
                label = myfont.render("Person Detected", 1, (225, 225, 0))
                mqttc.publish("Sensor Status: " + sensor, qos=1)
                print("msg sent:" + sensor)
            else:
                pass
        if event.type == KEYUP:
            key = event.key
            if key == pygame.K_d:
                sensor = "Person Not Detected"
                label = myfont.render(" No Person Detected", 1, (225, 225, 0))
                mqttc.publish("Sensor Status: " + sensor, qos=1)
                print("msg sent:" + sensor)
            else:
                pass
    appDisplay.fill(BLACK)
    appDisplay.blit(label, (100, 100))
    pygame.display.update()