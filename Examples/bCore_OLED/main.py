# OLED ekran üzerinde mesafe sensörünü kullanarak resim ve metin gösterme.
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import machine
import utime

trigger = Pin(13, Pin.OUT)
echo = Pin(14, Pin.IN)


WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # I2C Pinlerini Ayarla -  GPIO8 & GPIO9 (varsayılan I2C0 pinleri)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Ekran adresini göster
print("I2C Configuration: "+str(i2c))                   # I2C konfigürasyonunu göster


oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # OLED ekranı başlatalım

# Raspberry Pi logo'sunu 32x32 bytearray içerisine alalım
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   print("Nesnenin uzaklığı ",distance,"cm")
   return distance;

while True:
    # Raspberry Pi logosunu (32x32 px) framebuffer içerisine alalım. 
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
    
    # Ekranı temizleyelim.
    oled.fill(0)
    
    # Resmin framebuffer'ını oled ekrana aktaralım.
    oled.blit(fb, 96, 24)
    
    # Bir başlık yazdıralım...
    oled.text("Biga BILSEM",5,0)
    

    dist = ultra()

    # Mesafeyi Ekrana Yazdıralım
    oled.text("Mesafe: ", 5, 20)
    oled.text(str(round(dist,2)), 5, 30)

    # Sonunda da ekranı güncelleyelim...
    oled.show()
    # Biraz uyuyalım...
    utime.sleep(0.1)


