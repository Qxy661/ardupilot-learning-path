# 00 — 环境搭建

> 目标: 在WSL2 Ubuntu上搭建ArduPilot开发环境, 完成首次SITL仿真飞行

---

## 1. 安装WSL2

在Windows终端(PowerShell管理员)中执行:

```powershell
wsl --install -d Ubuntu-22.04
```

重启后设置用户名和密码。

验证:
```bash
wsl --list --verbose
# 应显示 Ubuntu-22.04 Running 2
```

---

## 2. 安装ArduPilot工具链

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y git python3-pip python3-venv

# 克隆ArduPilot (必须用 --recursive!)
cd ~
git clone https://github.com/ArduPilot/ardupilot.git --recursive
cd ardupilot

# 运行官方安装脚本
Tools/environment_install/install-prereqs-ubuntu.sh -y

# 重新加载环境变量
source ~/.bashrc
```

**关键点**: `--recursive` 会拉取所有子模块, 不加的话会缺失重要库。

---

## 3. 首次编译

```bash
cd ~/ardupilot

# 编译四旋翼SITL目标
./waf configure --board sitl
./waf copter
```

编译成功标志: 看到 `Build successful`

编译时间: 首次约10-15分钟, 后续增量编译约1-2分钟。

---

## 4. 启动SITL仿真

### 4.1 标准启动 (推荐)

```bash
sim_vehicle.py -v ArduCopter --console --map
```

成功标志:
- MAVProxy 控制台出现
- 地图窗口弹出
- `APM: ArduCopter V4.x.x` 消息

### 4.2 常用参数

```bash
# 指定初始位置
sim_vehicle.py -v ArduCopter --console --map --location "37.7749,-122.4194,10,0"

# 无GUI模式
sim_vehicle.py -v ArduCopter --console --no-map

# 指定端口
sim_vehicle.py -v ArduCopter --console --map --out udp:127.0.0.1:14550

# 使用 Gazebo
sim_vehicle.py -v ArduCopter --console --map --gazebo
```

### 4.3 其他载具

```bash
# 固定翼
sim_vehicle.py -v ArduPlane --console --map

# 车辆
sim_vehicle.py -v Rover --console --map

# 潜艇
sim_vehicle.py -v ArduSub --console --map
```

---

## 5. 验证飞行

在 MAVProxy 控制台中:

```bash
# 查看当前状态
status

# 解锁
arm throttle

# 起飞到10米
takeoff 10

# 等待几秒, 观察地图上无人机起飞

# 切换到Guided模式 (点击地图上的点)
mode guided

# 降落
mode land

# 上锁
disarm
```

---

## 6. 安装Mission Planner

### 6.1 Windows安装

1. 下载: https://firmware.ardupilot.org/Tools/MissionPlanner/MissionPlanner-latest.msi
2. 运行安装程序
3. 连接: 选择 UDP, 端口 14550

### 6.2 Linux (Wine)

```bash
# 安装 Wine
sudo apt install wine64

# 下载 Mission Planner
wget https://firmware.ardupilot.org/Tools/MissionPlanner/MissionPlanner-latest.msi

# 运行
wine msiexec /i MissionPlanner-latest.msi
```

---

## 7. 安装DroneKit (可选, Python控制)

```bash
pip3 install dronekit

# 或从源码
git clone https://github.com/dronekit/dronekit-python.git
cd dronekit-python
pip3 install -e .
```

---

## 8. 安装MAVProxy (调试用)

```bash
pip3 install mavproxy

# 连接到SITL
mavproxy.py --master=tcp:127.0.0.1:5760
```

---

## 常见问题

### Q: `./waf` 报错找不到子模块

```bash
# 解决: 重新拉取子模块
cd ~/ardupilot
git submodule update --init --recursive
```

### Q: Gazebo窗口不弹出

```bash
# 检查WSLg是否启用
echo $DISPLAY
# 应该输出类似 :0 的值

# 如果为空, 更新WSL2
wsl --update
```

### Q: 起飞后翻车

默认参数可能不适合你的仿真环境。先继续学习, 后面调参章节会解决。

### Q: 编译内存不足

```bash
# 减少并行编译数
./waf copter -j2
```

### Q: sim_vehicle.py 找不到

```bash
# 检查 PATH
echo $PATH | grep ardupilot

# 如果没有, 手动添加
export PATH=$PATH:$HOME/ardupilot/Tools/autotest
```

---

## 下一步

→ [01 — ArduPilot架构解析](01-architecture.md)
