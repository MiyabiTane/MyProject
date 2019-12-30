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

parser = argparse.ArgumentParser()
#please change IP
parser.add_argument("--ip", default='192.168.3.11',
                    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5075,
                    help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)

def sound_control():
    client.send_message("/filter", 9)
    play_sound.play_sound('./sounds/opening.mp3',14.5)

thread=threading.Thread(target=sound_control)
thread.start()

start=time.time()
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
count=0
sound_flag=0
images=[[0,140,325,300,300],[1,310,350,300,300],[2,475,350,300,300],[3,690,340,300,300],[4,850,350,300,300],[5,0,350,300,300],[6,1000,350,300,300],[0]]
info=[]
while len(images)>0:
    print("count={}".format(count))
    img=ame_movie.OpeningPicture('./images/sky.jpg',info)
    cv2.imwrite('./outputs/test_1223.jpg',img)
    img=cv2.resize(img,(640,480))
    cv2.imshow("result",img)

    if cv2.waitKey(1000) >= 0:
        break
    info.append(images.pop(0))
    count+=1
end=time.time()

time.sleep(14.5-(end-start))
