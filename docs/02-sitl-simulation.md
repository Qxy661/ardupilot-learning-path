# 02 — SITL 仿真深入

> 目标: 掌握ArduPilot SITL仿真的完整使用方法

---

## 1. SITL 架构

### 1.1 什么是SITL

SITL (Software In The Loop) = 纯软件仿真:
```
┌──────────────┐     TCP      ┌──────────────┐
│ ArduPilot SITL│ ←──────────→ │   Gazebo     │
│  (飞控代码)   │  MAVLink     │  (物理仿真)   │
└──────┬───────┘              └──────────────┘
       │ TCP 5760
       ▼
┌──────────────┐
│ Mission Planner│
│  (地面站)     │
└──────────────┘
```

### 1.2 启动方式

| 方式 | 命令 | 特点 |
|------|------|------|
| 内置模型 | `sim_vehicle.py -v ArduCopter` | **推荐**, 简单 |
| Gazebo | `sim_vehicle.py -v ArduCopter --gazebo` | 3D可视化 |
| jMAVSim | `sim_vehicle.py -v ArduCopter --jmavsim` | 轻量 |
| AirSim | `sim_vehicle.py -v ArduCopter --aircraft Iris` | 高保真 |

---

## 2. sim_vehicle.py 使用

### 2.1 基本启动

```bash
cd ~/ardupilot/Tools/autotest

# 启动四旋翼
sim_vehicle.py -v ArduCopter --console --map
```

### 2.2 常用参数

```bash
# 指定初始位置 (纬度, 经度, 高度, 航向)
sim_vehicle.py -v ArduCopter --console --map \
    --location "37.7749,-122.4194,10,0"

# 无GUI模式 (CI/测试)
sim_vehicle.py -v ArduCopter --console --no-map

# 输出到其他地面站
sim_vehicle.py -v ArduCopter --console --map \
    --out udp:127.0.0.1:14550

# 自定义速度
sim_vehicle.py -v ArduCopter --console --map \
    --speedup 2

# 使用 Gazebo
sim_vehicle.py -v ArduCopter --console --map --gazebo

# 指定实例 (多机)
sim_vehicle.py -v ArduCopter --console --map --instance 0
```

### 2.3 其他载具

```bash
# 固定翼
sim_vehicle.py -v ArduPlane --console --map

# 车辆
sim_vehicle.py -v Rover --console --map

# 潜艇
sim_vehicle.py -v ArduSub --console --map

# 直升机
sim_vehicle.py -v ArduHeli --console --map
```

---

## 3. MAVProxy 控制台

### 3.1 常用命令

```bash
# 查看状态
status

# 解锁
arm throttle

# 起飞
takeoff 10

# 切换模式
mode loiter
mode rtl
mode auto

# 查看参数
param show ATC_RAT_RLL_P

# 设置参数
param set ATC_RAT_RLL_P 0.15

# 查看航点
wp list

# 加载航点
wp load mission.txt

# 保存航点
wp save mission.txt
```

### 3.2 模块加载

```bash
# 加载地图模块
module load map

# 加载控制台模块
module load console

# 加载图形模块
module load graph

# 查看已加载模块
module list
```

### 3.3 图形化工具

```bash
# 启动图形化界面
sim_vehicle.py -v ArduCopter --console --map --osd

# 启动虚拟摇杆
module load joystick
```

---

## 4. Gazebo 仿真

### 4.1 启动 Gazebo

```bash
# 使用 Gazebo Classic
sim_vehicle.py -v ArduCopter --console --map --gazebo

# 使用 Gazebo (Ignition)
sim_vehicle.py -v ArduCopter --console --map --gazebo-iris
```

### 4.2 自定义世界

```bash
# 使用空旷世界
sim_vehicle.py -v ArduCopter --console --map --gazebo-world empty

# 使用自定义世界
sim_vehicle.py -v ArduCopter --console --map \
    --gazebo-world ~/my_world.sdf
```

---

## 5. 多机仿真

### 5.1 启动多机

```bash
# 终端1: 实例0
sim_vehicle.py -v ArduCopter --console --map --instance 0

# 终端2: 实例1
sim_vehicle.py -v ArduCopter --console --map --instance 1

# 终端3: 实例2
sim_vehicle.py -v ArduCopter --console --map --instance 2
```

### 5.2 端口分配

| 实例 | TCP 端口 | UDP 端口 |
|------|----------|----------|
| 0 | 5760 | 14550 |
| 1 | 5770 | 14560 |
| 2 | 5780 | 14570 |

---

## 6. 日志分析

### 6.1 飞行日志

日志自动保存在:
```
~/ardupilot/logs/
```

### 6.2 使用 Mission Planner 分析

1. 打开 Mission Planner
2. Flight Data → DataFlash Logs → Review a Log
3. 选择 `.bin` 文件
4. 查看图表

### 6.3 关键日志字段

| 字段 | 说明 | 正常范围 |
|------|------|----------|
| ATT.Roll | 滚转角 | ±5° (悬停) |
| ATT.Pitch | 俯仰角 | ±5° (悬停) |
| CTUN.NavRoll | 期望滚转 | 跟踪 ATT.Roll |
| POS.Lat | 纬度 | 航点位置 |
| POS.Lng | 经度 | 航点位置 |
| BAT.Volt | 电压 | > 14V (4S) |
| BAT.Curr | 电流 | < 50A |

### 6.4 使用 mavlogdump

```bash
# 安装
pip3 install pymavlink

# 转换为 CSV
mavlogdump.py --format CSV flight.bin > flight.csv

# 查看消息
mavlogdump.py --types ATT,POS,BAT flight.bin
```

---

## 7. 性能调优

### 7.1 仿真速度

```bash
# 加速仿真
sim_vehicle.py -v ArduCopter --console --map --speedup 4

# 减速仿真 (调试用)
sim_vehicle.py -v ArduCopter --console --map --speedup 0.5
```

### 7.2 减少延迟

```bash
# 禁用不需要的模块
param set SERIAL5_PROTOCOL -1  # 禁用串口5

# 减少日志频率
param set LOG_BITMASK 830
```

### 7.3 Headless 模式

```bash
# 无 GUI (CI/测试)
sim_vehicle.py -v ArduCopter --console --no-map
```

---

## 8. 故障注入

### 8.1 传感器故障

```bash
# 模拟 GPS 丢失
param set GPS_TYPE 0

# 模拟气压计故障
param set SIM_BARO_FAIL 1

# 模拟磁力计故障
param set SIM_MAG_FAIL 1
```

### 8.2 电机故障

```bash
# 模拟电机1失效
param set SIM_ENGINE_FAIL 1

# 恢复
param set SIM_ENGINE_FAIL 0
```

### 8.3 通信故障

```bash
# 模拟遥控器丢失
param set SIM_RC_FAIL 1
```

---

## 9. 实验练习

### 练习 1: 基本飞行

```bash
# 1. 启动仿真
sim_vehicle.py -v ArduCopter --console --map

# 2. 在 MAVProxy 中:
arm throttle
takeoff 10
# 等待起飞完成

mode loiter
# 用 Mission Planner 拖动位置

mode rtl
```

### 练习 2: 航点任务

1. 启动仿真
2. 打开 Mission Planner
3. Flight Plan → 添加航点
4. Write WPs → Auto

### 练习 3: 日志分析

```bash
# 1. 执行一次飞行
arm throttle
takeoff 10
mode rtl

# 2. 找到日志文件
ls ~/ardupilot/logs/

# 3. 用 Mission Planner 分析
# 观察: 高度曲线、姿态曲线、电机输出
```

---

## 下一步

→ [03 — 参数调优](03-parameter-tuning.md)
