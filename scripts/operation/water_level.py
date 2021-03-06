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
import datetime
from twilio.rest import Client

# file name
results = "test.csv"
# serial set up
ser = serial.Serial('COM4', 9600)
ser.flushInput()

# twilio SMS set up
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

# create empty csv
with open(results,"w") as new_file:
    pass

# initializing
message_sent = False
time_points = 0

while True:
    ser_bytes = ser.readline()
    decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
    print decoded_bytes
    with open(results,"ab") as f:
        writer = csv.writer(f,delimiter=",")
        writer.writerow([datetime.datetime.now(),decoded_bytes])
    if "high" in decoded_bytes:
        if message_sent == False:
            message = client.messages.create(body="high water level",
            from_="+14023477198",to="+12624702789")
            print message.sid
            message_sent = True
        elif message_sent == True:
            pass
