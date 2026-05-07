# ArduPilot 学习进度清单

> 每完成一项打勾, 追踪你的学习进度

---

## Week 1: 环境搭建 + 首次飞行

### 环境搭建
- [ ] WSL2 Ubuntu 22.04 安装成功
- [ ] ArduPilot 代码克隆成功 (`--recursive`)
- [ ] 工具链安装完成 (`install-prereqs-ubuntu.sh`)
- [ ] 首次编译成功 (`./waf copter`)
- [ ] SITL 启动成功 (`sim_vehicle.py`)
- [ ] Mission Planner 连接成功

### 首次飞行
- [ ] 在 MAVProxy 中解锁 (`arm throttle`)
- [ ] 起飞 (`takeoff 10`)
- [ ] 观察地图上无人机悬停
- [ ] 降落 (`mode land`)
- [ ] 切换飞行模式 (`mode loiter`)

---

## Week 2: 架构理解 + MAVLink

### 架构理解
- [ ] 理解 AP_HAL 硬件抽象层
- [ ] 理解 Libraries 库结构
- [ ] 理解 Vehicle Code 载具代码
- [ ] 能画出完整数据流图

### MAVLink 通信
- [ ] MAVProxy 基本命令
- [ ] 参数查看和修改
- [ ] 航点加载和保存
- [ ] 模块加载 (map/console)
- [ ] 理解 MAVLink 消息格式

---

## Week 3: SITL 深入 + Mission Planner

### SITL 使用
- [ ] 使用不同载具 (Copter/Plane/Rover)
- [ ] 启动多机仿真 (`--instance`)
- [ ] 使用加速模式 (`--speedup`)
- [ ] 故障注入 (GPS/电机/遥控器)
- [ ] 日志分析 (mavlogdump)

### Mission Planner
- [ ] 航点任务规划
- [ ] 参数修改
- [ ] 传感器校准界面
- [ ] 飞行日志下载和分析

---

## Week 4: PID 调参

### 理论
- [ ] 理解 P/I/D 各项作用
- [ ] 理解级联 PID 结构
- [ ] 理解从内环到外环调参顺序

### 实操
- [ ] 角速率环调参 (Roll/Pitch/Yaw)
- [ ] 姿态环调参
- [ ] 位置环调参
- [ ] 推力模型调整 (`MOT_THST_EXPO`)
- [ ] 使用 Autotune
- [ ] 参数文件导入/导出

---

## Week 5: 源码阅读

### 代码结构
- [ ] 理解 `libraries/` 目录结构
- [ ] 理解 `ArduCopter/` 载具代码
- [ ] 理解 `wscript` 构建系统

### 核心模块
- [ ] 阅读 AP_AHRS 姿态估计
- [ ] 阅读 AC_AttitudeControl 姿态控制
- [ ] 阅读 AC_PosControl 位置控制
- [ ] 阅读 AP_Motors 电机混控
- [ ] 能追踪完整控制链路

---

## Week 6: Lua 脚本开发

### 基础
- [ ] 启用 Lua 脚本 (`SCR_ENABLE`)
- [ ] Hello World 脚本运行
- [ ] 传感器数据读取
- [ ] 地面站消息发送

### 进阶
- [ ] 圆形轨迹脚本
- [ ] 自定义参数定义
- [ ] 串口数据读取
- [ ] 事件处理 (模式切换)

---

## Week 7: ROS2 集成

### 环境搭建
- [ ] ROS2 Humble 安装成功
- [ ] MAVROS 安装成功
- [ ] ROS2 能看到 MAVROS 话题

### Offboard 控制
- [ ] 基本 Offboard 节点运行
- [ ] 解锁 + 起飞
- [ ] 位置控制 (悬停)
- [ ] 圆形轨迹飞行
- [ ] 坐标系转换 (NED↔ENU)

### DroneKit
- [ ] DroneKit 安装成功
- [ ] 基本连接测试
- [ ] 航点任务执行

---

## Week 8: 实机部署

### 硬件准备
- [ ] Pixhawk 接线完成
- [ ] 电调连接正确
- [ ] GPS 安装正确
- [ ] 遥控器对频成功

### 固件和校准
- [ ] ArduPilot 固件烧录成功
- [ ] 传感器校准 (加速度计/磁力计)
- [ ] 遥控器校准
- [ ] 电调校准
- [ ] 飞行模式配置
- [ ] 失控保护设置

### 首飞
- [ ] 起飞前检查清单完成
- [ ] 首次悬停成功
- [ ] 小幅度操控测试
- [ ] 降落并上锁
- [ ] 日志分析无异常

---

## 进阶技能

- [ ] 自定义混控器
- [ ] 故障检测和处理
- [ ] 避障集成
- [ ] 多机协调
- [ ] 提交 Issue/PR 到 ArduPilot 社区
