^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package lc29h_da_rtk_gps_driver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.1.0 (2026-06-12)
------------------
Changes from the original repo at https://github.com/amaltp13/GPS-RTK-Localisation
* Rename repo and package to lc29h_da_rtk_gps_driver to be more specific to what it is
* Retain the original LICENSE with the original author as the copyright holder
* Make the repo the package, vs original had the package as a subfolder, to standardize it and make it easier to install and use
* Fill out package.xml properly
* Update README.md to reflect the new repo name and provide instructions for installation and usage
* Add a CHANGELOG.rst file to document changes and updates to the package
* Update setup.py to include the new package name and any necessary dependencies
* Remove tmux script and replace with launchfile for easier use and better integration with ROS2 launch system
* Combine gps_bridge.py, gps_fix_node.py, gps_xy_node.py into a single lc29h_da_rtk_gps_driver.py node for simplicity and better organization (the tmux script ran them all anyway)
* Make topic names relative (e.g. 'nmea' instead of '/nmea') to allow for better integration with ROS2 namespaces and remapping
* Populate NavSatFix messages with covariance based on the GPS fix quality and HDOP from the GGA sentence
* Add altitude to gps_xy_node, along with origin_alt parameter, and include it in the PointStamped message (z = altitude - origin_alt) to provide 3D position information instead of just 2D

