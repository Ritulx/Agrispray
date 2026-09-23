# AgriSpray-AI — ROS 2 Control Package

A multi-crop AI-enabled ground agribot for plant-level disease/pest detection and targeted spraying.
This repository contains the ROS 2 (Jazzy) `agrispray_control` package: a vision/streaming node
and a motor + spray supervisor node, running on a Raspberry Pi 5.

## Package layout

```
agrispray_ws/
└── src/
    └── agrispray_control/
        ├── agrispray_control/
        │   ├── __init__.py
        │   ├── mock_vision_node.py     # camera capture, MJPEG stream, detection publisher
        │   └── robot_supervisor.py     # motor control (L298N) + spray sequence supervisor
        ├── resource/agrispray_control
        ├── package.xml
        ├── setup.cfg
        ├── setup.py
        └── requirements.txt
```

## Nodes

- **mock_vision_node** — captures frames via `rpicam-vid`, serves a live MJPEG stream over
  Flask at `http://<pi-ip>:5000/`, and periodically publishes a simulated detection
  (`"<disease>|<dosage>"`) to `/crop/disease_detected`.
- **robot_supervisor** — drives the differential-drive chassis via an L298N motor driver
  (`gpiozero` on BCM pins 12/5/6/18/13/19), subscribes to `/crop/disease_detected`, halts the
  rover on a detection, and runs the spray sequence.

## Current implementation status

| Subsystem | Status |
|---|---|
| Camera capture (Pi Camera Module 3 + `rpicam-vid`) | Implemented and tested |
| MJPEG live streaming (Flask) | Implemented and tested |
| L298N motor driver / differential-drive actuation | Implemented and tested |
| Ultrasonic obstacle sensor | Implemented and tested |
| ROS 2 detection → motor-halt trigger (`/crop/disease_detected`) | Implemented and tested |
| Relay + 12V spray pump / nozzle actuation | Hardware wiring complete; **not yet functionally tested**. `execute_spray_sequence()` currently logs and times the spray window in software but does not yet drive a physical relay output. |

## Build

```bash
cd ~/agrispray_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Run

```bash
# Terminal 1
ros2 run agrispray_control mock_vision_node

# Terminal 2
ros2 run agrispray_control robot_supervisor
```

Open `http://<raspberry-pi-ip>:5000/` in a browser on the same network to view the live feed.

## License

Apache-2.0 (see `package.xml`).
