import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Circle(Node):
    def __init__(self):
        super().__init__('circle')
        self.radius = 2.0  
        self.linear_speed = 1.0  
        self.angular_speed = self.linear_speed / self.radius  # w = v / r keeps a fixed radius
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10) 
        self.timer = self.create_timer(0.1, self.tick)  

    def tick(self):  # Timer callback
        msg = Twist()
        msg.linear.x = self.linear_speed 
        msg.angular.z = self.angular_speed  
        self.pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(Circle())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
