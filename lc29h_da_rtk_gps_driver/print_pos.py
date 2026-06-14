from geometry_msgs.msg import PointStamped
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix


class PrintPos(Node):
    """ROS2 node that subscribes to GPS data and prints it periodically."""

    def __init__(self):
        """Initialize the PrintPos node."""
        super().__init__('print_pos')

        # Initialize fields
        self.fix_type = 'invalid'
        self.x = None
        self.y = None
        self.z = None

        # Subscribers
        self.fix_sub = self.create_subscription(
            NavSatFix,
            'gps/fix',
            self.fix_callback,
            10
        )

        self.xy_sub = self.create_subscription(
            PointStamped,
            'gps/xy',
            self.xy_callback,
            10
        )

        # Periodic timer (4 seconds)
        self.timer = self.create_timer(4.0, self.timer_callback)

        self.get_logger().info('PrintPos node initialized and listening.')

    def fix_callback(self, msg):
        """Update the latest fix type status."""
        status_val = msg.status.status
        # Map values according to spec:
        # GPS fix status (0 = invalid, 1 = GPS fix, 2 = DGPS fix, 4 = RTK_FIX, 5 = RTK_FLOAT)
        mapping = {
            0: 'invalid',
            1: 'GPS fix',
            2: 'DGPS fix',
            4: 'RTK_FIX',
            5: 'RTK_FLOAT'
        }
        self.fix_type = mapping.get(status_val, f'unknown ({status_val})')

    def xy_callback(self, msg):
        """Update the latest local x, y, z coordinates."""
        self.x = msg.point.x
        self.y = msg.point.y
        self.z = msg.point.z

    def timer_callback(self):
        """Print the latest coordinates and fix type status."""
        # Format values to 3 decimal places if available, otherwise 'None'
        x_str = f'{self.x:.3f}' if self.x is not None else 'None'
        y_str = f'{self.y:.3f}' if self.y is not None else 'None'
        z_str = f'{self.z:.3f}' if self.z is not None else 'None'

        # Print to stdout/logger
        output_str = f'{self.fix_type}, {x_str}, {y_str}, {z_str}'
        # self.get_logger().info(output_str)
        # Also print to stdout directly to ensure it appears in raw output
        print(output_str, flush=True)


def main(args=None):
    """Run the print_pos node."""
    rclpy.init(args=args)
    node = PrintPos()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
