import cv2
import numpy as np

#info=[alpha_img,x_left,y_up,wid,hei]が入ってる。
def Some2OnePicture(base_img,info):
    dst=cv2.imread(base_img)
    src=[0]*len(info)
    mask=[0]*len(info)
    width=[0]*len(info)
    height=[0]*len(info)
    for i in range(len(info)):
        if info[i][0]==0:
            alpha_image='./images2/candy2.png'
        else:
            alpha_image='./images2/rain.png'
        src[i]=cv2.imread(alpha_image,-1)
        src[i]=cv2.resize(src[i],dsize=(int(info[i][3]),int(info[i][4])))
        width[i], height[i] = src[i].shape[:2]

        mask[i] = src[i][:,:,3]  # アルファチャンネルだけ抜き出す。
        mask[i]=np.tile(mask[i][:,:,np.newaxis],(1,1,3))
        #mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)  # 3色分に増やす。
        mask[i] = mask[i] / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
        mask[i]=mask[i].astype(np.uint8)
        src[i] = src[i][:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

        dst[info[i][2]:info[i][2]+height[i],info[i][1]:info[i][1]+width[i]] *= 1 - mask[i]  # 透過率に応じて元の画像を暗くする。
        dst[info[i][2]:info[i][2]+height[i],info[i][1]:info[i][1]+width[i]] += src[i] * mask[i]  # 貼り付ける方の画像に透過率をかけて加算。

    return dst

#ふってくるあめを生成
time=np.array([0,45])
x_left=[50,1000]
images=np.array([0,1])
size=np.zeros((len(time),2))
size[np.where(images==0)]=[250,250]
size[np.where(images==1)]=[200,200]
obs_info=[]
#fall_obs[i]にi番目に降るあめの情報を入れる。
for i in range(len(time)):
    obs_info.append([images[i],x_left[i],0,size[i][0],size[i][1]])
print(obs_info)

dst=Some2OnePicture('./images2/sky.jpg',obs_info)
cv2.imwrite('./outputs/paste_some_alpha.jpg', dst)
