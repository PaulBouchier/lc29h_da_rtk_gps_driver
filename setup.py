import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'lc29h_da_rtk_gps_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bouchier',
    maintainer_email='paul.bouchier@gmail.com',
    description='TODO: Package description',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'lc29h_da_rtk_gps_driver = lc29h_da_rtk_gps_driver.lc29h_da_rtk_gps_driver:main',
            'gps_xy_node = lc29h_da_rtk_gps_driver.gps_xy_node:main',
            'print_pos = lc29h_da_rtk_gps_driver.print_pos:main'
        ],
    },
)
