import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random
import threading
import socket
import subprocess
from flask import Flask, Response

app = Flask(__name__)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def generate_frames():
    cmd = [
        "rpicam-vid", "-t", "0", 
        "--codec", "mjpeg", 
        "--width", "640", "--height", "480", 
        "--framerate", "15", 
        "--inline", "-o", "-"
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    buffer = b''
    while True:
        chunk = process.stdout.read(4096)
        if not chunk:
            break
        buffer += chunk
        
        start = buffer.find(b'\xff\xd8')
        end = buffer.find(b'\xff\xd9')
        
        if start != -1 and end != -1 and end > start:
            jpg = buffer[start:end+2]
            buffer = buffer[end+2:]
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

class MockVisionNode(Node):
    def __init__(self):
        super().__init__('mock_vision_node')
        self.publisher_ = self.create_publisher(String, '/crop/disease_detected', 10)
        self.timer = self.create_timer(10.0, self.simulate_detection)
        
        threading.Thread(target=run_flask, daemon=True).start()
        
        local_ip = get_local_ip()
        self.get_logger().info("==================================================")
        self.get_logger().info(f"HARDWARE STREAM LIVE AT: http://{local_ip}:5000")
        self.get_logger().info("==================================================")

    def simulate_detection(self):
        disease = random.choice(["Early Blight", "Leaf Rust", "Powdery Mildew"])
        dosage = random.randint(15, 35)
        
        msg = String()
        msg.data = f"{disease}|{dosage}"
        self.publisher_.publish(msg)
        
        self.get_logger().info(f"Target Acquired: {disease} | Dosage: {dosage} ml (Sent to Supervisor)")

def main(args=None):
    rclpy.init(args=args)
    node = MockVisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
