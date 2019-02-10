from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from duckietown_msgs.msg import Twist2DStamped
import numpy as np
import sys
import rospy
import cv2
import time


#180 90;turn+stop;find center;a line

#wide detect_wide turn_wide

#global flag
flag = 3
#global rflag
rflag = 0
#global lflag
lflag = 0
#global sflag
sflag = 0
wflag = 0
t = 0
turnflag = 0

def move(flag):
    pub = rospy.Publisher('duckiebot1/joy_mapper_node/car_cmd', Twist2DStamped, queue_size=10)
    msg = Twist2DStamped()
    msg.header.seq = 0
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = ""
    time90 = 2.5
    time45 = 1

    if flag == 0:
        msg.omega = 0.0
        msg.v = 0.0
    elif flag == 1:#right
        msg.omega = -0.2
        msg.v = 0.0
	#pub.publish(msg)
	#print("send")
	#time.sleep(time45)
	#print("f")
    elif flag == 2:#left
        msg.omega = 0.2
        msg.v = 0.0
	#pub.publish(msg)
	#time.sleep(time45)
    elif flag == 3:#f
        msg.omega = 0.0
        msg.v = 0.05
	#pub.publish(msg)
	#time.sleep(time45)
    elif flag == 4:#b
        msg.omega = 0.0
        msg.v = -0.1
    elif flag == 5:#90right
        msg.omega = -0.2
        msg.v = 0.00
	#pub.publish(msg)
	#time.sleep(time90)
	#msg.omega = 0.0
        #msg.v = 0.1
	#pub.publish(msg)
	
    elif flag == 6:#90left
        msg.omega = 0.2
        msg.v = 0.00
	#pub.publish(msg)
	#time.sleep(time90)
	#msg.omega = 0.0
        #msg.v = 0.1
	#pub.publish(msg)
    else:
        msg.omega = 0.0
        msg.v = 0.0
	#pub.publish(msg)

    #if time.clock() < 1:
	#msg.omega = 0.0
        #msg.v = 0.0
    #else:
	#time.clock()
    #print "msg.omega = ", msg.omega , "msg.v = ", msg.v
    pub.publish(msg)
    

def callback(rosdata):
	print("!")
	print(time.clock())
	global rflag
	global lflag
	global sflag
	global wflag
	global t
	#global turnflag
        #rospy.loginfo(rospy.get_caller_id())
        np_arr = np.fromstring(rosdata.data, np.uint8)
        img = cv2.imdecode(np_arr, 1)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	lower_red = np.array([0, 43, 46])                                      
	high_red = np.array([10,255, 255]) 
	lower_black = np.array([20,0,0])                                      
	high_black = np.array([50,255, 75]) 
	mask_red = cv2.inRange(hsv, lowerb = lower_red, upperb = high_red)
	mask_black = cv2.inRange(hsv, lowerb = lower_black, upperb = high_black)
	cv2.imshow("black", mask_black)
	cv2.imshow("red", mask_red)

	image_contour, contours, hierarchy = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	image_contour_black, contours_black, hierarchy_black = cv2.findContours(mask_black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#hierarchy = hierarchy[0]
	#hierarchy_black = hierarchy_black[0]




	minnum_stop = 150
	minnum_turn = 250
	morenum = 30
	red = 0
	black = 0
	max_num = 0
	center_r = 0
	center_b = 0
	img_avg_x = img.shape[1] / 2
	img_avg_y = img.shape[0] / 2
	wide = 50 #detect
	turn_wide = 40
	whole_max_x = 15
	whole_min_x = 0
	
	for i in range(len(contours)):
		center_x = 0
		center_y = 0
		max_x = 0
		min_x = 1000	
		for k in range(len(contours[i])):
		    center_x += contours[i][k][0][0]
		    center_y += contours[i][k][0][1]
		    if contours[i][k][0][0] > max_x:
	    	    	max_x = contours[i][k][0][0]
		    if contours[i][k][0][0] < min_x:
	     		min_x = contours[i][k][0][0]
	
		center_x = int(center_x / len(contours[i]))     
		center_y = int(center_y / len(contours[i]))
		if len(contours[i]) > max_num and center_x < img_avg_x + wide and center_y < img_avg_y + wide and center_x > img_avg_x - wide and center_y > img_avg_y - wide:
		
			max_num = len(contours[i])
			red = i
			center_r = center_x
	if red == 0:
		for i in range(len(contours)):
			center_x = 0
			center_y = 0
			
			for k in range(len(contours[i])):
			    center_x += contours[i][k][0][0]
			    center_y += contours[i][k][0][1]
	
			center_x = int(center_x / len(contours[i]))     
			center_y = int(center_y / len(contours[i]))
			if len(contours[i]) > max_num :
		
				max_num = len(contours[i])
				red = i
				center_r = center_x
	#if red == 0:
		#move(4)
		#time.sleep(0.1) 



	max_num = 0
	#center = 0

	for i in range(len(contours_black)):
		center_x = 0
		center_y = 0
		max_x = 0
		min_x = 1000
		max_y = 0
		min_y = 1000	

		for k in range(len(contours_black[i])):
		    center_x += contours_black[i][k][0][0]
		    center_y += contours_black[i][k][0][1]
		    if contours_black[i][k][0][0] > max_x:
	    	    	max_x = contours_black[i][k][0][0]
		    if contours_black[i][k][0][1] > max_y:
			max_y = contours_black[i][k][0][1]
		    if contours_black[i][k][0][0] < min_x:
	     		min_x = contours_black[i][k][0][0]
		    if contours_black[i][k][0][1] < min_y:
			min_y = contours_black[i][k][0][1]
		center_x = int(center_x / len(contours_black[i]))     
		center_y = int(center_y / len(contours_black[i]))

		if  center_y > img_avg_y and len(contours_black[i]) > max_num and max_y - min_y > 30 and len(contours[red]) < 100:
		
			#t = i
			#c = 0
			max_num = len(contours_black[i])
			black = i
			center_b = center_x
			whole_max_x = max_x
			whole_min_x = min_x     
	#print(whole_max_x)
	#print(whole_min_x)

	cv2.drawContours(img, contours_black, black, (255, 255, 0), 2)
	if center_b < img_avg_x and whole_max_x > img_avg_x-10 and max_num >10:
	    flag = 1
	    print("turn right")
	elif center_b > img_avg_x and whole_min_x < img_avg_x+10 and max_num >10:
            flag = 2
	    print("turn left")
	else:
	    flag = 3
	    print("forward")





	
	

	#if red == 0:
		#print("no")
	#print(len(contours[red]))
	#if red != 0:
	cv2.drawContours(img, contours, red, (0, 255, 255), 2)

	print(len(contours[red]))
	if len(contours[red]) > 140:
		if center_r == 0:
			print("object lost!")
		elif center_r > img_avg_x + turn_wide:
			flag = 1
			print("turn right!")
		elif center_r < img_avg_x - turn_wide:
			flag = 2
			print("turn left!")
		else:
			flag = 3
	 		print("forward!")  


	if len(contours[red]) < minnum_stop:
		print("")
	else:
		left = 0
		right = 0
		for k in range(len(contours[red])):
			if contours[red][k][0][0] > center_r:
			    right = right + 1
			    #img[contours[red][k][0][1],contours[red][k][0][0]]=(0,0,0)
			else:
			    left = left +1
			    #img[contours[red][k][0][0],contours[red][k][0][0]]=(255,255,255)
		if right > left + morenum and len(contours[red]) > minnum_turn:
			#rflag = rflag + 1
			flag = 5
			print("right")
		elif left > right + morenum and len(contours[red]) > minnum_turn:
			#lflag = lflag + 1
			flag = 6
			print("left")
		elif right - left < 10 and right - left > -10:
			sflag = sflag + 1
			flag = 0
			print("stop")
		#else:
			#flag = 1


	if sflag > 3:
		flag = 0
		rflag = 0
		lflag = 0
		sflag = 0
		print("s")
		move(0)
		sys.exit()
	elif rflag > 3:
		flag = 5
		rflag = 0
		lflag = 0
		sflag = 0
		print("r")
	elif lflag > 3:
		flag = 6
		rflag = 0
		lflag = 0
		sflag = 0
		print("l")
	
			

	time90 = 2
        time45 = 0.5
	
	print(flag)
	#print(time.clock())
	if time.clock() > t:
		move(flag)
		wfalg = 1
		t = t + 0.5
		if flag == 5 or flag == 6:
			print("!!!!!!!!!!!!!!!!!!!!!!")
			time.sleep(time90)
			#turnflag = 1
	else:
		move(0)
	#move(flag)
	#if flag == 5 or flag == 6:
		#time.sleep(time90)
	#else:
		#time.sleep(time45)
	#move(0)
	#time.sleep(1)
	cv2.imshow('',img)
	cv2.waitKey(1)

def camera():
	rospy.init_node('car_ctr', anonymous=True)
	rospy.Subscriber("/duckiebot1/camera_node/image/rect/compressed", CompressedImage, callback)
	rospy.spin()
	time.clock()


if __name__ == '__main__':
        camera()
