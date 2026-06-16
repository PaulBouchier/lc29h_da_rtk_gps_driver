import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PointStamped
import math
from rclpy.qos import QoSProfile, QoSReliabilityPolicy


class GPSXYNode(Node):
    def __init__(self):
        super().__init__('gps_xy_node')

        # 🔥 Declare parameters (so you can change without editing code)
        self.declare_parameter('origin_lat', 0.0)
        self.declare_parameter('origin_lon', 0.0)
        self.declare_parameter('origin_alt', 0.0)

        self.origin_lat = self.get_parameter('origin_lat').value
        self.origin_lon = self.get_parameter('origin_lon').value
        self.origin_alt = self.get_parameter('origin_alt').value

        self.get_logger().info(
            f"Using FIXED origin: lat={self.origin_lat}, lon={self.origin_lon}, alt={self.origin_alt}"
        )

        # Subscriber
        # Define a BEST_EFFORT QoS profile for subscriptions
        best_effort_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            depth=10
        )

        self.sub = self.create_subscription(
            NavSatFix,
            'gps/fix',
            self.callback,
            qos_profile=best_effort_qos
        )

        # Publisher
        self.pub = self.create_publisher(
            PointStamped,
            'gps/xy',
            10
        )

    def callback(self, msg):
        lat = msg.latitude
        lon = msg.longitude

        # 🔥 More accurate conversion (use origin latitude)
        lat_rad = math.radians(self.origin_lat)

        meters_per_deg_lat = 110540
        meters_per_deg_lon = 111320 * math.cos(lat_rad)

        dx = (lon - self.origin_lon) * meters_per_deg_lon
        dy = (lat - self.origin_lat) * meters_per_deg_lat
        dz = msg.altitude - self.origin_alt

        pt = PointStamped()
        pt.header.stamp = self.get_clock().now().to_msg()
        pt.header.frame_id = "map"

        pt.point.x = dx
        pt.point.y = dy
        pt.point.z = dz

        self.pub.publish(pt)


def main():
    rclpy.init()
    node = GPSXYNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
