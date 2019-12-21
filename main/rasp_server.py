import argparse
import math
from pythonosc import dispatcher
from pythonosc import osc_server
import time
from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO

#for motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.OUT) #GPIO2
#default LOW
GPIO.output(2,GPIO.LOW)

# LED strip configuration:
LED_COUNT = 60        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Define functions which animate LEDs in various ways.
def gradationWipe(strip,color,wait_ms=20):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(strip.numPixels()//2-i-1, color+256*17*i)
        strip.setPixelColor(i+strip.numPixels()//2, color+256*17*i)
        #print(color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def lightAll(strip, color,wait):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
    time.sleep(wait)


def disappearRight(strip):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i,0)
        strip.show()


def disappearWipe(strip, wait_ms=20):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()//2):
        strip.setPixelColor(strip.numPixels()//2-i-1, 0)
        strip.setPixelColor(i+strip.numPixels()//2, 0)
        #print(color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def OpeningWipe(strip,color1,color2,iteration=100):
    for j in range(iteration):
        for q in range(2):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color1)
            strip.show()
            time.sleep(1)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color2)



def rasp_callback(unused_addr,num):
    if num==1:
        print("flip_rain")
        GPIO.output(2,GPIO.HIGH)
        theaterChase(strip, Color(0,50,255), wait_ms=40, iterations=5)
        disappearRight(strip)
        time.sleep(1)
        GPIO.output(2,GPIO.LOW)
    if num==2:
        print("paku")
        gradationWipe(strip,Color(150,50,50),wait_ms=20)
        disappearRight(strip)
    if num==3:
        print("flip_high") #pink
        colorWipe(strip,Color(255,45,55), wait_ms=10)
        disappearRight(strip)
    if num==4:
        print("flip_low") #orange
        colorWipe(strip,Color(255,50,0), wait_ms=10)
        disappearRight(strip)
    if num==5:
        print("dram")
        theaterChase(strip, Color(255,255,0), wait_ms=30, iterations=17)
        lightAll(strip, Color(255,255,0),2)
    if num==6:
        print("result")
        rainbowCycle(strip, wait_ms=10, iterations=3)
        disappearWipe(strip)
                    

parser_osc = argparse.ArgumentParser()
parser_osc.add_argument("--ip",
                    default='127.0.0.1', help="The ip to listen on")
parser_osc.add_argument("--port",
                    type=int, default=5005, help="The port to listen on")
args = .parse_args()

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/filter", rasp_callback)

server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()
