import rospy
from sensor_msgs.msg import Image, Imu, CameraInfo
import message_filters
import rosbag

bag = rosbag.Bag('/home/nirmal/catkin_ws/src/rosbag_data/image_imu.bag', 'w')

def callback(image_data, camera_info_data, imu_data):
    print('writing data to bag')
    bag.write('/camera/rgb/image_raw', image_data)
    bag.write('/camera/rgb/camera_info', camera_info_data)
    bag.write('/imu', imu_data)


def main():
    rospy.init_node('read_to_rosbag', anonymous=True)
    image_data = message_filters.Subscriber('/camera/rgb/image_raw', Image)
    camera_info_data = message_filters.Subscriber('/camera/rgb/camera_info', CameraInfo)
    imu_date = message_filters.Subscriber('/imu', Imu)
    ts = message_filters.ApproximateTimeSynchronizer([image_data, camera_info_data, imu_date], 10, 0.1)
    ts.registerCallback(callback)
    rospy.spin()

if __name__ == '__main__':
    main()
