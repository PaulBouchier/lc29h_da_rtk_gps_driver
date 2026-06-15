import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    port_arg = DeclareLaunchArgument(
        'port',
        default_value='/dev/ttyUSB0',
        description='Serial port for GPS device'
    )

    baudrate_arg = DeclareLaunchArgument(
        'baudrate',
        default_value='115200',
        description='Baudrate for GPS device'
    )

    # ntrip_client launch arguments (forwarded to included launch)
    ntrip_host_arg = DeclareLaunchArgument(
        'ntrip_host',
        default_value='',
        description='NTRIP host'
    )

    ntrip_port_arg = DeclareLaunchArgument(
        'ntrip_port',
        default_value='2101',
        description='NTRIP port'
    )

    ntrip_mountpoint_arg = DeclareLaunchArgument(
        'ntrip_mountpoint',
        default_value='',
        description='NTRIP mountpoint'
    )

    ntrip_username_arg = DeclareLaunchArgument(
        'ntrip_username',
        default_value='',
        description='NTRIP username'
    )

    ntrip_password_arg = DeclareLaunchArgument(
        'ntrip_password',
        default_value='none',
        description='NTRIP password'
    )

    ntrip_authenticate_arg = DeclareLaunchArgument(
        'ntrip_authenticate',
        default_value='true',
        description='NTRIP authenticate'
    )

    ntrip_send_nmea_arg = DeclareLaunchArgument(
        'ntrip_send_nmea',
        default_value='false',
        description='NTRIP send_nmea'
    )

    # Node 1: gps_xy_node
    # Command: ros2 run lc29h_da_rtk_gps_driver gps_xy_node --ros-args -p origin_lat:=33.1577935 -p origin_lon:=-96.9373084 -p origin_alt:=143.684
    gps_xy_node = Node(
        package='lc29h_da_rtk_gps_driver',
        executable='gps_xy_node',
        name='gps_xy_node',
        output='screen',
        parameters=[{
            'origin_lat': 33.15777543,
            'origin_lon': -96.93730808,
            'origin_alt': 169.54
        }]
    )

    # Node 2: lc29h_da_rtk_gps_driver
    # Command: ros2 run lc29h_da_rtk_gps_driver lc29h_da_rtk_gps_driver
    lc29h_da_rtk_gps_driver_node = Node(
        package='lc29h_da_rtk_gps_driver',
        executable='lc29h_da_rtk_gps_driver',
        name='lc29h_da_rtk_gps_driver',
        output='screen',
        parameters=[{
            'port': LaunchConfiguration('port'),
            'baudrate': LaunchConfiguration('baudrate')
        }]
    )

    # Launch file: ntrip_client ntrip_client_launch.py
    # Command: ros2 launch ntrip_client ntrip_client_launch.py host:=rtk2go.com port:=2101 mountpoint:=LittleElm_L1L5 username:=paul.bouchier@gmail.com password:=none authenticate:=true send_nmea:=false
    ntrip_client_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ntrip_client'),
                'ntrip_client_launch.py'
            )
        ),
        launch_arguments={
            'host': LaunchConfiguration('ntrip_host'),
            'port': LaunchConfiguration('ntrip_port'),
            'mountpoint': LaunchConfiguration('ntrip_mountpoint'),
            'username': LaunchConfiguration('ntrip_username'),
            'password': LaunchConfiguration('ntrip_password'),
            'authenticate': LaunchConfiguration('ntrip_authenticate'),
            'send_nmea': LaunchConfiguration('ntrip_send_nmea')
        }.items()
    )

    return LaunchDescription([
        port_arg,
        baudrate_arg,
        ntrip_host_arg,
        ntrip_port_arg,
        ntrip_mountpoint_arg,
        ntrip_username_arg,
        ntrip_password_arg,
        ntrip_authenticate_arg,
        ntrip_send_nmea_arg,
        gps_xy_node,
        lc29h_da_rtk_gps_driver_node,
        ntrip_client_launch
    ])
