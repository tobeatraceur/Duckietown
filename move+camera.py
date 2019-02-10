from sensor_msgs.msg import CompressedImage
import numpy as np
import os
import tty,termios
import sys
import rospy
from std_msgs.msg import String
from duckietown_msgs.msg import Twist2DStamped
import cv2
import threading
import time

def move():
    fd = sys.stdin.fileno()
    old_ttyinfo = termios.tcgetattr(fd)
    tty.setraw(fd)


    pub = rospy.Publisher('duckiebot1/joy_mapper_node/car_cmd', Twist2DStamped, queue_size=10)
    #rospy.init_node('move', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    count = 1

    while not rospy.is_shutdown():
        msg = Twist2DStamped()
        msg.header.seq = count
	msg.header.stamp = rospy.Time.now()
	msg.header.frame_id = ""

	ch = sys.stdin.read(1)
	
	if ch == 'a' or 'D' in ch :
	    print "left\n"
            msg.v = 0
	    msg.omega = 0.2
	    time.clock()	
	elif ch == 'd' or 'C' in ch:
	    print "right\n"
            msg.v = 0
	    msg.omega = -0.2
	elif ch == 'w' or 'A' in ch:
	    print "forward\n"
            msg.v = 0.1
	    msg.omega = 0.2
	    
	elif ch == 's' or 'B' in ch:
	    print "back\n"
            msg.v = -0.1
            msg.omega = 0
	elif ch == ' ':
            print "stop\n"
            msg.v = 0
	    msg.omega = 0
	    print(time.clock())
	elif ch == 'q':
            msg.v = 0
	    msg.omega = 0
	    pub.publish(msg)
            print "quit"
            return 0
        else:
            continue

	log = "succeed v:" + str(msg.v) + ", omega:" + str(msg.omega) + "\r"
        rospy.loginfo(log)
	pub.publish(msg)
        rate.sleep()

    termios.tcsetattr(fd, termios.TCSADRAIN, old_ttyinfo)

def callback(rosdata):
    #rospy.loginfo(rospy.get_caller_id())
    np_arr = np.fromstring(rosdata.data, np.uint8)
    image_np = cv2.imdecode(np_arr, 1)
    cv2.imshow('image', image_np)
    cv2.waitKey(1)
    

def camera():
	#rospy.init_node('car_ctr', anonymous=True)
	rospy.Subscriber("/duckiebot1/camera_node/image/rect/compressed", CompressedImage, callback)
	rospy.spin()

threads = []
t1 = threading.Thread(target=camera)
threads.append(t1)
t2 = threading.Thread(target=move)
threads.append(t2)

if __name__ == '__main__':
    try:
		rospy.init_node('move+camera', anonymous=True)
		for t in threads:
		    #t.setDaemon(True)
		    t.start()
		#if threads[1].get_result() == 0:
		#	sys.exit()

       
    except rospy.ROSInterruptException:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_ttyinfo)
        pass
