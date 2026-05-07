#!/usr/bin/env python3
"""
ArduPilot MAVLink 通信示例

使用 pymavlink 连接 ArduPilot SITL, 测试基本命令

运行方式:
  终端1: sim_vehicle.py -v ArduCopter --console --map
  终端2: python3 mavlink_example.py
"""

from pymavlink import mavutil
import time


def connect():
    """连接到 ArduPilot"""
    print("等待连接...")
    master = mavutil.mavlink_connection('tcp:127.0.0.1:5760')
    master.wait_heartbeat()
    print(f"已连接: system_id={master.target_system}")
    return master


def arm(master):
    """解锁电机"""
    print("解锁电机...")
    master.arducopter_arm()
    master.motors_armed_wait()
    print("已解锁")


def disarm(master):
    """上锁电机"""
    print("上锁电机...")
    master.arducopter_disarm()
    master.motors_disarmed_wait()
    print("已上锁")


def takeoff(master, altitude=10):
    """起飞"""
    print(f"起飞到 {altitude}m...")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0, 0, 0, 0, 0, 0, 0, altitude
    )
    # 等待到达高度
    while True:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        alt = msg.relative_alt / 1000.0
        print(f"  当前高度: {alt:.1f}m")
        if alt >= altitude * 0.9:
            break
        time.sleep(1)
    print("到达目标高度")


def goto(master, lat, lon, alt):
    """飞到目标点"""
    print(f"飞到目标点: {lat}, {lon}, {alt}m")
    master.mav.mission_item_send(
        master.target_system,
        master.target_component,
        0,  # 序号
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        2,  # 当前航点
        0,  # 自动继续
        0, 0, 0, 0,
        lat, lon, alt
    )


def land(master):
    """降落"""
    print("降落中...")
    master.set_mode('LAND')
    # 等待着陆
    while True:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        alt = msg.relative_alt / 1000.0
        if alt < 0.3:
            break
        time.sleep(1)
    print("已着陆")


def get_status(master):
    """获取状态"""
    msg = master.recv_match(type='HEARTBEAT', blocking=True, timeout=3)
    if msg:
        mode = mavutil.mode_string_v10(msg)
        armed = msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
        print(f"模式: {mode}, 解锁: {armed}")


def main():
    master = connect()

    try:
        # 获取状态
        get_status(master)

        # 解锁
        arm(master)

        # 起飞
        takeoff(master, altitude=10)

        # 悬停 10 秒
        print("悬停 10 秒...")
        time.sleep(10)

        # 飞到目标点
        # 注意: 这里需要替换为实际的坐标
        # goto(master, 37.7749, -122.4194, 20)

        # 降落
        land(master)

        # 上锁
        disarm(master)

    except KeyboardInterrupt:
        print("用户中断, 降落中...")
        land(master)
        disarm(master)
    except Exception as e:
        print(f"错误: {e}")
        land(master)


if __name__ == '__main__':
    main()
