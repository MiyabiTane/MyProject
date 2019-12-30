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
        elif info[i][0]==1:
            alpha_image='./images/candy.png'
        elif info[i][0]==2:
            alpha_image='./images/candy_small.png'
        elif info[i][0]==3:
            alpha_image='./images/start.png'
        elif info[i][0]==4:
            alpha_image='./images/flip_rain.png'
        elif info[i][0]==5:
            alpha_image='./images/paku_r_open.png'
        elif info[i][0]==6:
            alpha_image='./images/paku_l_open.png'
        elif info[i][0]==7:
            alpha_image='./images/paku_r_close.png'
        elif info[i][0]==8:
            alpha_image='./images/paku_l_close.png'
        elif info[i][0]==9:
            alpha_image='./images/plus_2.png'
        elif info[i][0]==10:
            alpha_image='./images/minus_1.png'
        elif info[i][0]==11:
            alpha_image='./images/pero_4.png'
        elif info[i][0]==12:
            alpha_image='./images/pero_5.png'
        elif info[i][0]==13:
            alpha_image='./images/pero_6.png'
        elif info[i][0]==14:
            alpha_image='./images/pero_7.png'
        elif info[i][0]==15:
            alpha_image='./images/pero_8.png'
        elif info[i][0]==16:
            alpha_image='./images/pero_1.png'
        elif info[i][0]==17:
            alpha_image='./images/pero_2.png'
        elif info[i][0]==18:
            alpha_image='./images/pero_3.png'
        elif info[i][0]==19:
            alpha_image='./images/plus_4.png'
        elif info[i][0]==20:
            alpha_image='./images/plus_10.png'
        elif info[i][0]==21:
            alpha_image='./images/gotsu_right.png'
        elif info[i][0]==22:
            alpha_image='./images/gotsu_left.png'
        elif info[i][0]==23:
            alpha_image='./images/sun_1.png'
        elif info[i][0]==24:
            alpha_image='./images/sun_2.png'
        elif info[i][0]==25:
            alpha_image='./images/rain_small.png'
        elif info[i][0]==26:
            alpha_image='./images/cloud1.png'
        elif info[i][0]==27:
            alpha_image='./images/cloud2.png'
        elif info[i][0]==28:
            alpha_image='./images/cloud3.png'
        elif info[i][0]==29:
            alpha_image='./images/cloud4.png'
        elif info[i][0]==30:
            alpha_image='./images/cloud5.png'
        elif info[i][0]==31:
            alpha_image='./images/cloud6.png'
        elif info[i][0]==32:
            alpha_image='./images/cloud7.png'
        elif info[i][0]==33:
            alpha_image='./images/cloud8.png'
        elif info[i][0]==34:
            alpha_image='./images/minus_2.png'


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


def ResultPicture(base_img,info):
    start=pytime.time()
    dst=cv2.imread(base_img)
    #print("size={}".format(dst.shape))
    src=[0]*len(info)
    mask=[0]*len(info)
    width=[0]*len(info)
    height=[0]*len(info)
    for i in range(len(info)):
        if info[i][0]==0:
            alpha_image='./images/number_0.png'
        elif info[i][0]==1:
            alpha_image='./images/number_1.png'
        elif info[i][0]==2:
            alpha_image='./images/number_2.png'
        elif info[i][0]==3:
            alpha_image='./images/number_3.png'
        elif info[i][0]==4:
            alpha_image='./images/number_4.png'
        elif info[i][0]==5:
            alpha_image='./images/number_5.png'
        elif info[i][0]==6:
            alpha_image='./images/number_6.png'
        elif info[i][0]==7:
            alpha_image='./images/number_7.png'
        elif info[i][0]==8:
            alpha_image='./images/number_8.png'
        elif info[i][0]==9:
            alpha_image='./images/number_9.png'
        elif info[i][0]==10:
            alpha_image='./images/point.png'
        elif info[i][0]==11:
            alpha_image='./images/minus.png'
        elif info[i][0]==12:
            alpha_image='./images/finish.png'
        elif info[i][0]==13:
            alpha_image='./images/dram.png'
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


def OpeningPicture(base_img,info):
    start=pytime.time()
    dst=cv2.imread(base_img)
    #print("size={}".format(dst.shape))
    src=[0]*len(info)
    mask=[0]*len(info)
    width=[0]*len(info)
    height=[0]*len(info)
    for i in range(len(info)):
        if info[i][0]==0:
            alpha_image='./images/a.png'
        elif info[i][0]==1:
            alpha_image='./images/me.png'
        elif info[i][0]==2:
            alpha_image='./images/ga.png'
        elif info[i][0]==3:
            alpha_image='./images/fu.png'
        elif info[i][0]==4:
            alpha_image='./images/ru.png'
        elif info[i][0]==5:
            alpha_image='./images/exp_candy.png'
        elif info[i][0]==6:
            alpha_image='./images/umbrella.png'

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


def RulePicture(base_img,info):
    start=pytime.time()
    dst=cv2.imread(base_img)
    #print("size={}".format(dst.shape))
    src=[0]*len(info)
    mask=[0]*len(info)
    width=[0]*len(info)
    height=[0]*len(info)
    for i in range(len(info)):
        if info[i][0]==0:
            alpha_image='./images/rule_exp.png'
        elif info[i][0]==1:
            alpha_image='./images/rule_exp_after.png'
        elif info[i][0]==2:
            alpha_image='./images/game_start.png'
        elif info[i][0]==3:
            alpha_image='./images/game_start_after.png'
        elif info[i][0]==4:
            alpha_image='./images/next.png'
        elif info[i][0]==5:
            alpha_image='./images/next_after.png'
        elif info[i][0]==6:
            alpha_image='./images/exp_flip_high.png'
        elif info[i][0]==7:
            alpha_image='./images/exp_flip_low.png'
        elif info[i][0]==8:
            alpha_image='./images/exp_pakkun.png'
        elif info[i][0]==9:
            alpha_image='./images/arrow.png'
        elif info[i][0]==10:
            alpha_image='./images/exp_flip_rain.png'
        elif info[i][0]==11:
            alpha_image='./images/exp_point_get.png'
        elif info[i][0]==12:
            alpha_image='./images/piko_left.png'
        elif info[i][0]==13:
            alpha_image='./images/piko_right.png'

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
