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
    src=[0]*len(info)
    mask=[0]*len(info)
    width=[0]*len(info)
    height=[0]*len(info)
    for i in range(len(info)):
        if info[i][0]==0:
            alpha_image='./images2/rain.png'
        else:
            alpha_image='./images2/candy2.png'
        src[i]=cv2.imread(alpha_image,-1)
        src[i]=cv2.resize(src[i],dsize=(int(info[i][3]),int(info[i][4])))
        width[i], height[i] = src[i].shape[:2]

        mask[i] = src[i][:,:,3]  # get only alpha
        mask[i]=np.tile(mask[i][:,:,np.newaxis],(1,1,3))
        #mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)  # change to 3 colors
        mask[i] = mask[i] / 255.0  # 0-255->0.0-1.0
        mask[i]=mask[i].astype(np.uint8)
        src[i] = src[i][:,:,:3]  # remove alpha channel

        dst[int(info[i][2]):int(info[i][2])+height[i],int(info[i][1]):int(info[i][1])+width[i]] *= 1 - mask[i]
        dst[int(info[i][2]):int(info[i][2])+height[i],int(info[i][1]):int(info[i][1])+width[i]] += src[i] * mask[i]
    end=pytime.time()-start
    print("time={}".format(end))
    return dst

#fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
#video = cv2.VideoWriter('./outputs/fall_candy.mp4', fourcc, 20.0, (640, 640))

#make ame
time=np.random.randint(0,150,10)
x_left=np.random.randint(0,900,len(time))
#pitch candy:rain
images=np.random.randint(0,3,len(time))
size=np.zeros((len(time),2))
size[np.where(images==0)]=[200,200]
size[np.where(images!=0)]=[250,250]
fall_obs=[]
#info of each ame
for i in range(len(time)):
    fall_obs.append([images[i],x_left[i],0,size[i][0],size[i][1]])

fps = 25
j=0
info=np.array([])
while j<=200:
    start_time = pytime.time()
    if j in time:
        num=np.where(time==j)[0][0]
        print("num={}".format(num))
        info=info.tolist() #np.append is bad
        info.append(fall_obs[num])
    #print("info={}".format(info))
    img=Some2OnePicture('./images2/sky.jpg',info)
    img = cv2.resize(img, (640,640))
    #remove fallen ame max:1000
    info=np.array([i for i in info if i[2]<1000])
    info=np.array(info)
    if len(info)>0:
        info[:,2]+=[10]*len(info)
    print("info={}".format(info))
    cv2.imshow("result",img)
    end_time = pytime.time()
    elapsed_time = end_time - start_time # sec
    print(elapsed_time) # 100
    wait_time = max(200 - int(elapsed_time*1000), 1) # msec
    print(wait_time)
    if cv2.waitKey(wait_time) >= 0:
        break
    #video.write(img)
    j+=1

#video.release()
