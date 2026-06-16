# LC29H(DA) RTK-GPS Driver

This repository explains how to use the Waveshare LC29H GNSS modules for high-precision GPS-based localization in ROS 2.

The project uses the following modules from the Waveshare LC29H series:

- **LC29H (DA)** – RTK rover module (main focus of this repository)
- **LC29H (BS)** – RTK base station module

This repository focuses specifically on using the **LC29H DA** module together with an external RTK correction service for centimeter-level positioning.

More information about the base station, how to set it up, and the system as a whole can be found offline in this repo at docs/LC29H GNSS Receivers.md
or online for the latest version [here](https://docs.google.com/document/d/1Ivht8Sh4g13TqvNfCvS9TXndvV_6op5G-JnbM73DQEw/edit?tab=t.0)

---

# What is RTK?

RTK (Real-Time Kinematic) positioning is a GNSS technique that improves standard GPS accuracy from meter-level precision to centimeter-level precision using correction data from a base station or RTK network.

### Launch arguments

- **port**: Serial port for GPS device (default: /dev/ttyUSB0)
- **baudrate**: Baudrate for GPS device (default: 115200)
- **ntrip_host**: NTRIP host (default: '')
- **ntrip_port**: NTRIP port (default: 2101)
- **ntrip_mountpoint**: NTRIP mountpoint (default: '')
- **ntrip_username**: NTRIP username (default: '')
- **ntrip_password**: NTRIP password (default: none)
- **ntrip_authenticate**: NTRIP authenticate (default: true)
- **ntrip_send_nmea**: NTRIP send_nmea (default: false)
- **namespace**: no description given (default: /)
- **node_name**: no description given (default: ntrip_client)
- **debug**: no description given (default: false)
- **host**: no description given (default: 20.185.11.35)
- **mountpoint**: no description given (default: VRS_RTCM3)
- **ntrip_version**: no description given (default: None)
- **user_agent**: HTTP User-Agent sent to the caster. Must start with "NTRIP ". rtk2go blocks the stock "NTRIP ntrip_client_ros". (default: NTRIP ros_ntrip_client)
- **ntrip_server_hz**: no description given (default: 1)
- **send_nmea**: Forward NMEA from the "nmea" topic up to the caster. Needed for virtual/relayed (VRS) mountpoints; set false for plain base stations to skip the subscription and avoid uploading position. (default: true)
- **authenticate**: no description given (default: True)
- **username**: no description given (default: user)
- **password**: no description given (default: pass)
- **ssl**: no description given (default: False)
- **cert**: no description given (default: None)
- **key**: no description given (default: None)
- **ca_cert**: no description given (default: None)
- **rtcm_message_package**: no description given (default: rtcm_msgs)
- **reconnect_attempt_wait_max_seconds**: Ceiling for the exponential reconnect backoff. Retries are persistent (never give up); raise this to reduce footprint during long caster outages (e.g. 600 for rtk2go DDoS/maintenance downtime). (default: 120)

```bash


```

You can modify the origin and transformation logic with parameters to the node, or to
the launch file.

---

# Build

Copy this package into your ROS 2 workspace:

```bash
cd ~/ros2_ws/src
git clone <repository_link>
```

Build and source the workspace:

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

# Nodes

This package provides these nodes.

## lc29h_da_rtk_gps_driver
The driver pulls corrections
from the rtcm topic and writes them to the serial port, and pulls
NMEA data from the serial port and publishes the NavSatFix message on
the gps/fix topic

### Topics

- **rtcm** (subscribe): rtcm_msgs.msg.Message messages containing correction
data
- **gps/fix** (publish): sensor_msgs.msg.NavSatFix messages containing fixes.
Covariance is populated with fixed values based on the fix type. The technique
is copied from the nmea_gps_driver. **Caution** testing has shown that the
fix type is not very reliable.
- **nmea** (publish): nmea_msgs.msg.Sentence messages containing fix and other NMEA data. This may be forwarded to a CORS corrections caster if needed.
data

### Parameters

- **port:** The serial port path to use for LC29H comms. Default: /dev/ttyUSB0.
- **baudrate:** The baudrate to use for LC29H comms. Default: 115200

### Example run command

```bash
ros2 run lc29h_da_rtk_gps_driver lc29h_da_rtk_gps_driver
```

## gps_xy_node
The gps_xy_node publishes X/Y/Z offsets from a local
origin on the gps/xy topic. The local origin is defined with parameters.

### Topics

- **gps/fix** (subscribe): sensor_msgs.msg.NavSatFix messages containing fixes
- **gps/xy** (publish): geometry_msgs.msg.PointStamped messages containing the
X/Y/Z position offset from the provided local origin

### Parameters

- **origin_lat:** the latitude of the local origin
- **origin_lon:** the longitude of the local origin
- **origin_alt:** the altitude of the local origin

### Example run command

```bash
ros2 run lc29h_da_rtk_gps_driver gps_xy_node --ros-args -p origin_lat:=33.000 -p origin_lon:=-96.000 -p origin_alt:=164.0
```

## print_pos
The print_pos node prints the current X/Y/Z offset position and
fix type, and in verbose mode, Lat/Lon/Alt and UTM Northing and Easting.
Verbose mode is set with a parameter.

### Topics

- **gps/fix** (subscribe): sensor_msgs.msg.NavSatFix messages containing fixes
- **gps/xy** (subscribe): geometry_msgs.msg.PointStamped messages containing 
the X/Y/Z position offset from the provided local origin

### Parameters

- **verbose:** whether to print lat/lon and UTM Easting/Northing in addition
to X/Y/Z and fix type. Default: false

### Example run command

```bash
ros2 run lc29h_da_rtk_gps_driver print_pos
ros2 run lc29h_da_rtk_gps_driver print_pos --ros-args -p verbose:=true
```

# Launch files

## lc29h_da_rtk_gps_driver.launch.py
The launch file starts these nodes:

- lc29h_da_rtk_gps_driver 
- gps_xy_node
- ntrip_client via its launchfile

**Note** You need to have built ntrip_client, or have it in the
ROS path for this launchfile to work. There are **80** forks of ntrip_client!
The parameters in this launch file are provided for the fork at:
https://github.com/PaulBouchier/ntrip_client
If you use a different ntrip_client you may need to adjust this launch file.

### Launch arguments

    'port':
        Serial port for GPS device
        (default: '/dev/ttyUSB0')

    'baudrate':
        Baudrate for GPS device
        (default: '115200')

    'ntrip_host':
        NTRIP host
        (default: '')

    'ntrip_port':
        NTRIP port
        (default: '2101')

    'ntrip_mountpoint':
        NTRIP mountpoint
        (default: '')

    'ntrip_username':
        NTRIP username
        (default: '')

    'ntrip_password':
        NTRIP password
        (default: 'none')

    'ntrip_authenticate':
        NTRIP authenticate
        (default: 'true')

    'ntrip_send_nmea':
        NTRIP send_nmea
        (default: 'false')

    'namespace':
        no description given
        (default: '/')

    'node_name':
        no description given
        (default: 'ntrip_client')

    'debug':
        no description given
        (default: 'false')

    'host':
        no description given
        (default: '20.185.11.35')

    'mountpoint':
        no description given
        (default: 'VRS_RTCM3')

    'ntrip_version':
        no description given
        (default: 'None')

    'user_agent':
        HTTP User-Agent sent to the caster. Must start with "NTRIP ". rtk2go blocks the stock "NTRIP ntrip_client_ros".
        (default: 'NTRIP ros_ntrip_client')

    'ntrip_server_hz':
        no description given
        (default: '1')

    'send_nmea':
        Forward NMEA from the "nmea" topic up to the caster. Needed for virtual/relayed (VRS) mountpoints; set false for plain base stations to skip the subscription and avoid uploading position.
        (default: 'true')

    'authenticate':
        no description given
        (default: 'True')

    'username':
        no description given
        (default: 'user')

    'password':
        no description given
        (default: 'pass')

    'ssl':
        no description given
        (default: 'False')

    'cert':
        no description given
        (default: 'None')

    'key':
        no description given
        (default: 'None')

    'ca_cert':
        no description given
        (default: 'None')

    'rtcm_message_package':
        no description given
        (default: 'rtcm_msgs')

    'reconnect_attempt_wait_max_seconds':
        Ceiling for the exponential reconnect backoff. Retries are persistent (never give up); raise this to reduce footprint during long caster outages (e.g. 600 for rtk2go DDoS/maintenance downtime).
        (default: '120')


```bash

```

After startup, the localization output will be available on:

```bash
/gps/xy
```

---

# RTK Status Reference

In the NavSatFix message published on gps/fix, the status.status field indicates the current positioning quality.

Example:
- `status=4` → RTK FIX achieved

| Status | Meaning | Typical Accuracy |
|---|---|---|
| 1 | Standard GPS | ~3 m |
| 2 | DGPS / SBAS | ~0.5 m to 2 m |
| 3 | PPS Fix | High precision (rarely used) |
| 4 | RTK FIX | ~1–3 cm |
| 5 | RTK FLOAT | ~10–50 cm |



<img width="738" height="448" alt="rtk sample" src="https://github.com/user-attachments/assets/b8c39d9c-c317-4c65-9611-f640a7e242b0" />


---

# Important Notes

- If you are not getting **RTK FIX** or **RTK FLOAT**, recheck:
  - Antenna connection
  - Internet connectivity
  - RTK correction service
  - Satellite visibility

- A clean open sky with a high satellite count significantly improves RTK performance.

- Since the LC29H supports only:
  - L1
  - L5

RTK FIX may not always be guaranteed under difficult conditions.

# Acknowledgements

This code was originated by Amal TP in his repo at https://github.com/amaltp13/GPS-RTK-Localisation#
