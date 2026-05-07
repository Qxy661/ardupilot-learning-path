#!/bin/bash
# sitl_launch.sh — ArduPilot SITL 启动脚本
# 支持多种载具和配置

set -e

# 默认参数
VEHICLE="ArduCopter"
CONSOLE=true
MAP=true
GAZEBO=false
HEADLESS=false
INSTANCE=0
SPEEDUP=1

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --vehicle|-v)
            VEHICLE="$2"
            shift 2
            ;;
        --no-console)
            CONSOLE=false
            shift
            ;;
        --no-map)
            MAP=false
            shift
            ;;
        --gazebo)
            GAZEBO=true
            shift
            ;;
        --headless)
            HEADLESS=true
            shift
            ;;
        --instance|-i)
            INSTANCE="$2"
            shift 2
            ;;
        --speedup)
            SPEEDUP="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

# 检查 ArduPilot 目录
APM_DIR="$HOME/ardupilot"
if [ ! -d "$APM_DIR" ]; then
    echo "错误: ArduPilot 目录不存在: $APM_DIR"
    echo "请先运行 setup_ardupilot.sh"
    exit 1
fi

cd "$APM_DIR/Tools/autotest"

# 构建命令
CMD="sim_vehicle.py -v $VEHICLE"

if [ "$CONSOLE" = true ]; then
    CMD="$CMD --console"
fi

if [ "$MAP" = true ] && [ "$HEADLESS" = false ]; then
    CMD="$CMD --map"
fi

if [ "$GAZEBO" = true ]; then
    CMD="$CMD --gazebo"
fi

if [ "$HEADLESS" = true ]; then
    CMD="$CMD --no-map"
fi

if [ "$INSTANCE" -gt 0 ]; then
    CMD="$CMD --instance $INSTANCE"
fi

if [ "$SPEEDUP" -ne 1 ]; then
    CMD="$CMD --speedup $SPEEDUP"
fi

echo "========================================"
echo "启动 ArduPilot SITL"
echo "========================================"
echo "载具: $VEHICLE"
echo "控制台: $CONSOLE"
echo "地图: $MAP"
echo "Gazebo: $GAZEBO"
echo "实例: $INSTANCE"
echo "加速: ${SPEEDUP}x"
echo "命令: $CMD"
echo "========================================"

# 启动
$CMD
