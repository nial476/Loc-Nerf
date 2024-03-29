import rosbag
import rospy
import numpy as np
import csv
import os
import cv2
from cv_bridge import CvBridge

######## user params ##########
TOPIC_NAME = "/camera/rgb/image_raw"
data_bag = rosbag.Bag("/home/nirmal/2023-11-22-16-22-44.bag")
SAVE_LOC = "/home/nirmal/project/data_for_nerf"
DATA_NAME = "nerf_turtlebot"
downsample = 10
###############################

os.makedirs(SAVE_LOC + "/" + DATA_NAME)

count = 0
index=0
for topic, msg, t in data_bag.read_messages(topics=[TOPIC_NAME]):
	if topic == TOPIC_NAME:
		if count%downsample==0:
			bridge = CvBridge()
			cv_image = bridge.imgmsg_to_cv2(msg)
			cv_image.astype(np.uint8)
			cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
			cv2.imwrite(SAVE_LOC + "/" + DATA_NAME + "/r" + str(index) + '.jpg', cv_image)
			index += 1
		count += 1
