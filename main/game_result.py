import ame_movie
import cv2

#if point=minus
def game_result(point):
    flag=0
    original_point=point
    if point<0:
        flag=1
        point*=-1
    info=[]
    x_left=600
    while True:
        num=point%10
        if num==0:
            info.append([num+20,x_left,300,400,400])
        else:
            info.append([num+10,x_left,300,400,400])
        point-=num
        if point==0:
            if flag==1:
                info.append([22,x_left-170,380,300,300])
            break
        point/=10
        x_left-=200
    info.append([21,700,600,400,400])

    while True:
        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        if original_point>40:
            img=ame_movie.Some2OnePicture('./images/sky_nizi.jpg',info)
        elif original_point>20:
            img=ame_movie.Some2OnePicture('./images/sky_cloud.jpg',info)
        else:
            img=ame_movie.Some2OnePicture('./images/sky_rain.jpg',info)
        img = cv2.resize(img, (640,480))

        cv2.imshow("result",img)
        if cv2.waitKey(20) >= 0:
            break

game_result(-30)
