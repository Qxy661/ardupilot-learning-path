#!/usr/bin/env python3
"""
ROS2 Offboard 控制示例 (ArduPilot)

使用 MAVROS 连接 ArduPilot SITL, 实现 Offboard 控制

运行方式:
  终端1: sim_vehicle.py -v ArduCopter --console --map
  终端2: ros2 launch mavros apm.launch fcu_url:=tcp://127.0.0.1:5760
  终端3: python3 ros2_offboard.py
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.msg import State
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

        # 圆形轨迹参数
        self.radius = 5.0
        self.omega = 0.3
        self.height = 5.0
        self.t = 0.0

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

    def set_guided_mode(self):
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

        # 计算圆形轨迹
        x = self.radius * np.cos(self.omega * self.t)
        y = self.radius * np.sin(self.omega * self.t)
        z = self.height
        yaw = self.omega * self.t + np.pi / 2

        # 发送位置目标
        self.publish_position(x, y, z, yaw)
        self.t += 0.05

        # 检查是否需要切换模式
        if self.current_state.mode != 'GUIDED':
            self.set_guided_mode()

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
