from machine import Pin
import utime

# setup PINs associations
echo = 14
trigger = 13

def distance (ech,trig):
 new_reading = False
 counter = 0
 distance = 0
 duration = 0
 echoPIN = Pin(ech, Pin.IN)
 trigPIN = Pin(trig, Pin.OUT)
 # send trigger
 trigPIN.value(0)
 utime.sleep_us(2)
 trigPIN.value(1)
 utime.sleep_us(10)
 trigPIN.value(0)
 utime.sleep_us(2)
 # wait for echo reading
 while not echoPIN.value():
   pass
   counter += 1
   if counter == 5000:
      new_reading = True
      break

 if new_reading:
    return False
 startT = utime.ticks_us()/1000000

 while echoPIN.value(): pass
 feedbackT = utime.ticks_us()/1000000

 # calculating distance
 if feedbackT == startT:
  distance = "N/A"
 else:
  duration = feedbackT - startT
  soundSpeed = 34300 # cm/s
  distance = duration * soundSpeed / 2
  distance = round(distance, 1)
 return distance

while True:
 print (" Distance: " + str(distance(echo,trigger))+ "   ", end='\r')
 utime.sleep(0.5)
