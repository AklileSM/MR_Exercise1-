import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Circle(Node):
    def __init__(self):
        super().__init__('circle')
        self.radius = 2.0  # Circle radius in metres
        self.linear_speed = 1.0  # Forward speed in m/s
        self.angular_speed = self.linear_speed / self.radius  # w = v / r keeps a fixed radius
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)  # Publisher sending Twist msgs to turtle1's velocity topic
        self.timer = self.create_timer(0.1, self.tick)  # Call self.tick every 0.1 s (10 Hz)

    def tick(self):  # Timer callback
        msg = Twist()
        msg.linear.x = self.linear_speed  # Move forward along the turtle's x-axis
        msg.angular.z = self.angular_speed  # Turn at a constant rate around the z-axis
        self.pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(Circle())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
