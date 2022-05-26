from radio import *
from encoder import *
import RPi.GPIO as GPIO
import atexit

class Controls:
    PLAY_PAUSE_PIN = 10
    NEXT_STATION_PIN = 22
    PREV_STATION_PIN = 27
    ENCODER_LEFT_PIN = 30
    ENCODER_RIGHT_PIN = 31

    def __init__(self, radio: Radio):
        self.radio = radio

        GPIO.setmode(GPIO.BCM)
        atexit.register(GPIO.cleanup)

        GPIO.setup(self.PLAY_PAUSE_PIN, GPIO.IN)
        GPIO.add_event_detect(self.PLAY_PAUSE_PIN, GPIO.FALLING, callback=self.play_pause_btn_callback, bouncetime=200)
        GPIO.setup(self.NEXT_STATION_PIN, GPIO.IN)
        GPIO.add_event_detect(self.NEXT_STATION_PIN, GPIO.FALLING, callback=self.next_station_btn_callback, bouncetime=200)
        GPIO.setup(self.PREV_STATION_PIN, GPIO.IN)
        GPIO.add_event_detect(self.PREV_STATION_PIN, GPIO.FALLING, callback=self.prev_station_btn_callback, bouncetime=200)

        self.encoder = Encoder(self.ENCODER_LEFT_PIN, self.ENCODER_RIGHT_PIN, callback=self.volume_change_callback)

    def play_pause_btn_callback(self, channel):
        self.radio.play_pause()

    def next_station_btn_callback(self, channel):
        self.radio.next_station()

    def prev_station_btn_callback(self, channel):
        self.radio.prev_station()

    def volume_change_callback(self, value):
        print(value)
