import cv2
import numpy as np

src=cv2.imread('./images2/candy2.png',-1)
dst=cv2.imread('./images2/sky.jpg')
#print(src.shape)
src=cv2.resize(src,dsize=(250,250))

width, height = src.shape[:2]

mask = src[:,:,3]  # アルファチャンネルだけ抜き出す。
mask=np.tile(mask[:,:,np.newaxis],(1,1,3))
#mask = cv2.cvtColor(mask, cv2.cv.CV_GRAY2BGR)  # 3色分に増やす。
mask = mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
mask=mask.astype(np.uint8)

src = src[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

dst[0:height, 0:width] *= 1 - mask  # 透過率に応じて元の画像を暗くする。
dst[0:height, 0:width] += src * mask  # 貼り付ける方の画像に透過率をかけて加算。

cv2.imwrite('./outputs/paste_alpha.jpg', dst)
