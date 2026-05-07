# 06 — ROS2 集成

> 目标: 掌握ArduPilot与ROS2的集成方法

---

## 1. 架构概览

### 1.1 ArduPilot + ROS2 通信

```
┌──────────────┐     MAVLink     ┌──────────────┐
│  ArduPilot   │ ←─────────────→ │   ROS2       │
│              │   MAVROS/mavros2│   (DDS)      │
└──────────────┘                 └──────────────┘
```

ArduPilot 通过 MAVROS 或 mavros2 与 ROS2 通信:
- MAVLink 协议桥接
- 支持发布/订阅模式
- 支持服务调用

### 1.2 话题映射

| ArduPilot | ROS2 Topic | 类型 |
|-----------|------------|------|
| ATTITUDE | `/mavros/attitude` | geometry_msgs/PoseStamped |
| LOCAL_POSITION | `/mavros/local_position/pose` | geometry_msgs/PoseStamped |
| GLOBAL_POSITION | `/mavros/global_position/global` | sensor_msgs/NavSatFix |
| SET_POSITION_TARGET | `/mavros/setpoint_position/local` | geometry_msgs/PoseStamped |
| SET_ATTITUDE_TARGET | `/mavros/setpoint_attitude/attitude` | geometry_msgs/PoseStamped |

---

## 2. 环境搭建

### 2.1 安装 ROS2 Humble

```bash
# 设置源
sudo apt update && sudo apt install -y software-properties-common
sudo add-apt-repository universe
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 安装 ROS2
sudo apt update
sudo apt install -y ros-humble-desktop python3-colcon-common-extensions

# 设置环境
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 2.2 安装 MAVROS

```bash
# 安装 MAVROS
sudo apt install -y ros-humble-mavros ros-humble-mavros-extras

# 安装 GeographicLib 数据
sudo /opt/ros/humble/lib/mavros/install_geographiclib_datasets.sh
```

### 2.3 创建工作空间

```bash
mkdir -p ~/ardupilot_ws/src
cd ~/ardupilot_ws/src

# 创建功能包
ros2 pkg create --build-type ament_python ardupilot_control

# 编译
cd ~/ardupilot_ws
colcon build --symlink-install
source install/setup.bash
```

---

## 3. 启动 ArduPilot + ROS2

### 3.1 启动顺序

```bash
# 终端 1: 启动 ArduPilot SITL
cd ~/ardupilot/Tools/autotest
sim_vehicle.py -v ArduCopter --console --map

# 终端 2: 启动 MAVROS
ros2 launch mavros apm.launch fcu_url:=tcp://127.0.0.1:5760

# 终端 3: 启动 ROS2 节点
ros2 run ardupilot_control my_node
```

### 3.2 验证连接

```bash
# 查看 ROS2 话题
ros2 topic list

# 应该看到:
# /mavros/state
# /mavros/attitude
# /mavros/local_position/pose
# /mavros/setpoint_position/local
# ...

# 查看连接状态
ros2 topic echo /mavros/state
```

---

## 4. ROS2 Offboard 控制示例

### 4.1 基本 Offboard 节点

**offboard_control.py**:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State, CommandBool, SetMode
from mavros_msgs.srv import CommandBool, SetMode

import numpy as np


class OffboardControl(Node):
    def __init__(self):
        super().__init__('offboard_control')

        # 订阅
        self.state_sub = self.create_subscription(
            State, '/mavros/state', self.state_callback, 10)
        self.local_pos_sub = self.create_subscription(
            PoseStamped, '/mavros/local_position/pose',
            self.local_pos_callback, 10)

        # 发布
        self.local_pos_pub = self.create_publisher(
            PoseStamped, '/mavros/setpoint_position/local', 10)

        # 服务
        self.arming_client = self.create_client(
            CommandBool, '/mavros/cmd/arming')
        self.set_mode_client = self.create_client(
            SetMode, '/mavros/set_mode')

        # 状态
        self.current_state = None
        self.current_pose = None

        # 定时器 (20Hz)
        self.timer = self.create_timer(0.05, self.timer_callback)
        self.get_logger().info('Offboard Control 节点已启动')

    def state_callback(self, msg):
        self.current_state = msg

    def local_pos_callback(self, msg):
        self.current_pose = msg

    def arm(self):
        req = CommandBool.Request()
        req.value = True
        self.arming_client.call_async(req)
        self.get_logger().info('Arm 命令已发送')

    def set_offboard_mode(self):
        req = SetMode.Request()
        req.custom_mode = 'GUIDED'
        self.set_mode_client.call_async(req)
        self.get_logger().info('GUIDED 模式命令已发送')

    def publish_position(self, x, y, z, yaw=0.0):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map'
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z

        # 四元数 (yaw)
        msg.pose.orientation.w = np.cos(yaw / 2)
        msg.pose.orientation.z = np.sin(yaw / 2)

        self.local_pos_pub.publish(msg)

    def timer_callback(self):
        if self.current_state is None:
            return

        # 发送位置目标
        self.publish_position(0.0, 0.0, 5.0)

        # 检查是否需要切换模式
        if self.current_state.mode != 'GUIDED':
            self.set_offboard_mode()

        # 检查是否需要解锁
        if not self.current_state.armed:
            self.arm()

        # 输出状态
        if self.current_pose is not None:
            pos = self.current_pose.pose.position
            self.get_logger().info(
                f'位置: x={pos.x:.2f}, y={pos.y:.2f}, z={pos.z:.2f}',
                throttle_duration_sec=2.0)


def main(args=None):
    rclpy.init(args=args)
    node = OffboardControl()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('用户中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 4.2 运行

```bash
# 终端 1: ArduPilot SITL
sim_vehicle.py -v ArduCopter --console --map

# 终端 2: MAVROS
ros2 launch mavros apm.launch fcu_url:=tcp://127.0.0.1:5760

# 终端 3: ROS2 节点
python3 offboard_control.py
```

---

## 5. 圆形轨迹示例

```python
class CircleTrajectory(OffboardControl):
    def __init__(self):
        super().__init__()
        self.radius = 5.0
        self.omega = 0.3
        self.height = 5.0
        self.t = 0.0

    def timer_callback(self):
        if self.current_state is None:
            return

        # 圆形轨迹
        x = self.radius * np.cos(self.omega * self.t)
        y = self.radius * np.sin(self.omega * self.t)
        z = self.height
        yaw = self.omega * self.t + np.pi / 2

        self.publish_position(x, y, z, yaw)
        self.t += 0.05

        if self.current_state.mode != 'GUIDED':
            self.set_offboard_mode()
        if not self.current_state.armed:
            self.arm()
```

---

## 6. 坐标系转换

### 6.1 ArduPilot 坐标系

ArduPilot 使用 NED (北东地):
- X: 北 (North)
- Y: 东 (East)
- Z: 下 (Down)

### 6.2 ROS2 坐标系

ROS2 使用 ENU (东北天):
- X: 东 (East)
- Y: 北 (North)
- Z: 天 (Up)

### 6.3 转换函数

```python
def ned_to_enu(ned):
    """NED → ENU"""
    return [ned[1], ned[0], -ned[2]]

def enu_to_ned(enu):
    """ENU → NED"""
    return [enu[1], enu[0], -enu[2]]
```

---

## 7. DroneKit (Python)

### 7.1 安装

```bash
pip3 install dronekit
```

### 7.2 基本示例

```python
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# 连接
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

# 解锁
vehicle.arm(wait=True)

# 起飞
vehicle.simple_takeoff(10)

# 等待到达高度
while True:
    alt = vehicle.location.global_relative_frame.alt
    if alt >= 9.5:
        break
    time.sleep(1)

# 飞到目标点
target = LocationGlobalRelative(37.7749, -122.4194, 20)
vehicle.simple_goto(target)

# 等待
time.sleep(30)

# 降落
vehicle.mode = VehicleMode("LAND")
```

---

## 8. 常见问题

### Q: MAVROS 无法连接

```bash
# 检查 ArduPilot 端口
# SITL 默认 TCP 5760

# 检查 MAVROS 配置
ros2 launch mavros apm.launch fcu_url:=tcp://127.0.0.1:5760
```

### Q: ROS2 话题为空

```bash
# 检查 MAVROS 状态
ros2 topic echo /mavros/state

# 检查 ArduPilot 输出
# 在 MAVProxy 中查看
```

### Q: 坐标系搞混

```python
# ArduPilot: NED (北东地)
# ROS2: ENU (东北天)
# Z 轴符号相反!
```

---

## 下一步

→ [07 — 实机部署](07-hardware-deploy.md)
