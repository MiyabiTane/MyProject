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

message_arrived=False
rospy.init_node('umbrella_pos')
rospy.Subscriber('/edgetpu_object_detector/output/rects',RectArray,position_cb)
while not rospy.is_shutdown() and flag==0:
    if message_arrived:
        print("message_arrived")
        #full screen
        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        um_pos_x=6000
        um_pos_y=6000
        fps = 25
        j=0
        point=0
        info=np.array([])
        flip_info_r=np.array([])
        flip_info_l=np.array([])
        flip_info_rfar=np.array([])
        flip_info_lfar=np.array([])
        pakkun_list=np.array([])
#------------------ゲームスタートorルール説明-------------------
        while True:
            um_pos_x=6000
            um_pos_y=6000
            break_flag=0
            #rects=[info1,info2...]
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

            info=[[0,140,600,500,500],[2,650,600,500,500]]

            if 200<um_pos_x and um_pos_x<340 and 1000<um_pos_y and um_pos_y<1100:
                info=[[1,140,600,500,500],[2,650,600,500,500]]
                break_flag=1 #次へ
            if 710<um_pos_x and um_pos_x<850 and 1000<um_pos_y and um_pos_y<1100:
                info=[[0,140,600,500,500],[3,650,600,500,500]]
                break_flag=2
                flag=1 #rule_explanation.py自体を抜ける

            img=ame_movie.RulePicture('./outputs/test_1223.jpg',info)
            img = cv2.resize(img, (640,480))
            cv2.imshow("result",img)

            if cv2.waitKey(20) >= 0:
                break
            if break_flag!=0:
                client.send_message("/filter", 10)
                play_sound.play_sound('./sounds/click.mp3',1)
                pytime.sleep(1)
                break

        if break_flag==2:
            continue
#--------あめを傘の真ん中で弾いてみよう--------------------------------------------------------
        break_flag=0
        #あめを１つ降らせる
        info=np.array([[1,580,0,140,140]])
        flip_rain_info=np.array([])

        while True:
            um_pos_x=6000
            um_pos_y=6000
            rule_list=[[2,0,500,300,300],[4,1000,500,300,300],[6,350,0,600,600]]
            start_time = pytime.time()
            sound_list=[]
            #rects=[info1,info2...]
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
                    if um_pos_x-70<=keep[1] and keep[1]<um_pos_x+140:
                    #x_center of parabola
                        keep.append(keep[1]+90)
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
                            flip_rain_info.append([10,max(keep[1]-20,0),max(keep[2]-180,0),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_r=flip_info_r.tolist()
                            flip_info_r.append(keep)
                            sound_list.append(3)

                    elif um_pos_x-280<=keep[1] and keep[1]<um_pos_x-70:
                        #x_centerof parabola
                        keep.append(keep[1]-90)
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
                            flip_rain_info.append([10,max(0,keep[1]-20),max(0,keep[2]-180),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_l=flip_info_l.tolist()
                            flip_info_l.append(keep)
                            sound_list.append(3)

                info=np.array(([l for l in info if l[4]!=0]),dtype=np.int)
                flip_info_r=np.array((flip_info_r),dtype=np.int)
                flip_info_l=np.array((flip_info_l),dtype=np.int)

            if len(flip_info_r)>0:
                flip_info_r[:,1]+=np.array([10]*len(flip_info_r),dtype=np.int)
                #make parabola
                num_3=np.where(flip_info_r[:,1]<flip_info_r[:,5])
                flip_info_r[num_3,2]-=np.array([20]*len(num_3[0]),dtype=np.int)
                num_4=np.where(flip_info_r[:,1]>flip_info_r[:,5])
                flip_info_r[num_4,2]+=np.array([10]*len(num_4[0]),dtype=np.int)
                #flip_info[:,2]=parabola(a=0.5,x_left=flip_info[:,1],y_up=flip_info[:,2],x_cen=flip_info[:,5],y_plus=10)
            flip_info_r=np.array([l for l in flip_info_r if (l[1]<1100 and 0<l[2] and l[2]<1100)])
            print("flip_info_r={}".format(flip_info_r))

            if len(flip_info_l)>0:
                flip_info_l[:,1]-=np.array([10]*len(flip_info_l),dtype=np.int)
                #make parabola
                num_5=np.where(flip_info_l[:,1]>flip_info_l[:,5])
                flip_info_l[num_5,2]-=np.array([20]*len(num_5[0]),dtype=np.int)
                num_6=np.where(flip_info_l[:,1]<flip_info_l[:,5])
                flip_info_l[num_6,2]+=np.array([10]*len(num_6[0]),dtype=np.int)
            flip_info_l=np.array([l for l in flip_info_l if (0<l[1] and 0<l[2] and l[2]<1100)])
            print("flip_info_l={}".format(flip_info_l))

            info=np.array(([i for i in info if i[2]<=1100]),dtype=np.int)
            info=np.array(info)
            if len(info)>0:
                info[:,2]+=np.array([10]*len(info),dtype=np.int)
            print("info={}".format(info))

            #ボタンが押されたら
            if 50<um_pos_x and um_pos_x<200 and 700<um_pos_y and um_pos_y<800:
                rule_list=[[3,0,500,300,300],[4,1000,500,300,300]]
                break_flag=2
                flag=1 #ルール説明自体を抜ける。
            elif 1050<um_pos_x and um_pos_x<1200 and 700<um_pos_y and um_pos_y<800:
                rule_list=[[2,0,500,300,300],[5,1000,500,300,300]]
                break_flag=1

            img_1=ame_movie.Some2OnePicture('./images/sky.jpg',info)
            cv2.imwrite('./outputs/test_1224_1.jpg',img_1)
            img_2=ame_movie.Some2OnePicture('./outputs/test_1224_1.jpg',flip_info_r)
            cv2.imwrite('./outputs/test_1224_2.jpg',img_2)
            img_3=ame_movie.Some2OnePicture('./outputs/test_1224_2.jpg',flip_info_l)
            cv2.imwrite('./outputs/test_1224_3.jpg',img_3)
            img=ame_movie.RulePicture('./outputs/test_1224_3.jpg',rule_list)
            img = cv2.resize(img, (640,480))

            cv2.imshow("result",img)
            end_time = pytime.time()
            elapsed_time = end_time - start_time # sec
            print(elapsed_time) # 100
            wait_time = max(200 - int(elapsed_time*1000), 1) # msec
            print(wait_time)
            if cv2.waitKey(wait_time) >= 0:
                break

            if 3 in sound_list:
                client.send_message("/filter", 3)
                play_sound.play_sound('./sounds/flip_high.mp3',1)
            if break_flag!=0:
                client.send_message("/filter",10)
                play_sound.play_sound('./sounds/click.mp3',1)
                pytime.sleep(1)
                break
            if len(info)==0 and len(flip_info_l)==0 and len(flip_info_r)==0:
                info=np.array(info)
                info=info.tolist()
                info.append([1,580,0,140,140])
                info=np.array(info)

        if break_flag==2:
            continue
#--------------あめを傘の端っこで弾いてみよう-----------
        break_flag=0
        #あめを１つ降らせる
        info=np.array([[1,580,0,140,140]])
        flip_rain_info=np.array([])

        while True:
            um_pos_x=6000
            um_pos_y=6000
            start_time = pytime.time()
            sound_list=[]
            rule_list=[[2,0,500,300,300],[4,1000,500,300,300],[7,350,0,600,600]]
            #rects=[info1,info2...]
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

            # think the relationship with umbrella
            if len(info)>0 and len(np.where((um_pos_y-50<info[:,2]) & (info[:,2]<um_pos_y+50))[0])>0:
                #remove candy from info
                num_f=np.where((um_pos_y-50<info[:,2]) & (info[:,2]<um_pos_y+50))[0]
                for m in range(len(num_f)):
                    keep=info[num_f[m]]
                    keep=np.array(keep)
                    keep=keep.tolist()
                    if um_pos_x+140<=keep[1] and keep[1]<um_pos_x+280:
                        #x_centerof parabola
                        keep.append(keep[1]+110)
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
                            flip_rain_info.append([10,max(0,keep[1]-20),max(0,keep[2]-180),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_rfar=flip_info_rfar.tolist()
                            flip_info_rfar.append(keep)
                            sound_list.append(4)

                    elif um_pos_x-420<=keep[1] and keep[1]<um_pos_x-280:
                        #x_centerof parabola
                        keep.append(keep[1]-110)
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
                            flip_rain_info.append([10,max(keep[1]-20,0),max(0,keep[2]-180),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_lfar=flip_info_lfar.tolist()
                            flip_info_lfar.append(keep)
                            sound_list.append(4)

                info=np.array(([l for l in info if l[4]!=0]),dtype=np.int)
                flip_info_rfar=np.array((flip_info_rfar),dtype=np.int)
                flip_info_lfar=np.array((flip_info_lfar),dtype=np.int)
                flip_rain_info=np.array((flip_rain_info),dtype=np.int)
            print("flip_rain_info={}".format(flip_rain_info))

            if len(flip_info_rfar)>0:
                flip_info_rfar[:,1]+=np.array([10]*len(flip_info_rfar),dtype=np.int)
                #make parabola
                num_7=np.where(flip_info_rfar[:,1]<flip_info_rfar[:,5])
                flip_info_rfar[num_7,2]-=np.array([10]*len(num_7[0]),dtype=np.int)
                num_8=np.where(flip_info_rfar[:,1]>flip_info_rfar[:,5])
                flip_info_rfar[num_8,2]+=np.array([5]*len(num_8[0]),dtype=np.int)
            flip_info_rfar=np.array([l for l in flip_info_rfar if (l[1]<1100 and 0<l[2] and l[2]<1100)])
            print("flip_info_rfar={}".format(flip_info_rfar))

            if len(flip_info_lfar)>0:
                flip_info_lfar[:,1]-=np.array([10]*len(flip_info_lfar),dtype=np.int)
                #make parabola
                num_9=np.where(flip_info_lfar[:,1]>flip_info_lfar[:,5])
                flip_info_lfar[num_9,2]-=np.array([10]*len(num_9[0]),dtype=np.int)
                num_6=np.where(flip_info_lfar[:,1]<flip_info_lfar[:,5])
                flip_info_lfar[num_6,2]+=np.array([5]*len(num_6[0]),dtype=np.int)
            flip_info_lfar=np.array(([l for l in flip_info_lfar if (0<l[1] and 0<l[2] and l[2]<1100)]),dtype=np.int)
            print("flip_info_lfar={}".format(flip_info_lfar))

            info=np.array(([i for i in info if i[2]<=1100]),dtype=np.int)
            info=np.array(info)
            if len(info)>0:
                info[:,2]+=np.array([10]*len(info),dtype=np.int)
            print("info={}".format(info))

            #ボタンが押されたら
            if 50<um_pos_x and um_pos_x<200 and 700<um_pos_y and um_pos_y<800:
                rule_list=[[3,0,500,300,300],[4,1000,500,300,300]]
                break_flag=2
                flag=1 #ルール説明自体を抜ける。
            elif 1050<um_pos_x and um_pos_x<1200 and 700<um_pos_y and um_pos_y<800:
                rule_list=[[2,0,500,300,300],[5,1000,500,300,300]]
                break_flag=1

            img_1=ame_movie.Some2OnePicture('./images/sky.jpg',info)
            cv2.imwrite('./outputs/test_1224_01.jpg',img_1)
            img_2=ame_movie.Some2OnePicture('./outputs/test_1224_01.jpg',flip_info_rfar)
            cv2.imwrite('./outputs/test_1224_02.jpg',img_2)
            img_3=ame_movie.Some2OnePicture('./outputs/test_1224_02.jpg',flip_info_lfar)
            cv2.imwrite('./outputs/test_1224_03.jpg',img_3)
            img=ame_movie.RulePicture('./outputs/test_1224_03.jpg',rule_list)
            img = cv2.resize(img, (640,480))

            cv2.imshow("result",img)
            end_time = pytime.time()
            elapsed_time = end_time - start_time # sec
            print(elapsed_time) # 100
            wait_time = max(200 - int(elapsed_time*1000), 1) # msec
            print(wait_time)
            if cv2.waitKey(wait_time) >= 0:
                break

            if break_flag!=0:
                client.send_message("/filter",10)
                play_sound.play_sound('./sounds/click.mp3',1)
                pytime.sleep(1)
                break
            if 4 in sound_list:
                client.send_message("/filter", 4)
                play_sound.play_sound('./sounds/flip_low.mp3',1)

            if len(info)==0 and len(flip_info_rfar)==0 and len(flip_info_lfar)==0:
                info=np.array(info)
                info=info.tolist()
                info.append([1,580,0,140,140])
                info=np.array(info)

        if break_flag==2:
            continue
#--------------ゴールにいれてみよう-----------------
        break_flag=0
        #あめを１つ降らせる
        info=np.array([[1,580,0,140,140]])
        flip_rain_info=np.array([])
        flip_info_r=np.array([])
        flip_info_l=np.array([])
        flip_info_rfar=np.array([])
        flip_info_lfar=np.array([])
        pakkun_list=np.array([])

        j=0
        while True:
            um_pos_x=6000
            um_pos_y=6000
            if j%4==0 or j%4==1:
                rule_list=[[2,0,200,300,300],[4,1000,200,300,300],[8,350,0,600,600],[9,1050,550,250,250],[9,0,550,250,250]]
            else:
                rule_list=[[2,0,200,300,300],[4,1000,200,300,300],[8,350,0,600,600],[9,1050,500,250,250],[9,0,500,250,250]]
            flip_rain_info=np.array([])
            pakkun_list=np.array([[5,900,800,400,400],[6,0,800,400,400]])
            start_time = pytime.time()
            sound_list=[]

            #rects=[info1,info2...]
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

            #pakkun goal
            if len(flip_info_r)>0 and len(np.where((800<=flip_info_r[:,2]) & (flip_info_r[:,2]<=1000))[0])>0:
                num_g=np.where((800<=flip_info_r[:,2]) & (flip_info_r[:,2]<=1000))[0]
                for k in num_g:
                    keep=flip_info_r[k]
                    keep=keep.tolist()
                    if 930<=keep[1] and keep[1]<=1130:
                        pakkun_list=np.array(pakkun_list)
                        pakkun_list=pakkun_list.tolist()
                        pakkun_list.append([7,900,800,400,400])
                        pakkun_list.append([9,900,720,180,180])
                        flip_info_r[k][4]=0
                        pakkun_list=np.array(pakkun_list)
                        point+=2
                        sound_list.append(2)

                flip_info_r=np.array(([l for l in flip_info_r if l[4]!=0]),dtype=np.int)


            if len(flip_info_rfar)>0 and len(np.where((800<=flip_info_rfar[:,2]) & (flip_info_rfar[:,2]<=1000))[0])>0:
                num_g=np.where((800<=flip_info_rfar[:,2]) & (flip_info_rfar[:,2]<=1000))[0]
                for k in num_g:
                    keep=flip_info_rfar[k]
                    keep=keep.tolist()
                    if 930<=keep[1] and keep[1]<=1130:
                        pakkun_list=np.array(pakkun_list)
                        pakkun_list=pakkun_list.tolist()
                        pakkun_list.append([7,900,800,400,400])
                        pakkun_list.append([9,900,720,180,180])
                        flip_info_rfar[k][4]=0
                        pakkun_list=np.array(pakkun_list)
                        point+=2
                        sound_list.append(2)
                flip_info_rfar=np.array(([l for l in flip_info_rfar if l[4]!=0]),dtype=np.int)


            if len(flip_info_l)>0 and len(np.where((800<=flip_info_l[:,2]) & (flip_info_l[:,2]<=1000))[0])>0:
                num_g=np.where((800<=flip_info_l[:,2]) & (flip_info_l[:,2]<=1000))[0]
                for k in num_g:
                    keep=flip_info_l[k]
                    keep=keep.tolist()
                    if 30<=keep[1] and keep[1]<=230:
                        pakkun_list=np.array(pakkun_list)
                        pakkun_list=pakkun_list.tolist()
                        pakkun_list.append([8,0,800,400,400])
                        pakkun_list.append([9,220,720,180,180])
                        flip_info_l[k][4]=0
                        pakkun_list=np.array(pakkun_list)
                        point+=2
                        sound_list.append(2)
                flip_info_l=np.array(([l for l in flip_info_l if l[4]!=0]),dtype=np.int)

            if len(flip_info_lfar)>0 and len(np.where((800<=flip_info_lfar[:,2]) & (flip_info_lfar[:,2]<=1000))[0])>0:
                num_g=np.where((800<=flip_info_lfar[:,2]) & (flip_info_lfar[:,2]<=1000))[0]
                for k in num_g:
                    keep=flip_info_lfar[k]
                    keep=keep.tolist()
                    if 30<=keep[1] and keep[1]<=230:
                        pakkun_list=np.array(pakkun_list)
                        pakkun_list=pakkun_list.tolist()
                        pakkun_list.append([8,0,800,400,400])
                        pakkun_list.append([9,220,700,180,180])
                        flip_info_lfar[k][4]=0
                        pakkun_list=np.array(pakkun_list)
                        point+=2
                        sound_list.append(2)
                flip_info_lfar=np.array(([l for l in flip_info_lfar if l[4]!=0]),dtype=np.int)

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
                    if um_pos_x-70<=keep[1] and keep[1]<um_pos_x+140:
                    #x_center of parabola
                        keep.append(keep[1]+90)
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
                            flip_rain_info.append([10,max(keep[1]-20,0),max(keep[2]-180,0),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_r=flip_info_r.tolist()
                            flip_info_r.append(keep)
                            sound_list.append(3)

                    elif um_pos_x-280<=keep[1] and keep[1]<um_pos_x-70:
                        #x_centerof parabola
                        keep.append(keep[1]-90)
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
                            flip_rain_info.append([10,max(0,keep[1]-20),max(0,keep[2]-180),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_l=flip_info_l.tolist()
                            flip_info_l.append(keep)
                            sound_list.append(3)

                    elif um_pos_x+140<=keep[1] and keep[1]<um_pos_x+280:
                        #x_centerof parabola
                        keep.append(keep[1]+110)
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
                            flip_rain_info.append([10,max(0,keep[1]-20),max(0,keep[2]-180),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_rfar=flip_info_rfar.tolist()
                            flip_info_rfar.append(keep)
                            sound_list.append(4)

                    elif um_pos_x-420<=keep[1] and keep[1]<um_pos_x-280:
                        #x_centerof parabola
                        keep.append(keep[1]-110)
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
                            flip_rain_info.append([10,max(keep[1]-20,0),max(0,keep[2]-180),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_lfar=flip_info_lfar.tolist()
                            flip_info_lfar.append(keep)
                            sound_list.append(4)

                info=np.array(([l for l in info if l[4]!=0]),dtype=np.int)
                flip_info_r=np.array((flip_info_r),dtype=np.int)
                flip_info_l=np.array((flip_info_l),dtype=np.int)
                flip_info_rfar=np.array((flip_info_rfar),dtype=np.int)
                flip_info_lfar=np.array((flip_info_lfar),dtype=np.int)
                flip_rain_info=np.array((flip_rain_info),dtype=np.int)
            print("flip_rain_info={}".format(flip_rain_info))

            if len(flip_info_r)>0:
                flip_info_r[:,1]+=np.array([10]*len(flip_info_r),dtype=np.int)
                #make parabola
                num_3=np.where(flip_info_r[:,1]<flip_info_r[:,5])
                flip_info_r[num_3,2]-=np.array([20]*len(num_3[0]),dtype=np.int)
                num_4=np.where(flip_info_r[:,1]>flip_info_r[:,5])
                flip_info_r[num_4,2]+=np.array([10]*len(num_4[0]),dtype=np.int)
                #flip_info[:,2]=parabola(a=0.5,x_left=flip_info[:,1],y_up=flip_info[:,2],x_cen=flip_info[:,5],y_plus=10)
            flip_info_r=np.array([l for l in flip_info_r if (l[1]<1100 and 0<l[2] and l[2]<1100)])
            print("flip_info_r={}".format(flip_info_r))

            if len(flip_info_l)>0:
                flip_info_l[:,1]-=np.array([10]*len(flip_info_l),dtype=np.int)
                #make parabola
                num_5=np.where(flip_info_l[:,1]>flip_info_l[:,5])
                flip_info_l[num_5,2]-=np.array([20]*len(num_5[0]),dtype=np.int)
                num_6=np.where(flip_info_l[:,1]<flip_info_l[:,5])
                flip_info_l[num_6,2]+=np.array([10]*len(num_6[0]),dtype=np.int)
            flip_info_l=np.array([l for l in flip_info_l if (0<l[1] and 0<l[2] and l[2]<1100)])
            print("flip_info_l={}".format(flip_info_l))

            if len(flip_info_rfar)>0:
                flip_info_rfar[:,1]+=np.array([10]*len(flip_info_rfar),dtype=np.int)
                #make parabola
                num_7=np.where(flip_info_rfar[:,1]<flip_info_rfar[:,5])
                flip_info_rfar[num_7,2]-=np.array([10]*len(num_7[0]),dtype=np.int)
                num_8=np.where(flip_info_rfar[:,1]>flip_info_rfar[:,5])
                flip_info_rfar[num_8,2]+=np.array([5]*len(num_8[0]),dtype=np.int)
            flip_info_rfar=np.array([l for l in flip_info_rfar if (l[1]<1100 and 0<l[2] and l[2]<1100)])
            print("flip_info_rfar={}".format(flip_info_rfar))

            if len(flip_info_lfar)>0:
                flip_info_lfar[:,1]-=np.array([10]*len(flip_info_lfar),dtype=np.int)
                #make parabola
                num_9=np.where(flip_info_lfar[:,1]>flip_info_lfar[:,5])
                flip_info_lfar[num_9,2]-=np.array([10]*len(num_9[0]),dtype=np.int)
                num_6=np.where(flip_info_lfar[:,1]<flip_info_lfar[:,5])
                flip_info_lfar[num_6,2]+=np.array([5]*len(num_6[0]),dtype=np.int)
            flip_info_lfar=np.array(([l for l in flip_info_lfar if (0<l[1] and 0<l[2] and l[2]<1100)]),dtype=np.int)
            print("flip_info_lfar={}".format(flip_info_lfar))

            info=np.array(([i for i in info if i[2]<=1100]),dtype=np.int)
            info=np.array(info)
            if len(info)>0:
                info[:,2]+=np.array([10]*len(info),dtype=np.int)
            print("info={}".format(info))

            #ボタンが押されたら
            if 50<um_pos_x and um_pos_x<200 and 400<um_pos_y and um_pos_y<500:
                rule_list=[[3,0,200,300,300],[4,1000,200,300,300],[8,350,0,600,600],[9,1050,500,250,250],[9,0,500,250,250]]
                break_flag=2
                flag=1 #ルール説明自体を抜ける。
            elif 1050<um_pos_x and um_pos_x<1200 and 400<um_pos_y and um_pos_y<500:
                rule_list=[[2,0,200,300,300],[5,1000,200,300,300],[8,350,0,600,600],[9,1050,500,250,250],[9,0,500,250,250]]
                break_flag=1

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
            img_6=ame_movie.RulePicture('./outputs/test_1207_3.jpg',rule_list)
            cv2.imwrite('./outputs/test_1210.jpg',img_6)
            img=ame_movie.Some2OnePicture('./outputs/test_1210.jpg',pakkun_list)
            img = cv2.resize(img, (640,480))

            cv2.imshow("result",img)
            end_time = pytime.time()
            elapsed_time = end_time - start_time # sec
            print(elapsed_time) # 100
            wait_time = max(200 - int(elapsed_time*1000), 1) # msec
            print(wait_time)
            if cv2.waitKey(wait_time) >= 0:
                break

            if break_flag!=0:
                client.send_message("/filter",10)
                play_sound.play_sound('./sounds/click.mp3',1)
                pytime.sleep(1)
                break
            if 3 in sound_list:
                client.send_message("/filter", 3)
                play_sound.play_sound('./sounds/flip_high.mp3',1)
            if 4 in sound_list:
                client.send_message("/filter", 4)
                play_sound.play_sound('./sounds/flip_low.mp3',1)
            if 2 in sound_list:
                client.send_message("/filter", 2)
                play_sound.play_sound('./sounds/paku.mp3',1)

            if len(info)==0:
                info=info.tolist()
                info.append([1,580,0,140,140])
                info=np.array(info)
            j+=1

        if break_flag==2:
            continue
#--------------雨粒を弾いてみよう-------------------
        break_flag=0
        #雨粒を１つ降らせる
        info=np.array([[0,580,0,140,140]])
        flip_rain_info=np.array([])
        flip_info_r=np.array([])
        flip_info_l=np.array([])
        flip_info_rfar=np.array([])
        flip_info_lfar=np.array([])

        while True:
            um_pos_x=6000
            um_pos_y=6000
            flip_rain_info=np.array([])
            start_time = pytime.time()
            sound_list=[]
            rule_list=[[2,0,500,300,300],[4,1000,500,300,300],[10,350,0,600,600]]

            #rects=[info1,info2...]
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

            # think the relationship with umbrella
            if len(info)>0 and len(np.where((um_pos_y-50<info[:,2]) & (info[:,2]<um_pos_y+50))[0])>0:
                #remove candy from info
                num_f=np.where((um_pos_y-50<info[:,2]) & (info[:,2]<um_pos_y+50))[0]
                for m in range(len(num_f)):
                    keep=info[num_f[m]]
                    keep=np.array(keep)
                    keep=keep.tolist()
                    if um_pos_x-70<=keep[1] and keep[1]<um_pos_x+140:
                    #x_center of parabola
                        keep.append(keep[1]+90)
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
                            flip_rain_info.append([10,max(keep[1]-20,0),max(keep[2]-180,0),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_r=flip_info_r.tolist()
                            flip_info_r.append(keep)
                            sound_list.append(3)

                    elif um_pos_x-280<=keep[1] and keep[1]<um_pos_x-70:
                        #x_centerof parabola
                        keep.append(keep[1]-90)
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
                            flip_rain_info.append([10,max(0,keep[1]-20),max(0,keep[2]-180),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_l=flip_info_l.tolist()
                            flip_info_l.append(keep)
                            sound_list.append(3)

                    elif um_pos_x+140<=keep[1] and keep[1]<um_pos_x+280:
                        #x_centerof parabola
                        keep.append(keep[1]+110)
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
                            flip_rain_info.append([10,max(0,keep[1]-20),max(0,keep[2]-180),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_rfar=flip_info_rfar.tolist()
                            flip_info_rfar.append(keep)
                            sound_list.append(4)

                    elif um_pos_x-420<=keep[1] and keep[1]<um_pos_x-280:
                        #x_centerof parabola
                        keep.append(keep[1]-110)
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
                            flip_rain_info.append([10,max(keep[1]-20,0),max(0,keep[2]-180),180,180,0])
                            point-=1
                            sound_list.append(1)
                        else:
                            flip_info_lfar=flip_info_lfar.tolist()
                            flip_info_lfar.append(keep)
                            sound_list.append(4)

                info=np.array(([l for l in info if l[4]!=0]),dtype=np.int)
                flip_info_r=np.array((flip_info_r),dtype=np.int)
                flip_info_l=np.array((flip_info_l),dtype=np.int)
                flip_info_rfar=np.array((flip_info_rfar),dtype=np.int)
                flip_info_lfar=np.array((flip_info_lfar),dtype=np.int)
                flip_rain_info=np.array((flip_rain_info),dtype=np.int)
            print("flip_rain_info={}".format(flip_rain_info))
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

            info=np.array(([i for i in info if i[2]<=1100]),dtype=np.int)
            info=np.array(info)
            if len(info)>0:
                info[:,2]+=np.array([10]*len(info),dtype=np.int)
            print("info={}".format(info))

            #ボタンが押されたら
            if 50<um_pos_x and um_pos_x<200 and 700<um_pos_y and um_pos_y<800:
                rule_list=[[3,0,500,300,300],[4,1000,500,300,300],[10,350,0,600,600]]
                break_flag=2
                flag=1 #ルール説明自体を抜ける。
            elif 1050<um_pos_x and um_pos_x<1200 and 700<um_pos_y and um_pos_y<800:
                rule_list=[[2,0,500,300,300],[5,1000,500,300,300],[10,350,0,600,600]]
                break_flag=1

            img_1=ame_movie.Some2OnePicture('./images/sky.jpg',info)
            cv2.imwrite('./outputs/test_1224_001.jpg',img_1)
            img_2=ame_movie.Some2OnePicture('./outputs/test_1224_001.jpg',flip_rain_info)
            cv2.imwrite('./outputs/test_1224_002.jpg',img_2)
            img=ame_movie.RulePicture('./outputs/test_1224_002.jpg',rule_list)
            img = cv2.resize(img, (640,480))

            cv2.imshow("result",img)
            end_time = pytime.time()
            elapsed_time = end_time - start_time # sec
            print(elapsed_time) # 100
            wait_time = max(200 - int(elapsed_time*1000), 1) # msec
            print(wait_time)
            if cv2.waitKey(wait_time) >= 0:
                break

            if break_flag!=0:
                client.send_message("/filter",10)
                play_sound.play_sound('./sounds/click.mp3',1)
                pytime.sleep(1)
                break

            if 1 in sound_list:
                client.send_message("/filter", 1)
                play_sound.play_sound('./sounds/flip_rain.mp3',1)

            if len(info)==0:
                info=info.tolist()
                info.append([0,580,0,140,140])
                info=np.array(info)

        if break_flag==2:
            continue
#---------------------------------------------
        count=0
        while count<8:
            if count%2==0:
                info=[[11,350,100,600,600]]
            else:
                info=[[11,350,100,600,600],[12,150,380,250,250],[13,900,100,250,250]]

            img=ame_movie.RulePicture('./images/sky.jpg',info)
            img = cv2.resize(img, (640,480))

            cv2.imshow("result",img)
            if cv2.waitKey(500) >= 0:
                break
            count+=1

    message_arrived=False
    rospy.sleep(0.1)
