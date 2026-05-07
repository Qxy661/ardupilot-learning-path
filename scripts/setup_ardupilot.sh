#!/bin/bash
# setup_ardupilot.sh — ArduPilot 一键环境搭建脚本
# 适用于 Ubuntu 22.04 (WSL2 或原生)

set -e

echo "========================================"
echo "ArduPilot 开发环境一键搭建"
echo "========================================"

# 检查系统
if ! grep -q "Ubuntu 22.04" /etc/os-release; then
    echo "警告: 此脚本针对 Ubuntu 22.04, 其他版本可能需要调整"
fi

# 更新系统
echo "[1/5] 更新系统..."
sudo apt update && sudo apt upgrade -y

# 安装基础工具
echo "[2/5] 安装基础工具..."
sudo apt install -y git python3-pip python3-venv

# 克隆 ArduPilot
echo "[3/5] 克隆 ArduPilot 代码..."
if [ -d "$HOME/ardupilot" ]; then
    echo "ardupilot 目录已存在, 跳过克隆"
else
    cd ~
    git clone https://github.com/ArduPilot/ardupilot.git --recursive
fi

# 运行官方安装脚本
echo "[4/5] 运行 ArduPilot 安装脚本..."
cd ~/ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y

# 重新加载环境变量
echo "[5/5] 重新加载环境变量..."
source ~/.bashrc

echo ""
echo "========================================"
echo "ArduPilot 环境搭建完成!"
echo "========================================"
echo ""
echo "启动 SITL 仿真:"
echo "  cd ~/ardupilot/Tools/autotest"
echo "  sim_vehicle.py -v ArduCopter --console --map"
echo ""
echo "启动固定翼:"
echo "  sim_vehicle.py -v ArduPlane --console --map"
echo ""
