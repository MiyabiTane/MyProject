import ame_movie
import cv2
import time
import pygame
import threading
global sound_flag

def play_sound(music,sleep):
    pygame.mixer.init() #init
    pygame.mixer.music.load(music) #read
    pygame.mixer.music.play(1) #do
    time.sleep(sleep)
    pygame.mixer.music.stop() #finish

#if point=minus
def game_result(point):
    flag=0
    original_point=point
    if point<0:
        flag=1
        point*=-1
    info=[]
    x_left=600
    while True:
        num=point%10
        info.append([num,x_left,300,400,400])
        point-=num
        if point==0:
            if flag==1:
                info.append([11,x_left-170,380,300,300])
            break
        point/=10
        x_left-=200
    info.append([10,700,600,400,400])

    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    #show finish
    sound_flag=0
    count=0
    while count<10:
        img=ame_movie.ResultPicture('./images/sky.jpg',[[12,250,200,800,800]])
        img=cv2.resize(img,(640,480))
        cv2.imshow("result",img)
        if sound_flag==0:
            play_sound('./sounds/finish.mp3',2)
            sound_flag=1
        if cv2.waitKey(20)>=0:
            break
        count+=1


    sound_flag=0
    count=0
    while count<5:
        #wait result
        img=ame_movie.ResultPicture('./images/sky.jpg',[[13,250,200,800,800]])
        img=cv2.resize(img,(640,480))
        cv2.imshow("result",img)
        if cv2.waitKey(20)>=0:
            break
        count+=1
        if sound_flag==0:
            play_sound('./sounds/dram.mp3',3)
            sound_flag=1

    sound_flag=0
    count=0
    while count<15:
        #show result
        time.sleep(2)
        if original_point>40:
            img=ame_movie.ResultPicture('./images/sky_nizi.jpg',info)
        elif original_point>20:
            img=ame_movie.ResultPicture('./images/sky_cloud.jpg',info)
        else:
            img=ame_movie.ResultPicture('./images/sky_rain.jpg',info)
        img = cv2.resize(img, (640,480))
        cv2.imshow("result",img)
        if cv2.waitKey(20) >= 0:
            break
        count+=1
        if sound_flag==0:
            play_sound('./sounds/result.mp3',4)
            sound_flag=1


#game_result(80)
#play_sound('./sound/result.mp3',3)
