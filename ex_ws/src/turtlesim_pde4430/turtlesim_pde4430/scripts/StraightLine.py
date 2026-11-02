import rclpy  
from rclpy.node import Node  
from geometry_msgs.msg import Twist


class StraightLine(Node):  
    def __init__(self): 
        super().__init__('straight_line')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)  # Publisher sending Twist msgs to turtle1's velocity topic 
        self.timer = self.create_timer(0.1, self.tick)  # Call self.tick every 0.1 s (10 Hz)

    def tick(self):  # Timer callback,
        msg = Twist()  
        msg.linear.x = 1.0  # Set forward speed to 1.0 m/s along the turtle's x-axis
        self.pub.publish(msg) 


def main():  
    rclpy.init() 
    rclpy.spin(StraightLine()) 
    rclpy.shutdown()  
