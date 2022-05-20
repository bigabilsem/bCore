from machine import Pin, SPI
import struct
import time
from nrf24l01 import NRF24L01

trig = Pin(13, Pin.OUT)
echo = Pin(14, Pin.IN)
csn = Pin(5, mode=Pin.OUT, value=1)
ce  = Pin(10, mode=Pin.OUT, value=0)

pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

def setup():
    nrf = NRF24L01(SPI(0), csn, ce, payload_size=6)
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    return nrf

def olcum(nrf):
    while True:
        trig.low()
        time.sleep_us(2)
        trig.high()
        time.sleep_us(5)
        trig.low()
    
        while echo.value() == 0:
            signaloff = time.ticks_us()
    
        while echo.value() == 1:
            signalon = time.ticks_us()
        
        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2
        distance = int(distance)
    
        print("Mesafe: ", distance, "cm")
        
        try:
            nrf.send(struct.pack("i", distance))
            time.sleep(0.25)
        except OSError:
            print('message lost')
            
def auto_ack(nrf):
    nrf.reg_write(0x01, 0b11111000)  # enable auto-ack on all pipes
    

nrf = setup()
auto_ack(nrf)
olcum(nrf)
