import cv2
import numpy as np
import random

#base_img->.jpg,small_img->.png
#info=[alpha_img,x_left,y_up,wid,hei]が入ってる。
#base_img -> 1300*1300
def Some2OnePicture(base_img,info):
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

        mask[i] = src[i][:,:,3]  # アルファチャンネルだけ抜き出す。
        mask[i]=np.tile(mask[i][:,:,np.newaxis],(1,1,3))
        #mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)  # 3色分に増やす。
        mask[i] = mask[i] / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
        mask[i]=mask[i].astype(np.uint8)
        src[i] = src[i][:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

        dst[int(info[i][2]):int(info[i][2])+height[i],int(info[i][1]):int(info[i][1])+width[i]] *= 1 - mask[i]  # 透過率に応じて元の画像を暗くする。
        dst[int(info[i][2]):int(info[i][2])+height[i],int(info[i][1]):int(info[i][1])+width[i]] += src[i] * mask[i]  # 貼り付ける方の画像に透過率をかけて加算。

    return dst

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video = cv2.VideoWriter('./outputs/fall_candy.mp4', fourcc, 20.0, (640, 640))

#ふってくるあめを生成。timeだけ手動でいじる。
time=np.array([0,5,20,35,35,60,80,90,100,150])
x_left=np.random.randint(0,900,len(time))
#▼第２引数を大きくするほどcandyが増える。
images=np.random.randint(0,3,len(time))
size=np.zeros((len(time),2))
size[np.where(images==0)]=[200,200]
size[np.where(images!=0)]=[250,250]
fall_obs=[]
#fall_obs[i]にi番目に降るあめの情報を入れる。
for i in range(len(time)):
    fall_obs.append([images[i],x_left[i],0,size[i][0],size[i][1]])

i=0
info=np.array([])
while i<=200:
    if i in time:
        num=np.where(time==i)[0][0]
        print("num={}".format(num))
        info=info.tolist() #numpyのappendは遅いため。
        info.append(fall_obs[num])
    #print("info={}".format(info))
    img=Some2OnePicture('./images2/sky.jpg',info)
    img = cv2.resize(img, (640,640))
    video.write(img)
    #一番下に来たらinfoから削除する。1000超えるとおかしくなる。1000が一番下。
    info=np.array([i for i in info if i[2]<1000])
    info=np.array(info)
    if len(info)>0:
        info[:,2]+=[10]*len(info)
    print("info={}".format(info))
    #cv2.imshow("result",img)
    video.write(img)
    i+=1

video.release()
