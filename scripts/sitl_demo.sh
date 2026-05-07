#!/bin/bash
# ArduPilot SITL 快速演示脚本
# 用法: bash sitl_demo.sh [copter|plane|rover]

VEHICLE=${1:-copter}

echo "========================================="
echo "  ArduPilot SITL 演示"
echo "  载具: $VEHICLE"
echo "========================================="

cd ~/ardupilot/Tools/autotest

case $VEHICLE in
    copter)
        echo "启动四旋翼 SITL..."
        sim_vehicle.py -v ArduCopter --console --map
        ;;
    plane)
        echo "启动固定翼 SITL..."
        sim_vehicle.py -v ArduPlane --console --map
        ;;
    rover)
        echo "启动车辆 SITL..."
        sim_vehicle.py -v Rover --console --map
        ;;
    *)
        echo "未知载具: $VEHICLE (可选: copter, plane, rover)"
        exit 1
        ;;
esac
