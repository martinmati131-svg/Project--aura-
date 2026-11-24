#!/usr/bin/env python3
# Aura Core // Robotics & Edge-AI Subsystem
# Component: ROS 2 Serial Bridge Node for Breadboard Telemetry
# Target: ROS 2 Humble / Jazzy (Raspberry Pi 5 / Edge Workstation)

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import json

class BreadboardSerialBridge(Node):
    def __init__(self):
        super().__init__('breadboard_serial_bridge')
        
        # Declare parameters for serial port and baud rate
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        
        port = self.get_parameter('port').get_parameter_value().string_value
        baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value
        
        # Initialize Serial Connection
        try:
            self.serial_conn = serial.Serial(port, baudrate, timeout=1.0)
            self.get_logger().info(f"Connected to microcontroller on {port} at {baudrate} baud.")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial port {port}: {e}")
            raise e

        # ROS 2 Publisher
        self.publisher_ = self.create_publisher(String, 'breadboard/telemetry', 10)
        
        # Timer to poll serial buffer (e.g., 50Hz / 20ms)
        self.timer = self.create_timer(0.02, self.poll_serial_cb)

    def poll_serial_cb(self):
        if self.serial_conn.in_waiting > 0:
            try:
                line = self.serial_conn.readline().decode('utf-8').strip()
                if line.startswith("{") and line.endswith("}"):
                    # Validate JSON structure
                    data = json.loads(line)
                    
                    # Publish as a ROS 2 String message
                    msg = String()
                    msg.data = json.dumps(data)
                    self.publisher_.publish(msg)
                    
                    self.get_logger().debug(f"Published Telemetry: {msg.data}")
            except json.JSONDecodeError:
                self.get_logger().warn(f"Malformed JSON received: {line}")
            except Exception as e:
                self.get_logger().error(f"Serial read error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = BreadboardSerialBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

