import sys

import geometry_msgs.msg
import rclpy

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


msg = """

For DifferentialMotion mode : 
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For OmniMotion mode :
---------------------------
   r    t    y
   f    g    h
   v    b    n


anything else : stop

q/z : increase/decrease Linear velocity in x by 10%
w/x : increase/decrease Linear velocity in y by 10%
e/c : increase/decrease angular velocity in z by 10%

CTRL-C to quit
"""

moveBindings = {
    'i': (1, 0, 0, 0),
    ',': (-1, 0, 0, 0),
    'j': (0, 0, 0, 1),
    'l': (0, 0, 0, -1),
    'u': (1, 0, 0, 1),
    'o': (1, 0, 0, -1),
    'm': (-1, 0, 0, -1),
    '.': (-1, 0, 0, 1),
    't': (1, 0, 0, 0),
    'b': (-1, 0, 0, 0),
    'f': (0, 1, 0, 0),
    'h': (0, -1, 0, 0),
    'r': (0.7, 0.7, 0, 0),
    'y': (0.7, -0.7, 0, 0),
    'v': (-0.7, 0.7, 0, 0),
    'n': (-0.7, -0.7, 0, 0),
    
}

speedBindings = {
    'q': (1.1),
    'z': (.9),
    'w': (1.1),
    'x': (.9),
    'e': (1.1),
    'c': (.9),
}


def getKey(settings):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)


def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def vels(linear_x, linear_y, angular_z):
    return 'currently: lx {} ly {} az {}'.format(linear_x, linear_y, angular_z)


def main():
    settings = saveTerminalSettings()

    rclpy.init()

    node = rclpy.create_node('rosmaze_teleop_keyboard')
    pub = node.create_publisher(geometry_msgs.msg.Twist, 'cmd_vel', 10)

    linear_x = 0.10
    linear_y = 0.10
    angular_z = 0.35
    x = 0.0
    y = 0.0
    z = 0.0
    th = 0.0
    status = 0.0

    try:
        print(msg)
        print(vels(linear_x, linear_y, angular_z))
        while True:
            key = getKey(settings)
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                y = moveBindings[key][1]
                z = moveBindings[key][2]
                th = moveBindings[key][3]
            elif key in speedBindings.keys():
                if key == 'q' or key == 'z':
                    linear_x = round(linear_x * speedBindings[key], 3)
                elif key == 'w' or key == 'x':
                    linear_y = round(linear_y * speedBindings[key], 3)
                elif key == 'e' or key == 'c':
                    angular_z = round(angular_z * speedBindings[key], 3)

                print(vels(linear_x, linear_y, angular_z))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15
            else:
                x = 0.0
                y = 0.0
                z = 0.0
                th = 0.0
                if (key == '\x03'):
                    break

            twist = geometry_msgs.msg.Twist()
            twist.linear.x = x * linear_x
            twist.linear.y = y * linear_y
            twist.linear.z = z * 0.0
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = th * angular_z
            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        pub.publish(twist)

        restoreTerminalSettings(settings)


if __name__ == '__main__':
    main()
