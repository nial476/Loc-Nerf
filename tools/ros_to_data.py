import rosbag
from sensor_msgs.msg import Image, Imu
from cv_bridge import CvBridge
import cv2
from message_filters import TimeSynchronizer, Subscriber
import rospy

def image_callback(image_msg, imu_msg):
    # Process synchronized image and IMU data
    cv_image = bridge.imgmsg_to_cv2(image_msg, desired_encoding='passthrough')
    # Access IMU data using imu_msg
    print(imu_msg)
    # Do something with the synchronized data

if __name__ == "__main__":
    # Replace 'your_rosbag_file.bag' with the path to your ROS bag file
    bag_file_path = '/home/nirmal/2023-11-22-16-22-44.bag'

    # Open the ROS bag file
    bag = rosbag.Bag(bag_file_path, 'r')

    # Initialize a CV bridge to convert ROS Image messages to OpenCV images
    bridge = CvBridge()

    # Create subscribers for image and IMU topics
    image_sub = Subscriber('/camera/rgb/image_raw', Image)
    imu_sub = Subscriber('/imu/data', Imu)

    # Synchronize messages based on their timestamps
    ts = TimeSynchronizer([image_sub, imu_sub], queue_size=10)
    ts.registerCallback(image_callback)

    # Iterate through the messages in the bag and publish them to the subscribers
    for topic, msg, t in bag.read_messages(topics=['/camera/rgb/image_raw', '/imu']):
        if topic == '/camera/rgb/image_raw':
            ts.add('image', msg)
        elif topic == '/imu/data':
            ts.add('imu', msg)

    # Spin to allow callbacks to be executed
    rospy.spin()

    # Close the bag file
    bag.close()
