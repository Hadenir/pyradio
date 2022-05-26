#!/bin/python

# scp brzozkak@192.168.145.99:/malina/brzozkak/buildroot-2022.02/output/images/Image /tmp/d/user

import vlc
import time
import RPi.GPIO as GPIO

URL = 'http://us4.internet-radio.com:8266'


ENC_CLK = 2
ENC_DT  = 3

counter = 50

def clbck(s):
    global counter

    time.sleep(0.002)

    Switch_A = GPIO.input(ENC_CLK)
    Switch_B = GPIO.input(ENC_DT)

    if (Switch_A == 1) and (Switch_B == 0) : # A then B ->
        counter += 1
        # at this point, B may still need to go high, wait for it
        while Switch_B == 0:
            Switch_B = GPIO.input(ENC_DT)
        # now wait for B to drop to end the click cycle
        while Switch_B == 1:
            Switch_B = GPIO.input(ENC_DT)
        return

    elif (Switch_A == 1) and (Switch_B == 1): # B then A <-
        counter -= 1
         # A is already high, wait for A to drop to end the click cycle
        while Switch_A == 1:
            Switch_A = GPIO.input(ENC_CLK)
        return

    else: # discard all other combinations
        return

def main():
    # instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

    # player = instance.media_player_new()
    # media = instance.media_new(URL)
    # player.set_media(media)

    # player.play()

    # time.sleep(10)

    # player.stop()

    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENC_CLK, GPIO.IN)
    GPIO.setup(ENC_DT, GPIO.IN)

    GPIO.add_event_detect(ENC_CLK, GPIO.RISING, callback=clbck, bouncetime=2)

    return

if __name__ == '__main__':
    main()
