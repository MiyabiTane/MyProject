import cv2
import numpy as np
import random
import time as pytime

#x_left,y_list=[hoge,hoge,...]
def parabola(a,x_left,y_up,x_cen,y_plus):
    ans=[]
    for i in range(len(x_left)):
        ans.append(-a*((int(x_left[i])-int(x_cen[i]))**2)+int(y_up[i])-y_plus)
    return ans

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
            alpha_image='./images3/rain.png'
        elif info[i][0]==4:
            alpha_image='./images3/flip_rain.png'
        else:
            alpha_image='./images3/candy.png'
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
    print("time={}".format(end))
    return dst
"""
cv2.namedWindow('result', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
"""
#make ame
time=np.random.randint(0,250,10)
x_left=np.random.randint(0,900,len(time))
#pitch candy:rain
images=np.random.randint(0,3,len(time))
size=np.zeros((len(time),2))
size[np.where(images==0)]=[200,200]
size[np.where(images!=0)]=[180,180]
fall_obs=[]
#info of each ame
for i in range(len(time)):
    fall_obs.append([images[i],x_left[i],0,size[i][0],size[i][1]])

fps = 25
j=0
info=np.array([])
flip_info=np.array([])

while j<=300:
    flip_rain_info=np.array([])
    start_time = pytime.time()
    if j in time:
        num=np.where(time==j)[0][0]
        print("num={}".format(num))
        info=info.tolist() #np.append is bad
        info.append(fall_obs[num])
        info=np.array(info)

    #in the last, y=500 -> catch ame right
    #when y=500 flip candy or rain
    if len(info)>0 and (500 in info[:,2]):
        #remove candy from info
        num_f=np.where(info[:,2]==500)
        keep=info[num_f[0][0]]
        keep=keep.tolist()
        #x_center of parabola
        keep.append(keep[1]+80)
        info=info.tolist()
        info.pop(num_f[0][0])
        info=np.array(info)
        #add candy to flip_info
        flip_info=flip_info.tolist()
        flip_rain_info=flip_rain_info.tolist()
        #candy only
        if keep[0]==0:
            keep[0]=4
            flip_rain_info.append(keep)
        else:
            flip_info.append(keep)
        flip_info=np.array(flip_info)
        flip_rain_info=np.array(flip_rain_info)
    print("flip_rain_info={}".format(flip_rain_info))

    if len(flip_info)>0:
        flip_info[:,1]+=[10]*len(flip_info)
        #make parabola
        num_3=np.where(flip_info[:,1]<flip_info[:,5])
        flip_info[num_3,2]-=[20]*len(num_3[0])
        num_4=np.where(flip_info[:,1]>flip_info[:,5])
        flip_info[num_4,2]+=[10]*len(num_4[0])
        #flip_info[:,2]=parabola(a=0.5,x_left=flip_info[:,1],y_up=flip_info[:,2],x_cen=flip_info[:,5],y_plus=10)
    flip_info=np.array([l for l in flip_info if (l[1]<1100 and l[2]<1100)])
    print("flip_info={}".format(flip_info))

    #remove fallen ame max:1100
    info=np.array([i for i in info if i[2]<1100])
    info=np.array(info)
    if len(info)>0:
        info[:,2]+=[10]*len(info)
    print("info={}".format(info))

    img_1=Some2OnePicture('./images3/sky.jpg',info)
    cv2.imwrite('./outputs/test_1201.jpg',img_1)
    img_2=Some2OnePicture('./outputs/test_1201.jpg',flip_info)
    cv2.imwrite('./outputs/test_1203.jpg',img_2)
    img=Some2OnePicture('./outputs/test_1203.jpg',flip_rain_info)
    img = cv2.resize(img, (640,480))

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
