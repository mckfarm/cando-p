'''
Project: CANDO+P reactor operation
Purpose: Receive Arduino output and notify if water level is high
Output: csv of water level, text notification if level is high
Notes: written with Python 2.7
'''

# package import
import os
import serial
import csv
from twilio.rest import Client

# serial set up
ser = serial.Serial('COM4', 9600)
ser.flushInput()

# twilio SMS set up
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

# checking output
while True:
    ser_bytes = ser.readline()
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))

    with open("test.csv","a") as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerow([time.time(),decoded_bytes])

message_sent = False

# text message
# message = client.messages \
#                 .create(
#                      body='high water level',
#                      from_='+14023477198',
#                      to='+12624702789'
#                  )
#
# print message.sid
