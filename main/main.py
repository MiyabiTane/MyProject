import rospy
from jsk_recognition_msgs.msg import RectArray
from jsk_recognition_msgs.msg import Rect
import numpy as np
import ame_movie
import cv2
import random
import time as pytime

global flag
flag=0
message_arrived=False
def position_cb(msg):
    global message_arrived
    message_arrived=msg

if __name__=='__main__':
    try:
        message_arrived=False
        rospy.init_node('umbrella_pos')
        rospy.Subscriber('/edgetpu_object_detector/output/rects',RectArray,position_cb)
        while not rospy.is_shutdown() and flag==0:
            if message_arrived:
                print("message_arrived")

                #full screen
                #cv2.namedWindow('result', cv2.WINDOW_NORMAL)
                #cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                #make ame
                time=np.random.randint(0,250,20)
                x_left=np.random.randint(100,1000,len(time))
                #x_left=[500]*len(time)
                #pitch candy:rain
                images=np.random.randint(0,3,len(time))
                size=np.zeros((len(time),2))
                size[np.where(images==0)]=[140,140]
                size[np.where(images!=0)]=[140,140]
                fall_obs=[]
                #info of each ame
                for i in range(len(time)):
                    fall_obs.append([images[i],x_left[i],0,size[i][0],size[i][1]])

                um_pos_x=6000
                um_pos_y=6000
                fps = 25
                j=0
                info=np.array([])
                flip_info_r=np.array([])
                flip_info_l=np.array([])
                flip_info_rfar=np.array([])
                flip_info_lfar=np.array([])

                while True:
                    print("j={}".format(j))
                    flip_rain_info=np.array([])
                    start_time = pytime.time()

                    #rects=[info1,info2...]
                    if len(message_arrived.rects)>0:
                        x_min=10000
                        umb_index=100
                        #umbrella's x is min
                        for i in range(len(message_arrived.rects)):
                            #umbrella : 150<width<200 y~=115
                            if message_arrived.rects[i].x<x_min and message_arrived.rects[i].height<150:
                                umb_index=i
                                x_min=message_arrived.rects[i].x
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

                    #flip again
                    #right right
                    if len(flip_info_r)>0 and len(np.where((um_pos_y-50<flip_info_r[:,2]) & (flip_info_r[:,2]<um_pos_y+50))[0])>0:
                        num_fr=np.where((um_pos_y-50<flip_info_r[:,2]) & (flip_info_r[:,2]<um_pos_y+50))[0]
                        for k in range(len(num_fr)):
                            keep=flip_info_r[num_fr[k]]
                            keep=keep.tolist()
                            if um_pos_x-70<=flip_info_r[k][1] and flip_info_r[k][1]<um_pos_x+140:
                                keep[5]=keep[1]+100
                                flip_info_r=np.array(flip_info_r)
                                flip_info_r=flip_info_r.tolist()
                                flip_info_r.pop(num_fr[k])
                                flip_info_r.append(keep)
                                flip_info_r=np.array(flip_info_r)

                    #right left
                    if len(flip_info_r)>0 and len(np.where((um_pos_y-50<flip_info_r[:,2]) & (flip_info_r[:,2]<um_pos_y+50))[0])>0:
                        num_fr=np.where((um_pos_y-50<flip_info_r[:,2]) & (flip_info_r[:,2]<um_pos_y+50))[0]
                        for k in range(len(num_fr)):
                            keep=flip_info_r[num_fr[k]]
                            keep=keep.tolist()
                            if um_pos_x-280<=flip_info_r[k][1] and flip_info_r[k][1]<um_pos_x-70:
                                keep[5]=keep[1]-100
                                flip_info_r=np.array(flip_info_r)
                                flip_info_r=flip_info_r.tolist()
                                flip_info_r.pop(num_fr[k])
                                flip_info_l=np.array(flip_info_l)
                                flip_info_l=flip_info_l.tolist()
                                flip_info_l.append(keep)
                                flip_info_r=np.array(flip_info_r)
                                flip_info_l=np.array(flip_info_l)

                    #left left
                    if len(flip_info_l)>0 and len(np.where((um_pos_y-50<flip_info_l[:,2]) & (flip_info_l[:,2]<um_pos_y+50))[0])>0:
                        num_fl=np.where((um_pos_y-50<flip_info_l[:,2]) & (flip_info_l[:,2]<um_pos_y+50))[0]
                        for k in range(len(num_fl)):
                            keep=flip_info_l[num_fl[k]]
                            keep=keep.tolist()
                            if um_pos_x-280<=flip_info_l[k][1] and flip_info_l[k][1]<um_pos_x-70:
                                keep[5]=keep[1]-100
                                flip_info_l=np.array(flip_info_l)
                                flip_info_l=flip_info_l.tolist()
                                flip_info_l.pop(num_fl[k])
                                flip_info_l.append(keep)
                                flip_info_l=np.array(flip_info_l)

                    #left right
                    if len(flip_info_l)>0 and len(np.where((um_pos_y-50<flip_info_l[:,2]) & (flip_info_l[:,2]<um_pos_y+50))[0])>0:
                        num_fl=np.where((um_pos_y-50<flip_info_l[:,2]) & (flip_info_l[:,2]<um_pos_y+50))[0]
                        for k in range(len(num_fl)):
                            keep=flip_info_l[num_fl[k]]
                            keep=keep.tolist()
                            if um_pos_x-70<=flip_info_l[k][1] and flip_info_l[k][1]<um_pos_x+140:
                                keep[5]=keep[1]+100
                                flip_info_l=np.array(flip_info_l)
                                flip_info_l=flip_info_l.tolist()
                                flip_info_l.pop(num_fl[k])
                                flip_info_r=np.array(flip_info_r)
                                flip_info_r=flip_info_r.tolist()
                                flip_info_l.append(keep)
                                flip_info_r=np.array(flip_info_r)
                                flip_info_l=np.array(flip_info_l)

                    # think the relationship with umbrella
                    if len(info)>0 and len(np.where((um_pos_y-50<info[:,2]) & (info[:,2]<um_pos_y+50))[0])>0:
                        #remove candy from info
                        num_f=np.where((um_pos_y-50<info[:,2]) & (info[:,2]<um_pos_y+50))[0]
                        for m in range(len(num_f)):
                            keep=info[num_f[m]]
                            keep=keep.tolist()
                            if um_pos_x-70<=keep[1] and keep[1]<um_pos_x+140:
                            #x_center of parabola
                                keep.append(keep[1]+100)
                                info=info.tolist()
                                info.pop(num_f[m])
                                info=np.array(info)
                                #add candy to flip_info
                                flip_info_r=np.array(flip_info_r)
                                flip_rain_info=np.array(flip_rain_info)
                                #candy only
                                if keep[0]==0:
                                    keep[0]=4
                                    flip_rain_info=flip_rain_info.tolist()
                                    flip_rain_info.append(keep)
                                else:
                                    flip_info_r=flip_info_r.tolist()
                                    flip_info_r.append(keep)

                            elif um_pos_x-280<=keep[1] and keep[1]<um_pos_x-70:
                                #x_centerof parabola
                                keep.append(keep[1]-100)
                                info=info.tolist()
                                info.pop(num_f[m])
                                info=np.array(info)
                                #add candy to flip info
                                flip_info_l=np.array(flip_info_l)
                                flip_rain_info=np.array(flip_rain_info)
                                #candy only
                                if keep[0]==0:
                                    keep[0]=4
                                    flip_rain_info=flip_rain_info.tolist()
                                    flip_rain_info.append(keep)
                                else:
                                    flip_info_l=flip_info_l.tolist()
                                    flip_info_l.append(keep)

                            elif um_pos_x+140<=keep[1] and keep[1]<um_pos_x+280:
                                #x_centerof parabola
                                keep.append(keep[1]+120)
                                info=info.tolist()
                                info.pop(num_f[m])
                                info=np.array(info)
                                #to avoid error list.tolist()
                                flip_rain_info=np.array(flip_rain_info)
                                flip_info_rfar=np.array(flip_info_rfar)
                                #add candy to flip info
                                #candy only
                                if keep[0]==0:
                                    keep[0]=4
                                    flip_rain_info=flip_rain_info.tolist()
                                    flip_rain_info.append(keep)
                                else:
                                    flip_info_rfar=flip_info_rfar.tolist()
                                    flip_info_rfar.append(keep)

                            elif um_pos_x-420<=keep[1] and keep[1]<um_pos_x-280:
                                #x_centerof parabola
                                keep.append(keep[1]-120)
                                info=info.tolist()
                                info.pop(num_f[m])
                                info=np.array(info)
                                #add candy to flip info
                                flip_info_lfar=np.array(flip_info_lfar)
                                flip_rain_info=np.array(flip_rain_info)
                                #candy only
                                if keep[0]==0:
                                    keep[0]=4
                                    flip_rain_info=flip_rain_info.tolist()
                                    flip_rain_info.append(keep)
                                else:
                                    flip_info_lfar=flip_info_lfar.tolist()
                                    flip_info_lfar.append(keep)


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
                    img=ame_movie.Some2OnePicture('./outputs/test_1207_3.jpg',flip_rain_info)
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
                    if j==300:
                        flag=1
                        break

            message_arrived=False
            rospy.sleep(0.1)

    except rospy.ROSInterruptException:
        pass
