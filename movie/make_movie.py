import cv2

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video = cv2.VideoWriter('./outputs/video.mp4', fourcc, 20.0, (640, 640))
"""
for i in range(0,11):
    img = cv2.imread('./images1/image{0:03d}.jpg'.format(i))
    img = cv2.resize(img, (640,480))
    video.write(img)
"""
i=0
count=0
while i<=11:
    count+=1
    img = cv2.imread('./images1/image{0:03d}.jpg'.format(i))
    img = cv2.resize(img, (640,640))
    video.write(img)
    if count==3:
        i+=1
        count=0

video.release()
