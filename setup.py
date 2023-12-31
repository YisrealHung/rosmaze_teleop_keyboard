from setuptools import setup

package_name = 'rosmaze_teleop_keyboard'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ros2bot',
    maintainer_email='ros2bot@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'rosmaze_teleop_keyboard = rosmaze_teleop_keyboard.rosmaze_teleop_keyboard:main'
        ],
    },
)
