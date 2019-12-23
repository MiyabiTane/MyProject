import ame_movie
import game_result
import cv2
import time
import pygame
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
import play_sound
import threading

"""
parser = argparse.ArgumentParser()
#please change IP
parser.add_argument("--ip", default='127.0.0.1',
                    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,
                    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)
"""
def sound_control():
    play_sound.play_sound('./sounds/opening.mp3',10)
    #client.send_message("/filter", 9)

def opening():
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    count=0
    sound_flag=0
    while count<7:
        #opening sound
        if sound_flag==0:
            thread=threading.Thread(target=sound_control)
            thread.start()
            sound_flag=1

        print("count={}".format(count))
        if count==0:
            img=ame_movie.OpeningPicture('./images/sky.jpg',[[0,140,325,300,300]])
            cv2.imwrite('./outputs/test_1223_1.jpg',img)
            img=cv2.resize(img,(640,480))
            cv2.imshow("result",img)

        elif count==1:
            img=ame_movie.OpeningPicture('./outputs/test_1223_1.jpg',[[1,310,350,300,300]])
            cv2.imwrite('./outputs/test_1223_2.jpg',img)
            img=cv2.resize(img,(640,480))
            cv2.imshow("result",img)

        elif count==2:
            img=ame_movie.OpeningPicture('./outputs/test_1223_2.jpg',[[2,475,350,300,300]])
            cv2.imwrite('./outputs/test_1223_3.jpg',img)
            img=cv2.resize(img,(640,480))
            cv2.imshow("result",img)

        elif count==3:
            img=ame_movie.OpeningPicture('./outputs/test_1223_3.jpg',[[3,690,340,300,300]])
            cv2.imwrite('./outputs/test_1223_4.jpg',img)
            img=cv2.resize(img,(640,480))
            cv2.imshow("result",img)

        elif count==4:
            img=ame_movie.OpeningPicture('./outputs/test_1223_4.jpg',[[4,850,350,300,300]])
            cv2.imwrite('./outputs/test_1223_5.jpg',img)
            img=cv2.resize(img,(640,480))
            cv2.imshow("result",img)

        elif count==5:
            img=ame_movie.OpeningPicture('./outputs/test_1223_5.jpg',[[5,0,350,300,300]])
            cv2.imwrite('./outputs/test_1223_6.jpg',img)
            img=cv2.resize(img,(640,480))
            cv2.imshow("result",img)

        elif count==6:
            img=ame_movie.OpeningPicture('./outputs/test_1223_6.jpg',[[6,1000,350,300,300]])
            cv2.imwrite('./outputs/test_1223_7.jpg',img)
            img=cv2.resize(img,(640,480))
            cv2.imshow("result",img)

        if cv2.waitKey(1000) >= 0:
            break
        count+=1

opening()
