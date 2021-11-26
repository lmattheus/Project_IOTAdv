import RPi.GPIO as GPIO
import time
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN)
GPIO.setup(27,GPIO.IN)
GPIO.setup(5,GPIO.IN)
GPIO.setup(6,GPIO.IN)
status1 = ""
status2 = ""
status3 = ""
status4 = ""
counter = 4
while True:
	if (GPIO.input(22)==0 and status1 != "bezet"):
		print("bezet1")
		counter-=1
		status1 = "bezet"
		print(counter)

	elif (GPIO.input(22)==1 and status1 != ""):
		print("leeg")
		status1 = ""
		counter+=1
		print(counter)

	if (GPIO.input(27)==0 and status2 != "bezet"):
		print("bezet2")
		counter-=1
		status2 = "bezet"
		print(counter)

	elif (GPIO.input(27)==1 and status2 != ""):
		print("leeg")
		status2 = ""
		counter+=1
		print(counter)
	if (GPIO.input(5)==0 and status3 != "bezet"):
		print("bezet2")
		counter-=1
		status3 = "bezet"
		print(counter)

	elif (GPIO.input(5)==1 and status3 != ""):
		print("leeg")
		status3 = ""
		counter+=1
		print(counter)
	if (GPIO.input(6)==0 and status4 != "bezet"):
		print("bezet2")
		counter-=1
		status4 = "bezet"
		print(counter)

	elif (GPIO.input(6)==1 and status4 != ""):
		print("leeg")
		status4 = ""
		counter+=1
		print(counter)


	else:
		pass
	time.sleep(0.5)
	