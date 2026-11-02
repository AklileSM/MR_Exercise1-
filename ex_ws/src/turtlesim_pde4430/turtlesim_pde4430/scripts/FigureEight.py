import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class FigureEight(Node):
    def __init__(self):
        super().__init__('figure_eight')
        self.radius = 2.0  # Radius of each loop of the 8 in metres
        self.linear_speed = 1.0  # Forward speed in m/s
        self.angular_speed = self.linear_speed / self.radius  # w = v / r keeps a fixed radius
        self.direction = 1.0  # +1 turns left (anticlockwise), -1 turns right (clockwise)
        self.turned = 0.0  # Heading change accumulated in the current loop
        self.last_theta = None
        self.loops_done = 0  # Two loops (one left, one right) make one 8
        self.finished = False
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)  # Publisher sending Twist msgs to turtle1's velocity topic
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)  # Pose feedback to know when a loop is complete
        self.timer = self.create_timer(0.1, self.tick)  # Call self.tick every 0.1 s (10 Hz)

    def on_pose(self, pose):  # Pose callback, tracks how far the turtle has turned
        if self.last_theta is not None:
            delta = pose.theta - self.last_theta
            delta = math.atan2(math.sin(delta), math.cos(delta))  # Wrap to [-pi, pi] so crossing +/-pi is handled
            self.turned += abs(delta)
        self.last_theta = pose.theta

        if self.turned >= 2 * math.pi:  # Full loop done
            self.loops_done += 1
            self.turned = 0.0
            if self.loops_done >= 2:  # Both loops drawn, the 8 is complete
                self.stop()
            else:  # Switch to the other loop of the 8
                self.direction *= -1.0

    def stop(self):  # Stop sending motion commands and halt the turtle
        if self.finished:
            return
        self.timer.cancel()
        self.pub.publish(Twist())  # All-zero Twist stops the turtle immediately
        self.finished = True
        self.get_logger().info('Figure 8 complete')

    def tick(self):  # Timer callback
        if self.finished:
            return
        msg = Twist()
        msg.linear.x = self.linear_speed  # Move forward along the turtle's x-axis
        msg.angular.z = self.direction * self.angular_speed  # Turn left or right depending on the current loop
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = FigureEight()
    while rclpy.ok() and not node.finished:  # Spin until the 8 is drawn
        rclpy.spin_once(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
