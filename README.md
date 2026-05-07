# ArduPilot 飞控学习路径 — 从零到能改代码

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ArduPilot](https://img.shields.io/badge/ArduPilot-v4.4+-blue.svg)](https://github.com/ArduPilot/ardupilot)
[![ROS2](https://img.shields.io/badge/ROS2-Humble-green.svg)](https://docs.ros.org/en/humble/)

> 面向飞控方向学生/工程师的系统化学习指南
> 基于 ArduPilot 官方文档, 结合实操经验, 覆盖从环境搭建到实机部署全流程

---

## ArduPilot 架构总览

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户层                                   │
│   Mission Planner · DroneKit · MAVROS · Lua 脚本               │
├─────────────────────────────────────────────────────────────────┤
│                      Vehicle Code                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ ArduCopter / ArduPlane / Rover / ArduSub                  │ │
│  │  飞行模式 · 传感器 · MAVLink · 参数                        │ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│                       Libraries                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ AP_AHRS  │ │AC_Attit- │ │AC_Pos-   │ │ AP_Motors│          │
│  │ 姿态估计 │ │udeControl│ │Control   │ │ 电机混控 │          │
│  │          │ │ 姿态控制 │ │ 位置控制 │ │          │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │AP_Inert- │ │ AP_GPS   │ │ AP_Baro  │ │ AC_PID   │          │
│  │ialSensor │ │ GPS      │ │ 气压计   │ │ PID控制  │          │
│  │ IMU      │ │          │ │          │ │          │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
├─────────────────────────────────────────────────────────────────┤
│                        AP_HAL                                    │
│        硬件抽象层 (Pixhawk / Linux / SITL / ChibiOS)            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 你将学到什么

| 技能 | 内容 |
|------|------|
| 架构原理 | AP_HAL、库设计、载具代码、waf构建 |
| SITL仿真 | sim_vehicle.py、多机仿真、故障注入 |
| PID调参 | 内环→外环、Autotune、推力模型 |
| 控制链路 | 传感器→AHRS→控制器→混控→电机 |
| Lua脚本 | 传感器读取、任务脚本、自定义参数 |
| ROS2集成 | MAVROS、Offboard控制、坐标转换 |
| 实机部署 | Pixhawk烧录→校准→首飞→日志分析 |

---

## 学习路线 (建议8周)

```
Week 1 ─→ 环境搭建 + 首次SITL飞行 ──────────── docs/00-environment-setup.md
Week 2 ─→ 架构理解 + MAVLink通信 ────────────── docs/01-architecture.md
Week 3 ─→ SITL深入 + Mission Planner ────────── docs/02-sitl-simulation.md
Week 4 ─→ PID调参方法论 ────────────────────── docs/03-parameter-tuning.md
Week 5 ─→ 源码阅读 + 控制链路 ──────────────── docs/04-code-reading.md
Week 6 ─→ Lua脚本开发 ─────────────────────── docs/05-lua-scripting.md
Week 7 ─→ ROS2集成 + Offboard控制 ─────────── docs/06-ros2-integration.md
Week 8 ─→ 实机部署 + 首飞 ─────────────────── docs/07-hardware-deploy.md
```

---

## 快速开始

```bash
# 1. 克隆本项目
git clone https://github.com/Qxy661/ardupilot-learning-path.git

# 2. 搭建ArduPilot环境
cd ~
git clone https://github.com/ArduPilot/ardupilot.git --recursive
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
source ~/.bashrc

# 3. 首次SITL飞行
cd ~/ardupilot/Tools/autotest
sim_vehicle.py -v ArduCopter --console --map
# 在 MAVProxy 中:
arm throttle
takeoff 10

# 4. 开始学习
# 按 docs/ 顺序阅读, 使用 docs/learning-checklist.md 追踪进度
```

---

## 项目结构

```
ardupilot-learning-path/
├── README.md                          ← 你在这里
├── LICENSE
├── docs/                              # 学习文档
│   ├── 00-environment-setup.md        # 环境搭建
│   ├── 01-architecture.md             # ArduPilot架构解析
│   ├── 02-sitl-simulation.md          # SITL仿真
│   ├── 03-parameter-tuning.md         # 参数调优
│   ├── 04-code-reading.md             # 源码阅读指南
│   ├── 05-lua-scripting.md            # Lua脚本开发
│   ├── 06-ros2-integration.md         # ROS2集成
│   ├── 07-hardware-deploy.md          # 实机部署
│   ├── 08-common-pitfalls.md          # 常见坑
│   └── learning-checklist.md          # 学习进度清单
├── examples/                          # 示例代码
│   ├── mavlink_example.py             # MAVLink通信
│   ├── dronekit_example.py            # DroneKit控制
│   ├── ros2_offboard.py               # ROS2 Offboard
│   └── lua_scripts/                   # Lua脚本
│       ├── hello_world.lua
│       ├── circle_mission.lua
│       └── sensor_logger.lua
├── scripts/                           # 工具脚本
│   ├── setup_ardupilot.sh             # 一键环境搭建
│   ├── sitl_launch.sh                 # SITL启动脚本
│   └── param_template.parm            # 调参模板
└── reference/                         # 参考资料
    ├── quick-reference.md             # 快速参考卡
    ├── ap-parameter-list.md           # 常用参数列表
    ├── tuning-checklist.md            # 调参检查清单
    └── lua-api-reference.md           # Lua API参考
```

---

## 前置要求

| 要求 | 说明 |
|------|------|
| 系统 | Ubuntu 22.04 (推荐WSL2) |
| C++ | 基础知识 (能读懂类和函数) |
| Python | 基础知识 (DroneKit/ROS2需要) |
| 控制 | 了解PID基本概念 |
| 数学 | 了解坐标系和旋转矩阵 |

---

## 与 PX4 对比

| 方面 | ArduPilot | PX4 |
|------|-----------|-----|
| 消息系统 | 直接函数调用 | uORB (发布/订阅) |
| 构建系统 | waf | CMake |
| 脚本 | Lua | C++ 模块 |
| 地面站 | Mission Planner | QGroundControl |
| SITL | `sim_vehicle.py` | `make px4_sitl` |
| ROS2 | MAVROS | uXRCE-DDS |
| 优势 | 生态丰富, 社区大 | 架构清晰, 现代化 |

> 如果你也学 PX4, 看 [px4-learning-path](https://github.com/Qxy661/px4-learning-path)

---

## 参考资源

| 资源 | 链接 |
|------|------|
| ArduPilot 官方文档 | https://ardupilot.org/ardupilot/ |
| ArduPilot GitHub | https://github.com/ArduPilot/ardupilot |
| ArduPilot Wiki | https://ardupilot.org/dev/ |
| ArduPilot 论坛 | https://discuss.ardupilot.org/ |
| Mission Planner | https://ardupilot.org/planner/ |
| DroneKit | https://dronekit-python.readthedocs.io/ |
| Lua Scripts | https://ardupilot.org/rover/docs/common-lua-scripts.html |

---

## License

MIT - 详见 [LICENSE](LICENSE)
