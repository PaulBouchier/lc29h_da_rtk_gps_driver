# LC29H(DA) RTK-GPS Driver

This repository explains how to use the Waveshare LC29H GNSS modules for high-precision GPS-based localization in ROS 2.

The project uses the following modules from the Waveshare LC29H series:

- **LC29H (DA)** – RTK rover module (main focus of this repository)
- **LC29H (BS)** – RTK base station module

This repository focuses specifically on using the **LC29H DA** module together with an external RTK correction service for centimeter-level positioning.

More information about the base station, how to set it up, and the system as a whole can be found
[here](https://docs.google.com/document/d/1Ivht8Sh4g13TqvNfCvS9TXndvV_6op5G-JnbM73DQEw/edit?tab=t.0)

---

# What is RTK?

RTK (Real-Time Kinematic) positioning is a GNSS technique that improves standard GPS accuracy from meter-level precision to centimeter-level precision using correction data from a base station or RTK network.

If you are new to RTK GNSS systems, refer to:

https://en.wikipedia.org/wiki/Real-time_kinematic_positioning

---

# Why This Repository?

Professional RTK GNSS systems are often expensive and difficult to configure. The Waveshare LC29H series provides a low-cost and easy-to-use alternative while still delivering impressive performance.

However, there is very little complete documentation available online for setting up these modules with ROS 2 and RTK correction services.

This repository aims to provide:
- A simple and working ROS 2 setup
- RTK correction integration
- GPS-to-map coordinate conversion
- Ready-to-use scripts
- Practical guidance from real-world testing

Using this setup, I successfully achieved:
- **RTK FIX status**
- Approximately **2 cm positioning accuracy**
- Reliable autonomous navigation over a **100 meter test area**
- Navigation without fully depending on wheel odometry

The modules are relatively affordable (~₹6000 per unit) and support:
- **L1 frequency band**
- **L5 frequency band**

---

# Supported Hardware

## LC29H Module Variants

### LC29H (BS)
- RTK Base Station module
- Generates RTK correction data
- Not covered in detail in this repository

### LC29H (DA)
- RTK Rover module
- Receives RTK corrections
- Main focus of this repository

![LC29H Module](https://github.com/user-attachments/assets/2348699e-1302-49d9-8992-aa4dd70cd898)


<img width="400" height="400" alt="F4DlbMcC4cMepO2el6jO-XoXY2m28JdMvWTssyQdON6Z3dLXqhr4-qA7TpOfD5_m-ebT_CsyMMC-RjXJaLUMMq8_-WQXTKCyLZLsSvwUj9zQ-A0_mf3U3g4gP4ZEeintF3FM-O1WEwqRVitiCoK_8vtbkhS59TG2NnNYhG9Uz10" src="https://github.com/user-attachments/assets/a5fb224c-bdf5-41bc-9edd-49fd3e35bb5c" />


More details about the boards:

https://www.waveshare.com/lc29h-gps-hat.htm

---

# RTK Correction Service

This project can use an external RTK correction subscription service:

https://www.rtkdata.com

They provide:
- A free one-month trial
- Affordable subscription plans (~₹5000/month)

It can also use the free correction service:

http://rtk2go.com

The provide:
- Free publish and subscribe to corrections

---

# Hardware Setup

Setup is straightforward:

1. Connect the **LC29H DA** module to your PC or Raspberry Pi using a micro-USB cable
2. Connect the GNSS antenna
3. Run the ROS 2 nodes provided in this repository

No additional hardware configuration is required for basic operation.

---

# Repository Structure

The repository contains three ROS 2 nodes and one launchfile:

1. 'lc29h_da_rtk_gps_driver.launch.py'

- Launches ntrip_client and lc29h_da_rtk_gps_driver and gps_xy_node.
  - ntrip_client comes from a separate package and gets corrections from an internet caster
  and publishes them on /rtcm
- Accepts these launch parameters:
  - **port** - default: /dev/ttyUSB0
  - **baudrate** - default: 115200

2. `lc29h_da_rtk_gps_driver.py`
Connects the GNSS module to your PC/Raspberry Pi through USB serial communication.
Writes corrections on topic /rtcm to the receiver, and reads GPS fix data from the
receiver. Publishes GPS data as NMEA sentences on topic 'nmea', and also as NavSatFix
messages on topic gps/fix. Accepts parameters to set port and baud rate for the USB serial
connection to the LC29H(DA)

---

3. `gps_xy_node.py`
Converts latitude and longitude coordinates into local X-Y coordinates for:
- ROS map frame
- World coordinates
- Autonomous navigation

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

Run the provided startup script:

```bash
./run_rtk_tmux.sh
```

After startup, the localization output will be available on:

```bash
/gps/xy
```

---

# RTK Status Reference

The number shown next to `E` in the GNSS output indicates the current positioning quality.

Example:
- `E=4` → RTK FIX achieved

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

---

# ROS 2 Compatibility

All code in this repository is developed and tested using:

- ROS 2 Humble

You are free to review, modify, and adapt the code according to your project requirements.
