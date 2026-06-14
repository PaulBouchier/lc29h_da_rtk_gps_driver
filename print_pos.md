# Oveview

I want a ROS2 node that subscribes to GPS data and prints it periodically. The node should be called print_pos.py.
Make the appropriate changes to setup.py and other build files.

# Detailed specification

The node should subscribe to /gps/fix (type NavSatFix) and look at the status.status field to determine the fix type.
Here is the decode of the field:
GPS fix status (0 = invalid, 1 = GPS fix, 2 = DGPS fix, 4 = RTK_FIX, 5 = RTK_FLOAT)
This topic is published by lc29h_da_rtk_gps_driver/lc29h_da_rtk_gps_driver.py

The code should also subscribe to /gps/xy which is published by /home/bouchier/ros2_ws/src/lc29h_da_rtk_gps_driver/lc29h_da_rtk_gps_driver/gps_xy_node.py to determine the x/y/z pose.

The code should print a 1-line summary every 4 seconds which contains the following info. Abbreviation is fine - it needs to be brief.
fix_type, x, y, z


