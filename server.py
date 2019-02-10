import socket
import os
import tty,termios
import sys
import rospy
from std_msgs.msg import String
from duckietown_msgs.msg import Twist2DStamped

hostname = '192.169.1.103' 
port = 11111  
addr = (hostname,port)
srv = socket.socket() 
srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
srv.bind(addr)
srv.listen(10)
print("waiting connect")

def socket():
	connect_socket,client_addr = srv.accept()
	print(client_addr)
	recevent = connect_socket.recv(1024)
	ch = str(recevent)
	connect_socket.send(bytes("succeed"))
	connect_socket.close()
	return ch

def move():


    pub = rospy.Publisher('duckiebot1/joy_mapper_node/car_cmd', Twist2DStamped, queue_size=10)
    rospy.init_node('move_android', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    count = 1

    while not rospy.is_shutdown():
        msg = Twist2DStamped()
        msg.header.seq = count
	msg.header.stamp = rospy.Time.now()
	msg.header.frame_id = ""

	ch = socket()
	
	if 'a' in ch:
	    print "left\n"
            msg.v = 0
	    msg.omega = 1
	elif 'd' in ch:
	    print "right\n"
            msg.v = 0
	    msg.omega = -1
	elif 'w' in ch :
	    print "forward\n"
            msg.v = 0.2
	    msg.omega = 0
	elif 's' in ch :
	    print "back\n"
            msg.v = -0.2
            msg.omega = 0
	elif ' ' in ch:
            print "stop\n"
            msg.v = 0
	    msg.omega = 0
	elif 'q' in ch :
            msg.v = 0
	    msg.omega = 0
	    pub.publish(msg)
            print "quit"
            break
        else:
            continue

	log = "succeed v:" + str(msg.v) + ", omega:" + str(msg.omega) + "\r"
        rospy.loginfo(log)
	pub.publish(msg)
        rate.sleep()



if __name__ == '__main__':
	move()


