from machine import ADC, Pin
from time import sleep

photoPIN = 26

def readLight(photoGP):
    photoRes = ADC(Pin(26))
    light = photoRes.read_u16() # 16-bit resolution. It will be between 0 and 65535
    light = round(light/65535*100,2)
    return light

while True:
    print("light: " + str(readLight(photoPIN)) +"%")
    sleep(1) # set a delay between readings