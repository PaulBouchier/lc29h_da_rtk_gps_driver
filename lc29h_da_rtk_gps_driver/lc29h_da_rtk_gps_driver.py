import rclpy
from rclpy.node import Node
from nmea_msgs.msg import Sentence
from rtcm_msgs.msg import Message
from sensor_msgs.msg import NavSatFix
import serial
import math
from typing import List, Tuple


class LC29HDA(Node):

    def __init__(self):
        super().__init__('lc29h_da_rtk_gps_driver')

        # Serial connection
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)

        # NMEA publisher
        self.nmea_pub = self.create_publisher(
            Sentence,
            'nmea',
            10
        )

        # RTCM subscriber
        self.rtcm_sub = self.create_subscription(
            Message,
            'rtcm',
            self.rtcm_callback,
            10
        )
        self._rtcm_once = False

        # GPS Fix publisher
        self.fix_pub = self.create_publisher(
            NavSatFix,
            '/gps/fix',
            10)

        # Timer
        self.timer = self.create_timer(
            0.01,
            self.read_serial
        )

        self.get_logger().info("LC29H(DA) RTK-GPS driver Started")

    def rtcm_callback(self, msg):
        try:
            # Send RTCM corrections to GPS
            self.ser.write(bytearray(msg.message))
        except Exception as e:
            self.get_logger().error(f"Exception occurred while writing RTCM to LC29H(DA): {e}")

        if not self._rtcm_once:
            self.get_logger().info("Received first RTCM message, sending corrections to LC29H(DA)")
            self._rtcm_once = True

    def convert(self, raw, direction):
        deg = int(float(raw) / 100)
        minutes = float(raw) - deg * 100
        dd = deg + minutes / 60
        if direction in ['S','W']:
            dd = -dd
        return dd

    def calculate_ros_navsat_covariance(
        self,
        fix_type: int, 
        hdop: float
    ) -> Tuple[List[float], int]:
        """
        Replicates the covariance matrix approximation from ROS nmea_navsat_driver.
        
        Args:
            fix_type (int): NMEA GGA Fix Quality (0=Invalid, 1=GPS, 2=DGPS, 4=RTK Fixed, 5=RTK Float, etc.)
            hdop (float): Horizontal Dilution of Precision
            
        Returns:
            Tuple[List[float], int]: (A 9-element flat covariance matrix in ENU order, covariance_type)
        """
        # 0 = Unknown, 1 = Approximated (Standard for this driver calculation)
        COVARIANCE_TYPE_APPROXIMATED = 1 
        
        # Initialize a blank 3x3 row-major diagonal matrix
        covariance = [0.0] * 9
        
        if fix_type <= 0:
            # Invalid fix typically sets covariances to 0 or huge numbers, depending on driver status flags
            return covariance, 0

        # Modern ROS 2 logic maps NMEA fix quality to an Estimated Position Error (EPE) 
        # based on 1-sigma standard deviation benchmarks
        gps_qualities = {
            1: 4.0,   # Standard GPS Fix (SPS) -> 4m Base EPE
            2: 2.0,   # DGPS Fix / SBAS -> 2m Base EPE
            3: 2.0,   # PPS Fix -> 2m Base EPE
            4: 0.05,  # RTK Fixed -> 0.05m (5cm) Base EPE
            5: 0.5,   # RTK Float -> 0.5m (50cm) Base EPE
            6: 0.1,   # Dead Reckoning -> 0.1m Base EPE
            7: 0.0,   # Manual Input Mode
            8: 0.0    # Simulation Mode
        }
        
        # Fallback to standard GPS accuracy if fix type is unknown
        default_epe = gps_qualities.get(fix_type, 4.0)
        
        lat_std_dev = default_epe
        lon_std_dev = default_epe
        alt_std_dev = default_epe * 2.0  # Altitude uncertainty is generally double
        
        # Modern Equation: variance = (HDOP * standard_deviation)^2
        covariance[0] = (hdop * lon_std_dev) ** 2  # East/Longitude diagonal index 0
        covariance[4] = (hdop * lat_std_dev) ** 2  # North/Latitude diagonal index 4
        covariance[8] = (2.0 * hdop * alt_std_dev) ** 2  # Up/Altitude diagonal index 8
            
        return covariance, COVARIANCE_TYPE_APPROXIMATED

    def read_serial(self):

        while self.ser.in_waiting > 0:

            try:
                raw = self.ser.readline()
            except Exception as e:
                self.get_logger().error(f"Serial read error: {e}")
                return

            # Skip binary / invalid
            if b'$' not in raw:
                continue

            line = raw.decode('ascii', errors='ignore').strip()

            # Only valid NMEA sentences
            if not line.startswith('$'):
                continue

            # Ignore broken lines
            if '*' not in line:
                continue

            msg = Sentence()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = "gps"
            msg.sentence = line

            self.nmea_pub.publish(msg)

            # Only process GGA sentences for GPS fix
            if not line.startswith('$GNGGA'):
                return

            data = line.split(',')

            if data[2] == '' or data[3] == '' or data[4] == '' or data[5] == '' or data[8] == '' or data[9] == '':
                return

            lat = self.convert(data[2], data[3])
            lon = self.convert(data[4], data[5])
            alt = float(data[9])

            fix = NavSatFix()
            fix.header.stamp = self.get_clock().now().to_msg()
            fix.header.frame_id = "gps"

            fix.latitude = lat
            fix.longitude = lon
            fix.altitude = alt

            fix.status.status = int(data[6])  # GPS fix status (0 = invalid, 1 = GPS fix, 2 = DGPS fix, 4 = RTK_FIX, 5 = RTK_FLOAT)
            fix.position_covariance, fix.position_covariance_type = self.calculate_ros_navsat_covariance(fix.status.status, float(data[8]))

            self.fix_pub.publish(fix)

def main():
    rclpy.init()
    node = LC29HDA()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()