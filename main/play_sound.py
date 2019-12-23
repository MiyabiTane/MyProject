import cv2
import time
import pygame
import argparse

#memo 1=flip_rain 2=pakkun 3=flip_high 4=flip_low
def play_sound(music,sleep):
    pygame.mixer.init() #init
    pygame.mixer.music.load(music) #read
    pygame.mixer.music.play(1) #do
    time.sleep(sleep)
    pygame.mixer.music.stop() #finish
