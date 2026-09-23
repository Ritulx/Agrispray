import rclpy
from rclpy.node import Node
from gpiozero import OutputDevice
from std_msgs.msg import String
from time import sleep

class RobotSupervisor(Node):
    def __init__(self):
        super().__init__('robot_supervisor')
        
        self.ena = OutputDevice(12)
        self.in1 = OutputDevice(5)
        self.in2 = OutputDevice(6)
        self.enb = OutputDevice(18)
        self.in3 = OutputDevice(13)
        self.in4 = OutputDevice(19)

        self.subscription = self.create_subscription(
            String,
            '/crop/disease_detected',
            self.disease_callback,
            10
        )

        self.spraying = False
        self.loop_timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info('AgriSpray Supervisor Online. Motors driving forward.')

    def move_forward(self):
        self.in1.off(); self.in2.on(); self.ena.on()
        self.in3.off(); self.in4.on(); self.enb.on()

    def stop_motors(self):
        self.ena.off(); self.enb.off()
        self.in1.off(); self.in2.off()
        self.in3.off(); self.in4.off()

    def execute_spray_sequence(self, disease, dosage):
        self.spraying = True
        self.stop_motors()
        
        print(f"\n\033[93m{'='*50}\033[0m")
        print(f"\033[91m[ROBOT HALTED] Subject: {disease}\033[0m")
        print(f"\033[96m[VALVE OPEN]   Dispensing Dosage: {dosage} ml...\033[0m")
        
        sleep(3.0) 
        
        print(f"\033[92m[VALVE CLOSED] Spray complete. Resuming patrol.\033[0m")
        print(f"\033[93m{'='*50}\033[0m\n")
        
        self.spraying = False

    def disease_callback(self, msg: String):
        if not self.spraying:
            try:
                disease, dosage = msg.data.split('|')
                self.execute_spray_sequence(disease, dosage)
            except ValueError:
                self.get_logger().error("Malformed camera message received.")

    def control_loop(self):
        if not self.spraying:
            self.move_forward()

def main(args=None):
    rclpy.init(args=args)
    node = RobotSupervisor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_motors()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
