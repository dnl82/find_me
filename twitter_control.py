#!/usr/bin/env python3

from twython import Twython
import json
import time
import serial
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


app_key = "Kb1F0wdNnPNrydaLS7ISs4EKV"
app_secret = "Gt52bI9Hi8Oi3OjTcna8Ju5bmatHgEWB6hBSYaA9WDDEsc0m8D"
oauth_token = "828582153122365441-LSefccodxJyYxWHKbxw4CNNTRKUHUgr"
oauth_token_secret = "gk3XhVEFaeBvqXsFSdE1TuRkrOurjNedGS5S6Yn50KLuZ"
twitter = Twython(app_key,app_secret,oauth_token,oauth_token_secret)
previous = "null"

coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24

GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

delay  = 30  # rotation speed
steps = 3  # 3 step is 90 degree
status = 3  #Meeting


def forward(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(1, 0, 0, 1)
    time.sleep(delay)
 
def backwards(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(1, 0, 1, 0)
    time.sleep(delay)

def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)

def delete_tweet():
   timeline = twitter.get_user_timeline(count=1)
   for tweet in timeline:
        status = int(tweet['id_str'])
        twitter.destroy_status(id=status)

def check_twitter():
    print("I am in the twitter func")
    json_file = json.dumps(twitter.get_home_timeline()[0])
    
    data = json.loads(json_file)
    current_message = data["text"]
    print ("I have read the message")
    global status
#BackSoon == 0
#WFH == 1
#Onleave ==2
#Meeting == 3


    if current_message == "Meeting":
        print("Meeting")
        if status == 0: 			#BackSoon
            forward(int(delay) / 1000.0, int(steps))
        elif status == 1: 			#WFH
            forward(int(delay) / 1000.0, int(steps))
            forward(int(delay) / 1000.0, int(steps))
        elif status == 2: 			#Onleave
            backwards(int(delay) / 1000.0, int(steps))
        status = 3					#Meeting
        setStep(0, 0, 0, 0)
        delete_tweet()

    elif current_message == "WFH":
        print("WFH")
        if status == 0: 			#BackSoon
            backwards(int(delay) / 1000.0, int(steps))
        elif status == 2:			#Onleave
            forward(int(delay) / 1000.0, int(steps))
        elif status == 3:			#Meeting
            forward(int(delay) / 1000.0, int(steps))
            forward(int(delay) / 1000.0, int(steps))
        status = 1					#WFH
        setStep(0, 0, 0, 0)
        delete_tweet()

        
    elif current_message == "BackSoon":
        print("BackSoon")
        if status == 1:				#WFH
            forward(int(delay) / 1000.0, int(steps))
        elif status == 2:			#Onleave
            forward(int(delay) / 1000.0, int(steps))
            forward(int(delay) / 1000.0, int(steps))
        elif status == 3:			#Meeting
            backwards(int(delay) / 1000.0, int(steps))
        status = 0					#BackSoon
        setStep(0, 0, 0, 0)
        delete_tweet()


    elif current_message == "Leave":
        print("Leave")
        if status == 0:  			#BackSoon
            forward(int(delay) / 1000.0, int(steps))
            forward(int(delay) / 1000.0, int(steps))
        elif status == 1:			#WFH
            backwards(int(delay) / 1000.0, int(steps))
        elif status == 3:			#Meeting
            forward(int(delay) / 1000.0, int(steps))
        status = 2					#Onleave
        setStep(0, 0, 0, 0)
        delete_tweet()

def main():
#	try:
	while 1:
		print("Checking Twitter")
		check_twitter()
		for x in range (0,60):
			print('Time: %d'% (x))
			time.sleep(1)
#	except KeyboardInterrupt:
#		GPIO.cleanup()

if __name__ == "__main__":
	print("Starting")
	#sleep(60)
	main()
