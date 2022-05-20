from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(15))
pwm.freq(50)

#Function to set an angle
#The position is expected as a parameter
def setServoCycle (position):
    pwm.duty_u16(position)
    sleep(0.01)


while True:
    for pos in range(1000,9000,50):
        setServoCycle(pos)
    for pos in range(9000,1000,-50):
        setServoCycle(pos)