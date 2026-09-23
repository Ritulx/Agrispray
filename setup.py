from setuptools import find_packages, setup

package_name = 'agrispray_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'flask', 'gpiozero'],
    zip_safe=True,
    # TODO: update with your details before publishing
    maintainer='Ritul',
    maintainer_email='your_email@example.com',
    description='AgriSpray-AI ROS 2 control package: vision/streaming node and motor + spray supervisor node.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mock_vision_node = agrispray_control.mock_vision_node:main',
            'robot_supervisor = agrispray_control.robot_supervisor:main',
        ],
    },
)
