# ArduPilot 飞控学习路径 — 从零到能改代码

> 面向飞控方向学生/工程师的系统化学习指南
> 基于 ArduPilot 官方文档, 结合实操经验, 覆盖从环境搭建到实机部署全流程

---

## 你将学到什么

- ArduPilot 架构原理 (AP_HAL、库、载具代码)
- SITL 仿真环境 (sim_vehicle.py)
- PID 调参方法论 (内环→外环、Autotune)
- 控制链路追踪 (传感器→EKF→控制器→混控→电机)
- 自定义 Lua 脚本 (任务脚本、传感器驱动)
- ROS2 Offboard 控制 (MAVROS/mavros2)
- 实机部署流程 (Pixhawk 烧录→校准→首飞)

---

## 学习路线 (建议8周)

```
Week 1: 环境搭建 + 首次SITL飞行
Week 2: 架构理解 + MAVLink通信
Week 3: SITL深入 + Mission Planner
Week 4: PID调参方法论
Week 5: 源码阅读 + 控制链路
Week 6: Lua脚本开发
Week 7: ROS2集成 + Offboard控制
Week 8: 实机部署 + 首飞
```

---

## 项目结构

```
ardupilot-learning-path/
├── README.md                          # 本文件
├── .gitignore
├── docs/                              # 学习文档
│   ├── 00-environment-setup.md        # 环境搭建
│   ├── 01-architecture.md             # ArduPilot架构解析
│   ├── 02-sitl-simulation.md          # SITL仿真
│   ├── 03-parameter-tuning.md         # 参数调优
│   ├── 04-code-reading.md             # 源码阅读指南
│   ├── 05-lua-scripting.md            # Lua脚本开发
│   ├── 06-ros2-integration.md         # ROS2集成
│   ├── 07-hardware-deploy.md          # 实机部署
│   └── 08-common-pitfalls.md          # 常见坑
├── examples/                          # 示例代码
│   ├── mavlink_example.py             # MAVLink通信示例
│   ├── dronekit_example.py            # DroneKit控制示例
│   ├── lua_scripts/                   # Lua脚本示例
│   │   ├── hello_world.lua
│   │   ├── circle_mission.lua
│   │   └── sensor_logger.lua
│   └── ros2_offboard.py               # ROS2 Offboard控制
├── scripts/                           # 工具脚本
│   ├── setup_ardupilot.sh             # 一键环境搭建
│   ├── sitl_launch.sh                 # SITL启动脚本
│   └── param_template.parm            # 调参模板
└── reference/                         # 参考资料
    ├── ap-parameter-list.md           # 常用参数列表
    ├── tuning-checklist.md            # 调参检查清单
    └── lua-api-reference.md           # Lua API参考
```

---

## 快速开始

```bash
# 1. 克隆本项目
git clone https://github.com/YOUR_USERNAME/ardupilot-learning-path.git

# 2. 搭建ArduPilot环境 (参考 docs/00-environment-setup.md)
cd ~
git clone https://github.com/ArduPilot/ardupilot.git --recursive
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y

# 3. 首次SITL飞行
sim_vehicle.py -v ArduCopter --console --map

# 4. 在 MAVProxy 中:
arm throttle
takeoff 10

# 5. 开始学习
# 按 docs/ 顺序阅读
```

---

## ArduPilot vs PX4

| 方面 | ArduPilot | PX4 |
|------|-----------|-----|
| 构建系统 | waf | CMake |
| 硬件抽象 | AP_HAL | Platform Layer |
| 消息系统 | 直接调用 | uORB |
| 脚本 | Lua | C++ 模块 |
| 地面站 | Mission Planner | QGroundControl |
| SITL | sim_vehicle.py | make px4_sitl |
| 调参工具 | Mission Planner | QGroundControl |
| 社区 | discuss.ardupilot.org | discuss.px4.io |

---

## 前置要求

- Ubuntu 22.04 (推荐WSL2)
- 基础C++知识
- 基础Python知识
- 了解PID控制基本概念
- 了解坐标系和旋转矩阵

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

MIT
