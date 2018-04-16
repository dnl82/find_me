#!/usr/bin/env python3

from twython import Twython
import json
import time
import serial
import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BCM)


app_key = "xxx" # here you should add you app_key
app_secret = "xxx" # here you should add you app_secret
oauth_token = "#xxx" # here you should add you oauth_token
oauth_token_secret = "xxx" # here you should add you oauth_token_secret
twitter = Twython(app_key,app_secret,oauth_token,oauth_token_secret)

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
        status_t = int(tweet['id_str'])
        twitter.destroy_status(id=status_t)

def check_twitter():
    print("I am in the twitter function")
    #json_file = json.dumps(twitter.get_home_timeline()[0])
    timeline = twitter.get_user_timeline(count=1)
    for tweets in timeline:
        current_message = tweets['text']
    #data = json.loads(json_file)
    #current_message = data["text"]
    print ("I have read the message: ")

#BackSoon == 0
#WFH == 1
#Leave ==2
#Meeting == 3
    file = open("status_file.txt", "r")
    current_position=file.read(1)
    file.close()

    if current_message == "Meeting":
        print("Meeting")
        if current_position == "0": 			#BackSoon
            forward(int(delay) / 1000.0, int(steps))
        elif current_position == "1": 			#WFH
            forward(int(delay) / 1000.0, int(steps))
            forward(int(delay) / 1000.0, int(steps))
        elif current_position == "2": 			#Onleave
            backwards(int(delay) / 1000.0, int(steps))
        current_position = 3					#Meeting
        file = open("status_file.txt","w")
        file.write(str(current_position))
        file.close()
        setStep(0, 0, 0, 0)
        delete_tweet()

    elif current_message == "WFH":
        print("WFH")
        if current_position == "0": 			#BackSoon
            backwards(int(delay) / 1000.0, int(steps))
        elif current_position == "2":			#Onleave
            forward(int(delay) / 1000.0, int(steps))
        elif current_position == "3":			#Meeting
            forward(int(delay) / 1000.0, int(steps))
            forward(int(delay) / 1000.0, int(steps))
        current_position = 1					#WFH
        file = open("status_file.txt","w")
        file.write(str(current_position))
        file.close()
        setStep(0, 0, 0, 0)
        delete_tweet()


    elif current_message == "BackSoon":
        print("BackSoon")
        if current_position == "1":				#WFH
            forward(int(delay) / 1000.0, int(steps))
        elif current_position == "2":			#Onleave
            forward(int(delay) / 1000.0, int(steps))
            forward(int(delay) / 1000.0, int(steps))
        elif current_position == "3":			#Meeting
            backwards(int(delay) / 1000.0, int(steps))
        current_position = 0					#BackSoon
        file = open("status_file.txt","w")
        file.write(str(current_position))
        file.close()
        setStep(0, 0, 0, 0)
        delete_tweet()


    elif current_message == "Leave":
        print("Leave")
        if current_position == "0":  			#BackSoon
            forward(int(delay) / 1000.0, int(steps))
            forward(int(delay) / 1000.0, int(steps))
        elif current_position == "1":			#WFH
            backwards(int(delay) / 1000.0, int(steps))
        elif current_position == "3":			#Meeting
            forward(int(delay) / 1000.0, int(steps))
        current_position = 2					#Onleave
        file = open("status_file.txt","w")
        file.write(str(current_position))
        file.close()
        setStep(0, 0, 0, 0)
        delete_tweet()

def main():
#	try:
	while 1:
		print("%s - Checking Twitter" % datetime.datetime.now())
		check_twitter()
		#for x in range (0,60):
			#print('Time: %d'% (x))
		time.sleep(60)
#	except KeyboardInterrupt:
#		GPIO.cleanup()

if __name__ == "__main__":
	print("Starting")
	#sleep(60)
	main()
