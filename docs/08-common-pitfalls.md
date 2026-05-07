# 08 — 常见问题与避坑指南

> 目标: 总结ArduPilot学习和开发中的常见问题

---

## 1. 编译问题

### 1.1 子模块缺失

```bash
# 错误: fatal: not a tree object

# 解决:
cd ~/ardupilot
git submodule update --init --recursive
```

### 1.2 编译内存不足

```bash
# 错误: c++: internal compiler error: Killed

# 解决: 减少并行编译数
./waf copter -j2
```

### 1.3 waf 找不到

```bash
# 错误: ./waf: command not found

# 解决:
cd ~/ardupilot
./waf --version
# 如果不行, 重新安装
git submodule update --init --recursive
```

---

## 2. SITL 问题

### 2.1 无法连接 Mission Planner

```bash
# 原因: 端口配置错误

# 解决:
# SITL 默认 TCP 5760
# Mission Planner 选择 TCP, 端口 5760
```

### 2.2 仿真速度慢

```bash
# 原因: CPU 性能不足

# 解决:
# 1. 使用加速模式
sim_vehicle.py -v ArduCopter --console --map --speedup 2

# 2. 无 GUI
sim_vehicle.py -v ArduCopter --console --no-map
```

### 2.3 飞机翻车

```bash
# 原因: 默认参数不适合

# 解决:
# 1. 检查 EKF 是否收敛
# 2. 手动调参
param set ATC_RAT_RLL_P 0.1
param set ATC_RAT_PIT_P 0.1
```

---

## 3. ROS2 集成问题

### 3.1 MAVROS 连接失败

```bash
# 错误: [ERROR] [mavros_node]: FCU connection failed

# 解决:
# 1. 检查 ArduPilot 端口
# SITL 默认 TCP 5760

# 2. 检查 MAVROS 配置
ros2 launch mavros apm.launch fcu_url:=tcp://127.0.0.1:5760

# 3. 检查防火墙
sudo ufw allow 5760/tcp
```

### 3.2 ROS2 话题为空

```bash
# 原因: MAVROS 未连接

# 解决:
# 检查 MAVROS 状态
ros2 topic echo /mavros/state

# 检查 ArduPilot 输出
# 在 MAVProxy 中查看
```

---

## 4. PID 调参问题

### 4.1 高频振荡

```bash
# 现象: 电机声音尖锐, 飞机抖动

# 原因: 角速率环 P 或 D 太大

# 解决:
param set ATC_RAT_RLL_P 0.1
param set ATC_RAT_RLL_D 0.002
```

### 4.2 低频摆动

```bash
# 现象: 飞机缓慢摆动

# 原因: 姿态环 P 太大

# 解决:
param set ATC_ANG_RLL_P 4.0
```

### 4.3 位置跟踪有稳态误差

```bash
# 现象: 飞机位置有偏差

# 原因: 速度环 I 不够

# 解决:
param set PSC_VELXY_I 1.0
```

---

## 5. 硬件问题

### 5.1 GPS 信号差

```bash
# 现象: GPS 长时间不锁定

# 原因:
# 1. 室内
# 2. 遮挡
# 3. GPS 模块故障

# 解决:
# 1. 移到室外
# 2. 等待 1-2 分钟
# 3. 检查 GPS 模块
```

### 5.2 遥控器无响应

```bash
# 原因:
# 1. 遥控器未对频
# 2. 通道映射错误

# 解决:
# 1. 重新对频
# 2. 重新校准遥控器
```

---

## 6. 飞行问题

### 6.1 起飞后翻车

```bash
# 原因:
# 1. 螺旋桨装反
# 2. 电机转向错误
# 3. 电调未校准

# 解决:
# 1. 确认 CW/CCW
# 2. 确认电机转向
# 3. 重新校准电调
```

### 6.2 飞行中漂移

```bash
# 现象: 飞机缓慢漂移

# 原因:
# 1. 传感器未校准
# 2. GPS 信号差
# 3. PID 参数不合适

# 解决:
# 1. 重新校准传感器
# 2. 等待 GPS 锁定
# 3. 调整 PID 参数
```

---

## 7. 日志分析

### 7.1 日志文件为空

```bash
# 原因: 日志未启动

# 解决:
# 检查参数
param show LOG_BITMASK
# 应该非零
```

### 7.2 关键日志字段

| 字段 | 说明 | 正常范围 |
|------|------|----------|
| ATT.Roll | 滚转角 | ±5° (悬停) |
| ATT.Pitch | 俯仰角 | ±5° (悬停) |
| CTUN.NavRoll | 期望滚转 | 跟踪 ATT.Roll |
| POS.Lat | 纬度 | 航点位置 |
| BAT.Volt | 电压 | > 14V (4S) |

---

## 8. 安全提醒

```
1. 首飞务必在空旷场地
2. 保持安全距离 (> 5m)
3. 随时准备切换手动模式
4. 电池低电量立即降落
5. 检查螺旋桨是否损坏
6. 不要在人群附近飞行
7. 遵守当地法规
```

---

## 9. 学习资源

| 资源 | 链接 | 说明 |
|------|------|------|
| ArduPilot 官方文档 | https://ardupilot.org/ardupilot/ | 最权威 |
| ArduPilot 论坛 | https://discuss.ardupilot.org/ | 社区支持 |
| ArduPilot GitHub | https://github.com/ArduPilot/ardupilot | 源码 |
| Mission Planner | https://ardupilot.org/planner/ | 地面站 |
| DroneKit | https://dronekit-python.readthedocs.io/ | SDK |
| Lua Scripts | https://ardupilot.org/rover/docs/common-lua-scripts.html | 脚本 |

---

## 10. 总结

```
学习 ArduPilot 的关键:
1. 先理解架构, 再动手
2. 从 SITL 开始, 逐步到实机
3. 系统化调参, 不要盲目
4. 阅读源码, 理解原理
5. 多看日志, 多分析
6. 安全第一, 小心操作
```

---

## 完成!

恭喜你完成 ArduPilot 飞控学习路径!

你现在应该能够:
- 理解 ArduPilot 架构和数据流
- 使用 SITL 进行仿真
- 系统化调参
- 阅读和修改源码
- 使用 Lua 脚本扩展功能
- 集成 ROS2 进行 Offboard 控制
- 部署到实机

继续学习:
- 阅读 ArduPilot 源码, 理解更多细节
- 参与社区, 提问和回答问题
- 开发自己的 Lua 脚本
- 探索更高级的主题 (避障、SLAM、集群)
