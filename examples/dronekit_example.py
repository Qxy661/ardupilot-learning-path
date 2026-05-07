#!/usr/bin/env python3
"""
DroneKit 控制示例

使用 DroneKit 连接 ArduPilot SITL, 测试基本控制

运行方式:
  终端1: sim_vehicle.py -v ArduCopter --console --map
  终端2: python3 dronekit_example.py
"""

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math


def connect_vehicle():
    """连接到 ArduPilot"""
    print("等待连接...")
    vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)
    print(f"已连接: {vehicle.version}")
    return vehicle


def arm_and_takeoff(vehicle, altitude=10):
    """解锁并起飞"""
    print("预飞检查...")
    while not vehicle.is_armable:
        print("  等待飞控就绪...")
        time.sleep(1)

    print("切换到 GUIDED 模式...")
    vehicle.mode = VehicleMode("GUIDED")
    while vehicle.mode.name != "GUIDED":
        time.sleep(1)

    print("解锁电机...")
    vehicle.arm(wait=True)

    print(f"起飞到 {altitude}m...")
    vehicle.simple_takeoff(altitude)

    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(f"  当前高度: {alt:.1f}m")
        if alt >= altitude * 0.9:
            break
        time.sleep(1)

    print("到达目标高度")


def goto(vehicle, lat, lon, alt):
    """飞到目标点"""
    print(f"飞到目标点: {lat}, {lon}, {alt}m")
    target = LocationGlobalRelative(lat, lon, alt)
    vehicle.simple_goto(target)

    # 等待到达
    while True:
        current = vehicle.location.global_relative_frame
        distance = get_distance_metres(current, target)
        print(f"  距离目标: {distance:.1f}m")
        if distance < 1.0:
            break
        time.sleep(1)

    print("到达目标点")


def get_distance_metres(aLocation1, aLocation2):
    """计算两点距离 (米)"""
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5


def land(vehicle):
    """降落"""
    print("降落中...")
    vehicle.mode = VehicleMode("LAND")
    while vehicle.mode.name != "LAND":
        time.sleep(1)

    while True:
        alt = vehicle.location.global_relative_frame.alt
        if alt < 0.3:
            break
        time.sleep(1)

    print("已着陆")


def circle(vehicle, radius=10, altitude=10, duration=30):
    """飞圆形轨迹"""
    print(f"开始圆形轨迹: r={radius}m, h={altitude}m, t={duration}s")

    center = vehicle.location.global_relative_frame
    start_time = time.time()

    while time.time() - start_time < duration:
        angle = (time.time() - start_time) * 0.3  # 角速度
        lat = center.lat + radius * math.cos(angle) / 111320
        lon = center.lon + radius * math.sin(angle) / (111320 * math.cos(math.radians(center.lat)))

        target = LocationGlobalRelative(lat, lon, altitude)
        vehicle.simple_goto(target)

        time.sleep(0.1)

    print("圆形轨迹完成")


def get_status(vehicle):
    """获取状态"""
    print(f"模式: {vehicle.mode.name}")
    print(f"解锁: {vehicle.armed}")
    print(f"GPS: {vehicle.gps_0.fix_type}")
    print(f"电池: {vehicle.battery.voltage:.1f}V")
    print(f"位置: {vehicle.location.global_relative_frame}")


def main():
    vehicle = connect_vehicle()

    try:
        # 获取状态
        get_status(vehicle)

        # 解锁并起飞
        arm_and_takeoff(vehicle, altitude=10)

        # 悬停 5 秒
        print("悬停 5 秒...")
        time.sleep(5)

        # 飞圆形轨迹
        circle(vehicle, radius=10, altitude=10, duration=30)

        # 降落
        land(vehicle)

        # 上锁
        vehicle.armed = False
        while vehicle.armed:
            time.sleep(1)
        print("已上锁")

    except KeyboardInterrupt:
        print("用户中断, 降落中...")
        land(vehicle)
    except Exception as e:
        print(f"错误: {e}")
        land(vehicle)
    finally:
        vehicle.close()


if __name__ == '__main__':
    main()
