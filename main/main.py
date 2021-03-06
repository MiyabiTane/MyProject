import rospy
from jsk_recognition_msgs.msg import RectArray
from jsk_recognition_msgs.msg import Rect
import numpy as np
import ame_movie
import cv2
import random
import time as pytime
import game_result
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
import play_sound
import threading

#OSC communication
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default='192.168.3.11',
                    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5075,
                    help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

global flag
flag=0
message_arrived=False
def position_cb(msg):
    global message_arrived
    message_arrived=msg

def sound_thunder():
    play_sound.play_sound('./sounds/thunder.mp3',15)
def sound_kirarin():
    play_sound.play_sound('./sounds/kirarin.mp3',6)

try:
    #full screen
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    #show start
    sound_flag=0
    count=0
    while count<10:
        img=ame_movie.Some2OnePicture('./images/sky.jpg',[[3,250,200,800,800]])
        img=cv2.resize(img,(640,480))
        cv2.imshow("result",img)
        if sound_flag==0:
            play_sound.play_sound('./sounds/start.mp3',2)
            sound_flag=1
        if cv2.waitKey(20)>=0:
            break
        count+=1

    message_arrived=False
    rospy.init_node('umbrella_pos')
    rospy.Subscriber('/edgetpu_object_detector/output/rects',RectArray,position_cb)
    while not rospy.is_shutdown() and flag==0:
        if message_arrived:
            print("message_arrived")
            #full screen
            cv2.namedWindow('result', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            #make ame
            time_1=np.random.randint(0,90,11) #stage1
            time_2=np.random.randint(110,210,15) #stage2
            time_3=np.random.randint(220,310,15) #stage3
            time=np.concatenate([time_1,time_2,time_3],0)
            x_left=np.random.randint(270,820,len(time))
            #stage1
            images_rain=[0]*4
            images_candy=[1]*7
            #stage2
            images_rain_small=[25]*8
            images_rain_2=[0]*3
            images_candy_2=[1]*4
            #stage3
            images_candy_small=[2]*7
            images_pero=[16]*5
            images_candy_3=[1]*3

            images=np.concatenate([images_rain,images_candy,images_rain_small,images_rain_2,images_candy_2,images_candy_small,images_pero,images_candy_3],0)
            size=np.zeros((len(time),2))
            size[np.where(images==25)]=[100,100]
            size[np.where(images==2)]=[100,100]
            size[np.where(images==1)]=[140,140]
            size[np.where(images==16)]=[180,180]
            size[np.where(images==0)]=[140,140]
            fall_obs=[]
            #info of each ame
            for i in range(len(time)):
                fall_obs.append([images[i],x_left[i],0,size[i][0],size[i][1]])

            fps = 25
            j=0
            point=0
            info=np.array([])
            flip_info_r=np.array([])
            flip_info_l=np.array([])
            flip_info_rfar=np.array([])
            flip_info_lfar=np.array([])
            pakkun_list=np.array([])
            #小さいあめ
            flip_info_r_s=np.array([])
            flip_info_l_s=np.array([])
            flip_info_rfar_s=np.array([])
            flip_info_lfar_s=np.array([])

            while True:
                print("j={}".format(j))
                if j==100:
                    thread1=threading.Thread(target=sound_thunder)
                    thread1.start()

                if j==220:
                    thread2=threading.Thread(target=sound_kirarin)
                    thread2.start()

                if 220<=j and j<=320:
                    if j%4==0 or j%4==1:
                        pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[23,0,0,450,450]])
                    else:
                        pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[24,0,0,450,450]])

                elif j==100 or j==219:
                    pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[26,0,0,1300,1300]])
                elif j==101 or j==218:
                    pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[27,0,0,1300,1300]])
                elif j==102 or j==217:
                    pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[28,0,0,1300,1300]])
                elif j==103 or j==216:
                    pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[29,0,0,1300,1300]])
                elif j==104 or j==215:
                    pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[30,0,0,1300,1300]])
                elif j==105 or j==214:
                    pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[31,0,0,1300,1300]])
                elif j==106 or j==213:
                    pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[32,0,0,1300,1300]])
                elif 107<=j and j<=212:
                    pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400],[33,0,0,1300,1300]])
                else:
                    pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400]])

                flip_rain_info=np.array([])
                start_time = pytime.time()
                sound_list=[]

                #rects=[info1,info2...]
                um_pos_x=6000
                um_pos_y=6000
                if len(message_arrived.rects)>0:
                    x_min=10000
                    umb_index=100
                    #umbrella : 150<width<200 y~=115
                    for i in range(len(message_arrived.rects)):
                        if message_arrived.rects[i].height<150 and 100<message_arrived.rects[i].width and message_arrived.rects[i].width<250:
                            umb_index=i
                    #print("rects={}".format(message_arrived.rects[umb_index]))

                    if umb_index!=100:
                        um_pos_x=message_arrived.rects[umb_index].x+message_arrived.rects[umb_index].width/2
                        um_pos_y=message_arrived.rects[umb_index].y+message_arrived.rects[umb_index].height/2

                        um_pos_x=int(um_pos_x*65/24)-216
                        #consider the shadow of umbrella->-50
                        um_pos_y=int(um_pos_y*65/24)-50
                    #to satisfy the condition of flip ame
                    #um_pos_y=int(np.round(float(um_pos_y)/10)*10)
                        print("width={},height={}".format(message_arrived.rects[umb_index].width,message_arrived.rects[umb_index].height))

                    print("x={},y={}".format(um_pos_x,um_pos_y))

                if j in time:
                    num=np.where(time==j)[0][0]
                    #print("num={}".format(num))
                    info=info.tolist() #np.append is bad
                    info.append(fall_obs[num])
                    info=np.array(info)

                #pakkun goal
                if len(flip_info_r)>0 and len(np.where((750<=flip_info_r[:,2]) & (flip_info_r[:,2]<=950))[0])>0:
                    num_g=np.where((750<=flip_info_r[:,2]) & (flip_info_r[:,2]<=950))[0]
                    for k in num_g:
                        keep=flip_info_r[k]
                        keep=keep.tolist()
                        if 930<=keep[1] and keep[1]<=1130:
                            pakkun_list=np.array(pakkun_list)
                            pakkun_list=pakkun_list.tolist()
                            pakkun_list.append([7,900,800,400,400])
                            if 11<=keep[0] and keep[0]<=18:
                                pakkun_list.append([20,900,720,180,180])
                                point+=10
                            else:
                                pakkun_list.append([9,900,720,180,180])
                                point+=2
                            flip_info_r[k][4]=0
                            pakkun_list=np.array(pakkun_list)
                            sound_list.append(2)

                    flip_info_r=np.array(([l for l in flip_info_r if l[4]!=0]),dtype=np.int)


                if len(flip_info_rfar)>0 and len(np.where((750<=flip_info_rfar[:,2]) & (flip_info_rfar[:,2]<=950))[0])>0:
                    num_g=np.where((750<=flip_info_rfar[:,2]) & (flip_info_rfar[:,2]<=950))[0]
                    for k in num_g:
                        keep=flip_info_rfar[k]
                        keep=keep.tolist()
                        if 930<=keep[1] and keep[1]<=1130:
                            pakkun_list=np.array(pakkun_list)
                            pakkun_list=pakkun_list.tolist()
                            pakkun_list.append([7,900,800,400,400])
                            if 11<=keep[0] and keep[0]<=18:
                                pakkun_list.append([20,900,720,180,180])
                                point+=10
                            else:
                                pakkun_list.append([9,900,720,180,180])
                                point+=2
                            flip_info_rfar[k][4]=0
                            pakkun_list=np.array(pakkun_list)
                            sound_list.append(2)
                    flip_info_rfar=np.array(([l for l in flip_info_rfar if l[4]!=0]),dtype=np.int)


                if len(flip_info_l)>0 and len(np.where((750<=flip_info_l[:,2]) & (flip_info_l[:,2]<=950))[0])>0:
                    num_g=np.where((750<=flip_info_l[:,2]) & (flip_info_l[:,2]<=950))[0]
                    for k in num_g:
                        keep=flip_info_l[k]
                        keep=keep.tolist()
                        if 30<=keep[1] and keep[1]<=230:
                            pakkun_list=np.array(pakkun_list)
                            pakkun_list=pakkun_list.tolist()
                            pakkun_list.append([8,0,800,400,400])
                            if 11<=keep[0] and keep[0]<=18:
                                pakkun_list.append([20,220,720,180,180])
                                point+=10
                            else:
                                pakkun_list.append([9,220,720,180,180])
                                point+=2
                            flip_info_l[k][4]=0
                            pakkun_list=np.array(pakkun_list)
                            sound_list.append(2)
                    flip_info_l=np.array(([l for l in flip_info_l if l[4]!=0]),dtype=np.int)

                if len(flip_info_lfar)>0 and len(np.where((750<=flip_info_lfar[:,2]) & (flip_info_lfar[:,2]<=950))[0])>0:
                    num_g=np.where((750<=flip_info_lfar[:,2]) & (flip_info_lfar[:,2]<=950))[0]
                    for k in num_g:
                        keep=flip_info_lfar[k]
                        keep=keep.tolist()
                        if 30<=keep[1] and keep[1]<=230:
                            pakkun_list=np.array(pakkun_list)
                            pakkun_list=pakkun_list.tolist()
                            pakkun_list.append([8,0,800,400,400])
                            if 11<=keep[0] and keep[0]<=18:
                                pakkun_list.append([20,220,720,180,180])
                                point+=10
                            else:
                                pakkun_list.append([9,220,720,180,180])
                                point+=2
                            flip_info_lfar[k][4]=0
                            pakkun_list=np.array(pakkun_list)
                            sound_list.append(2)
                    flip_info_lfar=np.array(([l for l in flip_info_lfar if l[4]!=0]),dtype=np.int)

                #pakkun goal for small candy
                if len(flip_info_r_s)>0 and len(np.where((750<=flip_info_r_s[:,2]) & (flip_info_r_s[:,2]<=950))[0])>0:
                    num_g=np.where((750<=flip_info_r_s[:,2]) & (flip_info_r_s[:,2]<=950))[0]
                    for k in num_g:
                        keep=flip_info_r_s[k]
                        keep=keep.tolist()
                        if 930<=keep[1] and keep[1]<=1130:
                            pakkun_list=np.array(pakkun_list)
                            pakkun_list=pakkun_list.tolist()
                            pakkun_list.append([7,900,800,400,400])
                            pakkun_list.append([19,900,720,180,180])
                            point+=4
                            flip_info_r_s[k][4]=0
                            pakkun_list=np.array(pakkun_list)
                            sound_list.append(2)

                    flip_info_r_s=np.array(([l for l in flip_info_r_s if l[4]!=0]),dtype=np.int)


                if len(flip_info_rfar_s)>0 and len(np.where((750<=flip_info_rfar_s[:,2]) & (flip_info_rfar_s[:,2]<=950))[0])>0:
                    num_g=np.where((750<=flip_info_rfar_s[:,2]) & (flip_info_rfar_s[:,2]<=950))[0]
                    for k in num_g:
                        keep=flip_info_rfar_s[k]
                        keep=keep.tolist()
                        if 930<=keep[1] and keep[1]<=1130:
                            pakkun_list=np.array(pakkun_list)
                            pakkun_list=pakkun_list.tolist()
                            pakkun_list.append([7,900,800,400,400])
                            pakkun_list.append([19,900,720,180,180])
                            point+=4
                            flip_info_rfar_s[k][4]=0
                            pakkun_list=np.array(pakkun_list)
                            sound_list.append(2)
                    flip_info_rfar_s=np.array(([l for l in flip_info_rfar_s if l[4]!=0]),dtype=np.int)


                if len(flip_info_l_s)>0 and len(np.where((750<=flip_info_l_s[:,2]) & (flip_info_l_s[:,2]<=950))[0])>0:
                    num_g=np.where((750<=flip_info_l_s[:,2]) & (flip_info_l_s[:,2]<=950))[0]
                    for k in num_g:
                        keep=flip_info_l_s[k]
                        keep=keep.tolist()
                        if 30<=keep[1] and keep[1]<=230:
                            pakkun_list=np.array(pakkun_list)
                            pakkun_list=pakkun_list.tolist()
                            pakkun_list.append([8,0,800,400,400])
                            pakkun_list.append([19,220,720,180,180])
                            point+=4
                            flip_info_l_s[k][4]=0
                            pakkun_list=np.array(pakkun_list)
                            sound_list.append(2)
                    flip_info_l_s=np.array(([l for l in flip_info_l_s if l[4]!=0]),dtype=np.int)

                if len(flip_info_lfar_s)>0 and len(np.where((750<=flip_info_lfar_s[:,2]) & (flip_info_lfar_s[:,2]<=950))[0])>0:
                    num_g=np.where((750<=flip_info_lfar_s[:,2]) & (flip_info_lfar_s[:,2]<=950))[0]
                    for k in num_g:
                        keep=flip_info_lfar_s[k]
                        keep=keep.tolist()
                        if 30<=keep[1] and keep[1]<=230:
                            pakkun_list=np.array(pakkun_list)
                            pakkun_list=pakkun_list.tolist()
                            pakkun_list.append([8,0,800,400,400])
                            pakkun_list.append([19,220,720,180,180])
                            point+=4
                            flip_info_lfar_s[k][4]=0
                            pakkun_list=np.array(pakkun_list)
                            sound_list.append(2)
                    flip_info_lfar_s=np.array(([l for l in flip_info_lfar_s if l[4]!=0]),dtype=np.int)

                #flip again
                #right right
                if len(flip_info_r)>0 and len(np.where((um_pos_y-50<flip_info_r[:,2]) & (flip_info_r[:,2]<um_pos_y+50))[0])>0:
                    num_fr=np.where((um_pos_y-50<flip_info_r[:,2]) & (flip_info_r[:,2]<um_pos_y+50))[0]
                    for k in range(len(num_fr)):
                        keep=flip_info_r[num_fr[k]]
                        if um_pos_x-70<=keep[1] and keep[1]<um_pos_x+140:
                            keep[5]=keep[1]+90
                            flip_info_r=np.array(flip_info_r)
                            flip_info_r=flip_info_r.tolist()
                            flip_info_r.append(keep)
                            flip_info_r[num_fr[k]][4]=0
                            sound_list.append(3)
                    flip_info_r=np.array(([l for l in flip_info_r if l[4]!=0]),dtype=np.int)

                #right left
                if len(flip_info_r)>0 and len(np.where((um_pos_y-50<flip_info_r[:,2]) & (flip_info_r[:,2]<um_pos_y+50))[0])>0:
                    num_fr=np.where((um_pos_y-50<flip_info_r[:,2]) & (flip_info_r[:,2]<um_pos_y+50))[0]
                    for k in range(len(num_fr)):
                        keep=flip_info_r[num_fr[k]]
                        if um_pos_x-280<=keep[1] and keep[1]<um_pos_x-70:
                            keep[5]=keep[1]-90
                            flip_info_l=np.array(flip_info_l)
                            flip_info_l=flip_info_l.tolist()
                            flip_info_l.append(keep)
                            flip_info_l=np.array(flip_info_l)
                            flip_info_r[num_fr[k]][4]=0
                            sound_list.append(3)
                    flip_info_r=np.array(([l for l in flip_info_r if l[4]!=0]),dtype=np.int)


                #left left
                if len(flip_info_l)>0 and len(np.where((um_pos_y-50<flip_info_l[:,2]) & (flip_info_l[:,2]<um_pos_y+50))[0])>0:
                    num_fl=np.where((um_pos_y-50<flip_info_l[:,2]) & (flip_info_l[:,2]<um_pos_y+50))[0]
                    for k in range(len(num_fl)):
                        keep=flip_info_l[num_fl[k]]
                        if um_pos_x-280<=keep[1] and keep[1]<um_pos_x-70:
                            keep[5]=keep[1]-90
                            flip_info_l=np.array(flip_info_l)
                            flip_info_l=flip_info_l.tolist()
                            flip_info_l.append(keep)
                            flip_info_l[num_fl[k]][4]=0
                            sound_list.append(3)
                    flip_info_l=np.array(([l for l in flip_info_l if l[4]!=0]),dtype=np.int)

                #left right
                if len(flip_info_l)>0 and len(np.where((um_pos_y-50<flip_info_l[:,2]) & (flip_info_l[:,2]<um_pos_y+50))[0])>0:
                    num_fl=np.where((um_pos_y-50<flip_info_l[:,2]) & (flip_info_l[:,2]<um_pos_y+50))[0]
                    for k in range(len(num_fl)):
                        keep=flip_info_l[num_fl[k]]
                        if um_pos_x-70<=keep[1] and keep[1]<um_pos_x+140:
                            keep[5]=keep[1]+90
                            flip_info_r=np.array(flip_info_r)
                            flip_info_r=flip_info_r.tolist()
                            flip_info_r.append(keep)
                            flip_info_r=np.array(flip_info_r)
                            flip_info_l[num_fl[k]][4]=0
                            sound_list.append(3)
                    flip_info_l=np.array(([l for l in flip_info_l if l[4]!=0]),dtype=np.int)


                # think the relationship with umbrella
                if len(info)>0 and len(np.where((um_pos_y-50<info[:,2]) & (info[:,2]<um_pos_y+50))[0])>0:
                    #remove candy from info
                    num_f=np.where((um_pos_y-50<info[:,2]) & (info[:,2]<um_pos_y+50))[0]
                    for m in range(len(num_f)):
                        keep=info[num_f[m]]
                        keep=np.array(keep)
                        keep=keep.tolist()
                        if um_pos_x-70<=keep[1] and keep[1]<um_pos_x+140 and keep[0]!=2:
                            #remove ame from info
                            info[num_f[m]][4]=0
                            #add candy to flip_info
                            flip_info_r=np.array(flip_info_r)
                            flip_rain_info=np.array(flip_rain_info)
                            #candy only
                            if keep[0]==0:
                                keep[0]=4
                                flip_rain_info=flip_rain_info.tolist()
                                flip_rain_info.append(keep)
                                flip_rain_info.append([10,max(keep[1]-20,0),max(keep[2]-180,0),180,180])
                                point-=1
                                sound_list.append(1)
                            elif keep[0]==25:
                                keep[0]=4
                                flip_rain_info=flip_rain_info.tolist()
                                flip_rain_info.append(keep)
                                flip_rain_info.append([34,max(keep[1]-20,0),max(keep[2]-180,0),180,180])
                                point-=2
                                sound_list.append(1)
                            elif 14<=keep[0] and keep[0]<=18:
                                pakkun_list=np.array(pakkun_list)
                                pakkun_list=pakkun_list.tolist()
                                pakkun_list.append([21,keep[1],keep[2],150,150])
                                pakkun_list=np.array(pakkun_list)
                                sound_list.append(5)
                            else:
                                #x_center of parabola
                                keep.append(keep[1]+90)
                                flip_info_r=flip_info_r.tolist()
                                flip_info_r.append(keep)
                                sound_list.append(3)

                        elif um_pos_x-280<=keep[1] and keep[1]<um_pos_x-70 and keep[0]!=2:
                            #remove ame from info
                            info[num_f[m]][4]=0
                            #add candy to flip info
                            flip_info_l=np.array(flip_info_l)
                            flip_rain_info=np.array(flip_rain_info)
                            #candy only
                            if keep[0]==0:
                                keep[0]=4
                                flip_rain_info=flip_rain_info.tolist()
                                flip_rain_info.append(keep)
                                flip_rain_info.append([10,max(0,keep[1]-20),max(0,keep[2]-180),180,180])
                                point-=1
                                sound_list.append(1)
                            elif keep[0]==25:
                                keep[0]=4
                                flip_rain_info=flip_rain_info.tolist()
                                flip_rain_info.append(keep)
                                flip_rain_info.append([34,max(keep[1]-20,0),max(keep[2]-180,0),180,180])
                                point-=2
                                sound_list.append(1)
                            elif 14<=keep[0] and keep[0]<=18:
                                pakkun_list=np.array(pakkun_list)
                                pakkun_list=pakkun_list.tolist()
                                pakkun_list.append([22,keep[1],keep[2],150,150])
                                pakkun_list=np.array(pakkun_list)
                                sound_list.append(5)
                            else:
                                #x_centerof parabola
                                keep.append(keep[1]-90)
                                flip_info_l=flip_info_l.tolist()
                                flip_info_l.append(keep)
                                sound_list.append(3)

                        elif um_pos_x+140<=keep[1] and keep[1]<um_pos_x+280 and keep[0]!=2 and keep[0]!=25:
                            #remove
                            info[num_f[m]][4]=0
                            #to avoid error list.tolist()
                            flip_rain_info=np.array(flip_rain_info)
                            flip_info_rfar=np.array(flip_info_rfar)
                            #add candy to flip info
                            #candy only
                            if keep[0]==0:
                                keep[0]=4
                                flip_rain_info=flip_rain_info.tolist()
                                flip_rain_info.append(keep)
                                flip_rain_info.append([10,max(0,keep[1]-20),max(0,keep[2]-180),180,180])
                                point-=1
                                sound_list.append(1)
                            elif 14<=keep[0] and keep[0]<=18:
                                pakkun_list=np.array(pakkun_list)
                                pakkun_list=pakkun_list.tolist()
                                pakkun_list.append([21,keep[1],keep[2],150,150])
                                pakkun_list=np.array(pakkun_list)
                                sound_list.append(5)
                            else:
                                #x_centerof parabola
                                keep.append(keep[1]+110)
                                flip_info_rfar=flip_info_rfar.tolist()
                                flip_info_rfar.append(keep)
                                sound_list.append(4)

                        elif um_pos_x-420<=keep[1] and keep[1]<um_pos_x-280 and keep[0]!=2 and keep[0]!=25:
                            #remove
                            info[num_f[m]][4]=0
                            #add candy to flip info
                            flip_info_lfar=np.array(flip_info_lfar)
                            flip_rain_info=np.array(flip_rain_info)
                            #candy only
                            if keep[0]==0:
                                keep[0]=4
                                flip_rain_info=flip_rain_info.tolist()
                                flip_rain_info.append(keep)
                                flip_rain_info.append([10,max(keep[1]-20,0),max(0,keep[2]-180),180,180])
                                point-=1
                                sound_list.append(1)
                            elif 14<=keep[0] and keep[0]<=18:
                                pakkun_list=np.array(pakkun_list)
                                pakkun_list=pakkun_list.tolist()
                                pakkun_list.append([22,keep[1],keep[2],150,150])
                                pakkun_list=np.array(pakkun_list)
                                sound_list.append(5)
                            else:
                                #x_centerof parabola
                                keep.append(keep[1]-110)
                                flip_info_lfar=flip_info_lfar.tolist()
                                flip_info_lfar.append(keep)
                                sound_list.append(4)

                        #small candy
                        if um_pos_x-50<=keep[1] and keep[1]<um_pos_x+120 and keep[0]==2:
                            #x_center of parabola
                            keep.append(keep[1]+90)
                            #remove ame from info
                            info[num_f[m]][4]=0
                            #add candy to flip_info
                            flip_info_r_s=np.array(flip_info_r_s)
                            #candy only
                            flip_info_r_s=flip_info_r_s.tolist()
                            flip_info_r_s.append(keep)
                            sound_list.append(3)

                        elif um_pos_x-260<=keep[1] and keep[1]<um_pos_x-90 and keep[0]==2:
                            #x_centerof parabola
                            keep.append(keep[1]-90)
                            #remove ame from info
                            info[num_f[m]][4]=0
                            #add candy to flip info
                            flip_info_l_s=np.array(flip_info_l_s)
                            #candy only
                            flip_info_l_s=flip_info_l_s.tolist()
                            flip_info_l_s.append(keep)
                            sound_list.append(3)

                        elif um_pos_x+120<=keep[1] and keep[1]<um_pos_x+260 and keep[0]==2:
                            #x_centerof parabola
                            keep.append(keep[1]+110)
                            #remove
                            info[num_f[m]][4]=0
                            #to avoid error list.tolist()
                            flip_info_rfar_s=np.array(flip_info_rfar_s)
                            #add candy to flip info
                            #candy only
                            flip_info_rfar_s=flip_info_rfar_s.tolist()
                            flip_info_rfar_s.append(keep)
                            sound_list.append(4)

                        elif um_pos_x-400<=keep[1] and keep[1]<um_pos_x-260 and keep[0]==2:
                            #x_centerof parabola
                            keep.append(keep[1]-110)
                            #remove
                            info[num_f[m]][4]=0
                            #add candy to flip info
                            flip_info_lfar_s=np.array(flip_info_lfar_s)
                            #candy only
                            flip_info_lfar_s=flip_info_lfar_s.tolist()
                            flip_info_lfar_s.append(keep)
                            sound_list.append(4)
                    #for debug
                    print("flip_rain_info={}".format(flip_rain_info))
                    info=np.array(([l for l in info if l[4]!=0]),dtype=np.int)
                    flip_info_r=np.array((flip_info_r),dtype=np.int)
                    flip_info_l=np.array((flip_info_l),dtype=np.int)
                    flip_info_rfar=np.array((flip_info_rfar),dtype=np.int)
                    flip_info_lfar=np.array((flip_info_lfar),dtype=np.int)
                    flip_rain_info=np.array((flip_rain_info),dtype=np.int)
                    flip_info_r_s=np.array((flip_info_r_s),dtype=np.int)
                    flip_info_l_s=np.array((flip_info_l_s),dtype=np.int)
                    flip_info_rfar_s=np.array((flip_info_rfar_s),dtype=np.int)
                    flip_info_lfar_s=np.array((flip_info_lfar_s),dtype=np.int)
                print("flip_rain_info={}".format(flip_rain_info))

                if len(flip_info_r)>0:
                    #ペロペロキャンディの回転
                    num2=np.where(flip_info_r[:,0]==18)
                    num=np.where((11<=flip_info_r[:,0]) & (flip_info_r[:,0]<=17))
                    flip_info_r[num,0]+=np.array([1]*len(num[0]),dtype=np.int)
                    flip_info_r[num2,0]-=np.array([7]*len(num2[0]),dtype=np.int)
                    flip_info_r[num,2]+=np.array([5]*len(num[0]),dtype=np.int)
                    flip_info_r[num2,2]+=np.array([5]*len(num[0]),dtype=np.int)

                    flip_info_r[:,1]+=np.array([10]*len(flip_info_r),dtype=np.int)
                    #make parabola
                    num_3=np.where(flip_info_r[:,1]<flip_info_r[:,5])
                    flip_info_r[num_3,2]-=np.array([15]*len(num_3[0]),dtype=np.int)
                    num_4=np.where(flip_info_r[:,1]>flip_info_r[:,5])
                    flip_info_r[num_4,2]+=np.array([10]*len(num_4[0]),dtype=np.int)
                    #flip_info[:,2]=parabola(a=0.5,x_left=flip_info[:,1],y_up=flip_info[:,2],x_cen=flip_info[:,5],y_plus=10)
                flip_info_r=np.array([l for l in flip_info_r if (l[1]<1100 and 0<l[2] and l[2]<1100)])
                print("flip_info_r={}".format(flip_info_r))

                if len(flip_info_l)>0:
                    #ペロペロキャンディの回転
                    num2=np.where(flip_info_l[:,0]==18)
                    num=np.where((11<=flip_info_l[:,0]) & (flip_info_l[:,0]<=17))
                    flip_info_l[num,0]+=np.array([1]*len(num[0]),dtype=np.int)
                    flip_info_l[num2,0]-=np.array([7]*len(num2[0]),dtype=np.int)
                    flip_info_l[num,2]+=np.array([5]*len(num[0]),dtype=np.int)
                    flip_info_l[num2,2]+=np.array([5]*len(num2[0]),dtype=np.int)

                    flip_info_l[:,1]-=np.array([10]*len(flip_info_l),dtype=np.int)
                    #make parabola
                    num_5=np.where(flip_info_l[:,1]>flip_info_l[:,5])
                    flip_info_l[num_5,2]-=np.array([15]*len(num_5[0]),dtype=np.int)
                    num_6=np.where(flip_info_l[:,1]<flip_info_l[:,5])
                    flip_info_l[num_6,2]+=np.array([10]*len(num_6[0]),dtype=np.int)
                flip_info_l=np.array([l for l in flip_info_l if (0<l[1] and 0<l[2] and l[2]<1100)])
                print("flip_info_l={}".format(flip_info_l))

                if len(flip_info_rfar)>0:
                    #ペロペロキャンディの回転
                    num2=np.where(flip_info_rfar[:,0]==18)
                    num=np.where((11<=flip_info_rfar[:,0]) & (flip_info_rfar[:,0]<=17))
                    flip_info_rfar[num,0]+=np.array([1]*len(num[0]),dtype=np.int)
                    flip_info_rfar[num2,0]-=np.array([7]*len(num2[0]),dtype=np.int)
                    flip_info_rfar[num,2]+=np.array([5]*len(num[0]),dtype=np.int)
                    flip_info_rfar[num2,2]+=np.array([5]*len(num[0]),dtype=np.int)

                    flip_info_rfar[:,1]+=np.array([10]*len(flip_info_rfar),dtype=np.int)
                    #make parabola
                    num_7=np.where(flip_info_rfar[:,1]<flip_info_rfar[:,5])
                    flip_info_rfar[num_7,2]-=np.array([10]*len(num_7[0]),dtype=np.int)
                    num_8=np.where(flip_info_rfar[:,1]>flip_info_rfar[:,5])
                    flip_info_rfar[num_8,2]+=np.array([5]*len(num_8[0]),dtype=np.int)
                flip_info_rfar=np.array([l for l in flip_info_rfar if (l[1]<1100 and 0<l[2] and l[2]<1100)])
                print("flip_info_rfar={}".format(flip_info_rfar))

                if len(flip_info_lfar)>0:
                    #ペロペロキャンディの回転
                    num2=np.where(flip_info_lfar[:,0]==18)
                    num=np.where((11<=flip_info_lfar[:,0]) & (flip_info_lfar[:,0]<=17))
                    flip_info_lfar[num,0]+=np.array([1]*len(num[0]),dtype=np.int)
                    flip_info_lfar[num2,0]-=np.array([7]*len(num2[0]),dtype=np.int)
                    flip_info_lfar[num,2]+=np.array([5]*len(num[0]),dtype=np.int)
                    flip_info_lfar[num2,2]+=np.array([5]*len(num[0]),dtype=np.int)

                    flip_info_lfar[:,1]-=np.array([10]*len(flip_info_lfar),dtype=np.int)
                    #make parabola
                    num_9=np.where(flip_info_lfar[:,1]>flip_info_lfar[:,5])
                    flip_info_lfar[num_9,2]-=np.array([10]*len(num_9[0]),dtype=np.int)
                    num_6=np.where(flip_info_lfar[:,1]<flip_info_lfar[:,5])
                    flip_info_lfar[num_6,2]+=np.array([5]*len(num_6[0]),dtype=np.int)
                flip_info_lfar=np.array(([l for l in flip_info_lfar if (0<l[1] and 0<l[2] and l[2]<1100)]),dtype=np.int)
                print("flip_info_lfar={}".format(flip_info_lfar))

                #small candy
                if len(flip_info_r_s)>0:
                    flip_info_r_s[:,1]+=np.array([15]*len(flip_info_r_s),dtype=np.int)
                    #make parabola
                    num_3=np.where(flip_info_r_s[:,1]<flip_info_r_s[:,5])
                    flip_info_r_s[num_3,2]-=np.array([15]*len(num_3[0]),dtype=np.int)
                    num_4=np.where(flip_info_r_s[:,1]>flip_info_r_s[:,5])
                    flip_info_r_s[num_4,2]+=np.array([10]*len(num_4[0]),dtype=np.int)
                    #flip_info[:,2]=parabola(a=0.5,x_left=flip_info[:,1],y_up=flip_info[:,2],x_cen=flip_info[:,5],y_plus=10)
                flip_info_r_s=np.array([l for l in flip_info_r_s if (l[1]<1100 and 0<l[2] and l[2]<1100)])
                print("flip_info_r_s={}".format(flip_info_r_s))

                if len(flip_info_l_s)>0:
                    flip_info_l_s[:,1]-=np.array([15]*len(flip_info_l_s),dtype=np.int)
                    #make parabola
                    num_5=np.where(flip_info_l_s[:,1]>flip_info_l_s[:,5])
                    flip_info_l_s[num_5,2]-=np.array([15]*len(num_5[0]),dtype=np.int)
                    num_6=np.where(flip_info_l_s[:,1]<flip_info_l_s[:,5])
                    flip_info_l_s[num_6,2]+=np.array([10]*len(num_6[0]),dtype=np.int)
                flip_info_l_s=np.array([l for l in flip_info_l_s if (0<l[1] and 0<l[2] and l[2]<1100)])
                print("flip_info_l_s={}".format(flip_info_l_s))

                if len(flip_info_rfar_s)>0:
                    flip_info_rfar_s[:,1]+=np.array([15]*len(flip_info_rfar_s),dtype=np.int)
                    #make parabola
                    num_7=np.where(flip_info_rfar_s[:,1]<flip_info_rfar_s[:,5])
                    flip_info_rfar_s[num_7,2]-=np.array([10]*len(num_7[0]),dtype=np.int)
                    num_8=np.where(flip_info_rfar_s[:,1]>flip_info_rfar_s[:,5])
                    flip_info_rfar_s[num_8,2]+=np.array([5]*len(num_8[0]),dtype=np.int)
                flip_info_rfar_s=np.array([l for l in flip_info_rfar_s if (l[1]<1100 and 0<l[2] and l[2]<1100)])
                print("flip_info_rfar_s={}".format(flip_info_rfar_s))

                if len(flip_info_lfar_s)>0:
                    flip_info_lfar_s[:,1]-=np.array([15]*len(flip_info_lfar_s),dtype=np.int)
                    #make parabola
                    num_9=np.where(flip_info_lfar_s[:,1]>flip_info_lfar_s[:,5])
                    flip_info_lfar_s[num_9,2]-=np.array([10]*len(num_9[0]),dtype=np.int)
                    num_6=np.where(flip_info_lfar_s[:,1]<flip_info_lfar_s[:,5])
                    flip_info_lfar_s[num_6,2]+=np.array([5]*len(num_6[0]),dtype=np.int)
                flip_info_lfar_s=np.array(([l for l in flip_info_lfar_s if (0<l[1] and 0<l[2] and l[2]<1100)]),dtype=np.int)
                print("flip_info_lfar_s={}".format(flip_info_lfar_s))

                #remove fallen ame max:1100
                #rain flip
                if len(info)>0 and len(np.where(info[:,2]==1100)[0])>0:
                    num_rain=np.where(info[:,2]==1100)[0]
                    for m in num_rain:
                        if info[m][0]==0:
                            flip_rain_info=np.array(flip_rain_info)
                            flip_rain_info=flip_rain_info.tolist()
                            info[m][0]=4
                            flip_rain_info.append(info[m])

                if len(info)>0 and len(np.where(info[:,2]==1095)[0])>0:
                    num_rain=np.where(info[:,2]==1095)[0]
                    for m in num_rain:
                        if info[m][0]==25:
                            flip_rain_info=np.array(flip_rain_info)
                            flip_rain_info=flip_rain_info.tolist()
                            info[m][0]=4
                            flip_rain_info.append(info[m])


                info=np.array(([i for i in info if (i[2]<=1100 and i[1]<=1100)]),dtype=np.int)
                info=np.array(info)
                if len(info)>0:
                    info[:,2]+=np.array([10]*len(info),dtype=np.int)
                    #ペロペロキャンディの回転
                    num2=np.where(info[:,0]==18)
                    num=np.where((11<=info[:,0]) & (info[:,0]<=17))
                    info[num,0]+=np.array([1]*len(num[0]),dtype=np.int)
                    info[num,2]+=np.array([5]*len(num[0]),dtype=np.int)
                    info[num2,0]-=np.array([7]*len(num2[0]),dtype=np.int)
                    info[num2,2]+=np.array([5]*len(num2[0]),dtype=np.int)
                    #小さいあめ(candy)
                    num3=np.where(info[:,0]==2)
                    info[num3,2]+=np.array([5]*len(num3[0]),dtype=np.int)
                    #小さいあめ(rain)
                    num4=np.where(info[:,0]==25)
                    info[num4,2]+=np.array([5]*len(num4[0]),dtype=np.int)
                    info[num4,1]+=np.array([5]*len(num4[0]),dtype=np.int)
                print("info={}".format(info))


                img_1=ame_movie.Some2OnePicture('./images/sky.jpg',info)
                cv2.imwrite('./outputs/test_1201.jpg',img_1)
                img_2=ame_movie.Some2OnePicture('./outputs/test_1201.jpg',flip_info_r)
                cv2.imwrite('./outputs/test_1203.jpg',img_2)
                img_3=ame_movie.Some2OnePicture('./outputs/test_1203.jpg',flip_info_l)
                cv2.imwrite('./outputs/test_1207.jpg',img_3)
                img_4=ame_movie.Some2OnePicture('./outputs/test_1207.jpg',flip_info_rfar)
                cv2.imwrite('./outputs/test_1207_2.jpg',img_4)
                img_5=ame_movie.Some2OnePicture('./outputs/test_1207_2.jpg',flip_info_lfar)
                cv2.imwrite('./outputs/test_1207_3.jpg',img_5)
                img_6=ame_movie.Some2OnePicture('./outputs/test_1207_3.jpg',flip_rain_info)
                cv2.imwrite('./outputs/test_1210.jpg',img_6)
                img=ame_movie.Some2OnePicture('./outputs/test_1210.jpg',pakkun_list)
                cv2.imwrite('./outputs/test_1226_1.jpg',img)
                img=ame_movie.Some2OnePicture('./outputs/test_1226_1.jpg',flip_info_r_s)
                cv2.imwrite('./outputs/test_1226_2.jpg',img)
                img=ame_movie.Some2OnePicture('./outputs/test_1226_2.jpg',flip_info_l_s)
                cv2.imwrite('./outputs/test_1226_3.jpg',img)
                img=ame_movie.Some2OnePicture('./outputs/test_1226_3.jpg',flip_info_rfar_s)
                cv2.imwrite('./outputs/test_1226_4.jpg',img)
                img=ame_movie.Some2OnePicture('./outputs/test_1226_4.jpg',flip_info_lfar_s)
                img = cv2.resize(img, (640,480))

                cv2.imshow("result",img)
                end_time = pytime.time()
                elapsed_time = end_time - start_time # sec
                print(elapsed_time) # 100
                wait_time = max(200 - int(elapsed_time*1000), 1) # msec
                print(wait_time)
                if cv2.waitKey(wait_time) >= 0:
                    break
                j+=1
                if j==320:
                    flag=1
                    print("your point={}".format(point))
                    break
                if 3 in sound_list:
                    client.send_message("/filter", 3)
                    play_sound.play_sound('./sounds/flip_high.mp3',1)
                if 4 in sound_list:
                    client.send_message("/filter", 4)
                    play_sound.play_sound('./sounds/flip_low.mp3',1)
                if 1 in sound_list:
                    client.send_message("/filter", 1)
                    play_sound.play_sound('./sounds/flip_rain.mp3',1)
                if 2 in sound_list:
                    client.send_message("/filter", 2)
                    play_sound.play_sound('./sounds/paku.mp3',1)
                if 5 in sound_list:
                    client.send_message("./filter",11)
                    play_sound.play_sound('./sounds/gotsun.mp3',1)

        message_arrived=False
        rospy.sleep(0.1)

    game_result.game_result(point)

except rospy.ROSInterruptException:
    pass
