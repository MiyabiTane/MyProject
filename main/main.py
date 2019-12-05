import rospy
from jsk_recognition_msgs.msg import RectArray
from jsk_recognition_msgs.msg import Rect
import numpy as np
import ame_movie

message_arrived=False
def position_cb(msg):
    global message_arrived
    message_arrived=msg

if __name__=='__main__':
    try:
        message_arrived=False
        rospy.init_node('umbrella_pos')
        rospy.Subscriber('/edgetpu_object_detector/output/rects',RectArray,position_cb)
        while not rospy.is_shutdown():
            if message_arrived:
                print("message_arrived")
                #rects=[info1,info2...]
                if len(message_arrived.rects)>0:
                    y_min=500
                    umb_index=100
                    #umbrella's y is min
                    for i in range(len(message_arrived.rects)):
                        if message_arrived.rects[i].y<y_min:
                            umb_index=i
                            y_min=message_arrived.rects[i].y
                    print("rects={}".format(message_arrived.rects[umb_index]))

                    um_pos_x=message_arrived.rects[umb_index].x+message_arrived.rects[umb_index].width/2
                    um_pos_y=message_arrived.rects[umb_index].y+message_arrived.rects[umb_index].height/2

                    um_pos_x=np.clip(int(um_pos_x*65/24)-216,0,1300)
                    um_pos_y=np.clip(int(um_pos_y*65/24),0,1300)

                    ame_movie.fall_ame(um_pos_x,um_pos_y)

                    print("x={},y={}".format(um_pos_x,um_pos_y))

            message_arrived=False
            rospy.sleep(0.5)

    except rospy.ROSInterruptException:
        pass
