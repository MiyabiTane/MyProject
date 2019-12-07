import cv2
import numpy as np
import random
import time as pytime

#base_img->.jpg,small_img->.png
#info=[alpha_img,x_left,y_up,wid,hei]
#base_img -> 1300*1300
def Some2OnePicture(base_img,info):
    start=pytime.time()
    dst=cv2.imread(base_img)
    #print("size={}".format(dst.shape))
    src=[0]*len(info)
    mask=[0]*len(info)
    width=[0]*len(info)
    height=[0]*len(info)
    for i in range(len(info)):
        if info[i][0]==0:
            alpha_image='./images/rain.png'
        elif info[i][0]==4:
            alpha_image='./images/flip_rain.png'
        else:
            alpha_image='./images/candy.png'
        src[i]=cv2.imread(alpha_image,-1)
        src[i]=cv2.resize(src[i],dsize=(int(info[i][3]),int(info[i][4])))
        width[i], height[i] = src[i].shape[:2]

        mask[i] = src[i][:,:,3]  # get only alpha
        mask[i]=np.tile(mask[i][:,:,np.newaxis],(1,1,3))
        #mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)  # change to 3 colors
        mask[i] = mask[i] / 255.0  # 0-255->0.0-1.0
        mask[i]=mask[i].astype(np.uint8)
        src[i] = src[i][:,:,:3]  # remove alpha channel
        #print("width={},height={},mask={}".format(width[i],height[i],mask[i].shape))
        dst[int(info[i][2]):int(info[i][2]+height[i]),int(info[i][1]):int(info[i][1]+width[i])] *= 1 - mask[i]
        dst[int(info[i][2]):int(info[i][2]+height[i]),int(info[i][1]):int(info[i][1]+width[i])] += src[i] * mask[i]
    end=pytime.time()-start
    #print("time={}".format(end))
    return dst

def fall_ame(um_pos_x,um_pos_y):
    #full screen
    #cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    #make ame
    time=np.random.randint(0,250,20)
    x_left=np.random.randint(100,1000,len(time))
    #x_left=[579]*len(time)
    #pitch candy:rain
    images=np.random.randint(0,3,len(time))
    size=np.zeros((len(time),2))
    size[np.where(images==0)]=[140,140]
    size[np.where(images!=0)]=[140,140]
    fall_obs=[]
    #info of each ame
    for i in range(len(time)):
        fall_obs.append([images[i],x_left[i],0,size[i][0],size[i][1]])

    fps = 25
    j=0
    info=np.array([])
    flip_info_r=np.array([])
    flip_info_l=np.array([])
    flip_info_rfar=np.array([])
    flip_info_lfar=np.array([])

    while j<=300:
        flip_rain_info=np.array([])
        start_time = pytime.time()
        if j in time:
            num=np.where(time==j)[0][0]
            print("num={}".format(num))
            info=info.tolist() #np.append is bad
            info.append(fall_obs[num])
            info=np.array(info)

        # think the relationship with umbrella
        if len(info)>0 and len(np.where(info[:,2]==um_pos_y)[0])>0:
            #remove candy from info
            num_f=np.where(info[:,2]==um_pos_y)
            keep=info[num_f[0][0]]
            keep=keep.tolist()

            if um_pos_x-70<=keep[1] and keep[1]<um_pos_x+100:
            #x_center of parabola
                keep.append(keep[1]+80)
                info=info.tolist()
                info.pop(num_f[0][0])
                info=np.array(info)
                #add candy to flip_info
                flip_info_r=flip_info_r.tolist()
                flip_rain_info=flip_rain_info.tolist()
                #candy only
                if keep[0]==0:
                    keep[0]=4
                    flip_rain_info.append(keep)
                else:
                    flip_info_r.append(keep)

            elif um_pos_x-170<=keep[1] and keep[1]<um_pos_x-70:
                #x_centerof parabola
                keep.append(keep[1]-80)
                info=info.tolist()
                info.pop(num_f[0][0])
                info=np.array(info)
                #add candy to flip info
                flip_info_l=flip_info_l.tolist()
                flip_rain_info=flip_rain_info.tolist()
                #candy only
                if keep[0]==0:
                    keep[0]=4
                    flip_rain_info.append(keep)
                else:
                    flip_info_l.append(keep)

            elif um_pos_x+100<=keep[1] and keep[1]<um_pos_x+200:
                #x_centerof parabola
                keep.append(keep[1]+100)
                info=info.tolist()
                info.pop(num_f[0][0])
                info=np.array(info)
                #add candy to flip info
                flip_info_rfar=flip_info_rfar.tolist()
                flip_rain_info=flip_rain_info.tolist()
                #candy only
                if keep[0]==0:
                    keep[0]=4
                    flip_rain_info.append(keep)
                else:
                    flip_info_rfar.append(keep)

            elif um_pos_x-270<=keep[1] and keep[1]<um_pos_x-170:
                #x_centerof parabola
                keep.append(keep[1]-100)
                info=info.tolist()
                info.pop(num_f[0][0])
                info=np.array(info)
                #add candy to flip info
                flip_info_lfar=flip_info_lfar.tolist()
                flip_rain_info=flip_rain_info.tolist()
                #candy only
                if keep[0]==0:
                    keep[0]=4
                    flip_rain_info.append(keep)
                else:
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
        flip_info_r=np.array([l for l in flip_info_r if (l[1]<1100 and l[2]<1100)])
        print("flip_info_r={}".format(flip_info_r))

        if len(flip_info_l)>0:
            flip_info_l[:,1]-=np.array([10]*len(flip_info_l),dtype=np.int)
            #make parabola
            num_5=np.where(flip_info_l[:,1]>flip_info_l[:,5])
            flip_info_l[num_5,2]-=np.array([20]*len(num_5[0]),dtype=np.int)
            num_6=np.where(flip_info_l[:,1]<flip_info_l[:,5])
            flip_info_l[num_6,2]+=np.array([10]*len(num_6[0]),dtype=np.int)
        flip_info_l=np.array([l for l in flip_info_l if (0<l[1] and l[2]<1100)])
        print("flip_info_l={}".format(flip_info_l))

        if len(flip_info_rfar)>0:
            flip_info_rfar[:,1]+=np.array([10]*len(flip_info_rfar),dtype=np.int)
            #make parabola
            num_7=np.where(flip_info_rfar[:,1]<flip_info_rfar[:,5])
            flip_info_rfar[num_7,2]-=np.array([5]*len(num_7[0]),dtype=np.int)
            num_8=np.where(flip_info_rfar[:,1]>flip_info_rfar[:,5])
            flip_info_rfar[num_8,2]+=np.array([5]*len(num_8[0]),dtype=np.int)
        flip_info_rfar=np.array([l for l in flip_info_rfar if (l[1]<1100 and l[2]<1100)])
        print("flip_info_rfar={}".format(flip_info_rfar))

        if len(flip_info_lfar)>0:
            flip_info_lfar[:,1]-=np.array([10]*len(flip_info_lfar),dtype=np.int)
            #make parabola
            num_9=np.where(flip_info_lfar[:,1]>flip_info_lfar[:,5])
            flip_info_lfar[num_9,2]-=np.array([5]*len(num_9[0]),dtype=np.int)
            num_6=np.where(flip_info_lfar[:,1]<flip_info_lfar[:,5])
            flip_info_lfar[num_6,2]+=np.array([5]*len(num_6[0]),dtype=np.int)
        flip_info_lfar=np.array(([l for l in flip_info_lfar if (0<l[1] and l[2]<1100)]),dtype=np.int)
        print("flip_info_lfar={}".format(flip_info_lfar))

        #remove fallen ame max:1100
        info=np.array(([i for i in info if i[2]<1100]),dtype=np.int)
        info=np.array(info)
        if len(info)>0:
            info[:,2]+=np.array([10]*len(info),dtype=np.int)
        print("info={}".format(info))


        img_1=Some2OnePicture('./images/sky.jpg',info)
        cv2.imwrite('./outputs/test_1201.jpg',img_1)
        img_2=Some2OnePicture('./outputs/test_1201.jpg',flip_info_r)
        cv2.imwrite('./outputs/test_1203.jpg',img_2)
        img_3=Some2OnePicture('./outputs/test_1203.jpg',flip_info_l)
        cv2.imwrite('./outputs/test_1207.jpg',img_3)
        img_4=Some2OnePicture('./outputs/test_1207.jpg',flip_info_rfar)
        cv2.imwrite('./outputs/test_1207_2.jpg',img_4)
        img_5=Some2OnePicture('./outputs/test_1207_2.jpg',flip_info_lfar)
        cv2.imwrite('./outputs/test_1207_3.jpg',img_5)
        img=Some2OnePicture('./outputs/test_1207_3.jpg',flip_rain_info)
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

fall_ame(-10,650)
