import cv2
import numpy as np
import random

#base_img->.jpg,small_img->.png
def Two2OnePicture(base_img,alpha_img,x_left,y_up,wid,hei):
    src=cv2.imread(alpha_img,-1)
    dst=cv2.imread(base_img)
    src=cv2.resize(src,dsize=(wid,hei))
    width, height = src.shape[:2]

    mask = src[:,:,3]  # アルファチャンネルだけ抜き出す。
    mask=np.tile(mask[:,:,np.newaxis],(1,1,3))
    #mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)  # 3色分に増やす。
    mask = mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
    mask=mask.astype(np.uint8)
    src = src[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

    dst[y_up:y_up+height,x_left:x_left+width] *= 1 - mask  # 透過率に応じて元の画像を暗くする。
    dst[y_up:y_up+height,x_left:x_left+width] += src * mask  # 貼り付ける方の画像に透過率をかけて加算。

    return dst

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video = cv2.VideoWriter('./outputs/video_test1.mp4', fourcc, 20.0, (640, 640))

i=0
while i<=90:
    img=Two2OnePicture('./images2/sky.jpg','./images2/candy2.png',320,i*10,250,250)
    #img = cv2.imread('./images1/image{0:03d}.jpg'.format(i))
    img = cv2.resize(img, (640,640))
    video.write(img)
    i+=1

video.release()
