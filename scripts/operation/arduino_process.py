'''
Project: CANDO+P reactor operation
Purpose: Receive Arduino output, save log, and notify if water level is high
Output: csv of water level and N2O readings, text notification if level is high
Notes: written with Python 2.7
'''

# package import
import os
import serial
import csv
import logging
from __future__ import print_function
from logging.handlers import TimedRotatingFileHandler
from twilio.rest import Client

# serial set up
ser = serial.Serial('COM4', 9600)
ser.flushInput()

# logging set up
logname = "arduino.log"
handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
logger.addHandler(handler)

while True:
    ser_bytes = ser.readline()
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    print(decoded_bytes)
    with open("test.csv","a") as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerow([time.time(),decoded_bytes])

# twilio SMS set up
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

# text message
message = client.messages \
                .create(
                     body='high water level',
                     from_='+14023477198',
                     to='+12624702789'
                 )

print message.sid
