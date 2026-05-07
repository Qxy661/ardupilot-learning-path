# 07 — 实机部署指南

> 目标: 掌握ArduPilot固件烧录、传感器校准、实机首飞流程

---

## 1. 硬件准备

### 1.1 推荐硬件

| 组件 | 推荐型号 | 说明 |
|------|----------|------|
| 飞控 | Pixhawk 6C / CubeOrange | 高可靠性 |
| GPS | M10 GPS | 高精度 |
| 遥控器 | RadioMaster TX16S | OpenTX |
| 电调 | BLHeli_32 | 支持 DShot |
| 电池 | 4S LiPo 1500-2200mAh | 四旋翼 |
| 机架 | F450 / QAV250 | 标准机架 |

### 1.2 接线图

```
Pixhawk 6C:
┌─────────────────────────────────────┐
│  TELEM1   TELEM2   GPS    CAN1     │
│  (MAVLink) (备用)  (GPS)  (CAN总线) │
│                                     │
│  RC IN    PWM OUT 1-8   BATTERY    │
│  (遥控器)  (电调)        (电池)      │
│                                     │
│  USB      SD卡槽   BUZZER  SAFETY  │
│  (调试)   (日志)   (蜂鸣器) (安全开关)│
└─────────────────────────────────────┘

电调接线:
PWM OUT 1 → 电机1 (右前, CW)
PWM OUT 2 → 电机2 (右后, CCW)
PWM OUT 3 → 电机3 (左后, CW)
PWM OUT 4 → 电机4 (左前, CCW)
```

---

## 2. 固件烧录

### 2.1 使用 Mission Planner

1. 打开 Mission Planner
2. 连接飞控 (USB)
3. Initial Setup → Install Firmware
4. 选择 ArduCopter
5. 等待烧录完成

### 2.2 命令行烧录

```bash
# 克隆 ArduPilot
git clone https://github.com/ArduPilot/ardupilot.git --recursive
cd ardupilot

# 配置
./waf configure --board px4-v6c

# 编译
./waf copter

# 烧录 (USB连接飞控)
./waf copter --upload
```

---

## 3. 传感器校准

### 3.1 校准顺序

```
1. 加速度计校准 (必须)
2. 陀螺仪校准 (自动)
3. 磁力计校准 (必须)
4. 遥控器校准 (必须)
5. 电调校准 (必须)
6. 电池校准 (建议)
```

### 3.2 Mission Planner 校准

1. Initial Setup → Mandatory Hardware
2. 按顺序点击各传感器
3. 按照提示旋转飞机
4. 等待校准完成 (绿色勾)

### 3.3 加速度计校准

```bash
# 在 Mission Planner 中:
# 1. 放平飞机 → 点击 "Place vehicle flat"
# 2. 翻转 180° → 点击 "Place vehicle on its left side"
# 3. 左侧朝下 → 点击 "Place vehicle nose down"
# 4. 机头朝下 → 点击 "Place vehicle on its right side"
# 5. 右侧朝下 → 点击 "Place vehicle nose up"
# 6. 机头朝上 → 点击 "Place vehicle on its back"
```

### 3.4 磁力计校准

```bash
# 在 Mission Planner 中:
# 1. 开始旋转飞机 (所有方向)
# 2. 保持旋转直到进度条满
# 3. 点击完成
```

---

## 4. 电调校准

### 4.1 校准步骤

```bash
# 1. 取下螺旋桨!
# 2. 在 Mission Planner 中:
#    Initial Setup → Optional Hardware → ESC Calibration
# 3. 按照提示操作
# 4. 等待完成
```

---

## 5. 飞行模式配置

### 5.1 推荐模式

| 通道 | 模式 | 说明 |
|------|------|------|
| 低 | Stabilize | 手动, 姿态稳定 |
| 中 | AltHold | 高度保持 |
| 高 | Loiter | 位置保持 (推荐) |

### 5.2 失控保护

```bash
# 在 Mission Planner 中:
# Config → FailSafe

# 设置:
# - 遥控器丢失: RTL 或 Land
# - 地面站丢失: RTL
# - 电池低压: RTL
```

---

## 6. 首飞前检查

### 6.1 检查清单

```
[ ] 固件已烧录
[ ] 传感器已校准 (全部绿色)
[ ] 遥控器已校准
[ ] 电调已校准
[ ] 电池电压正常 (4S: 14.8-16.8V)
[ ] 螺旋桨安装正确 (CW/CCW)
[ ] 电机转向正确
[ ] GPS 信号良好 (> 10颗卫星)
[ ] 飞行模式已配置
[ ] 失控保护已设置
[ ] 地理围栏已设置
```

---

## 7. 首飞流程

### 7.1 起飞前

```bash
# 1. 将飞机放在空旷场地
# 2. 插入电池
# 3. 等待 GPS 锁定 (LED 绿色闪烁)
# 4. 遥控器切换到 Stabilize 模式
# 5. 解锁 (油门最低 + 偏航右)
# 6. 缓慢推油门
```

### 7.2 起飞

```bash
# 使用 Mission Planner:
# 1. 点击 "Arm/Disarm"
# 2. 切换到 Loiter 模式
# 3. 推油门起飞

# 使用 MAVProxy:
arm throttle
takeoff 10
```

### 7.3 首飞测试

```bash
# 测试顺序:
# 1. 悬停测试 (30秒)
#    - 观察: 无振荡, 位置稳定
#    - 检查: 电流正常, 温度正常

# 2. 前后左右 (小幅度)
#    - 观察: 响应正常, 无异常

# 3. 旋转测试
#    - 观察: 偏航响应正常

# 4. 降落
#    - 缓慢降低油门
#    - 触地后上锁
```

---

## 8. 日志分析

### 8.1 下载日志

```bash
# 在 Mission Planner 中:
# Flight Data → DataFlash Logs → Download Logs

# 或从 SD 卡复制:
# /APM/logs/
```

### 8.2 关键指标

| 指标 | 正常范围 | 说明 |
|------|----------|------|
| Roll/Pitch | ±5° | 悬停姿态 |
| 振动 | < 3 m/s² | IMU 振动 |
| GPS HDOP | < 2.0 | GPS 精度 |
| 电流 | < 50A | 峰值电流 |
| 电压 | > 14V (4S) | 电池电压 |

---

## 9. 常见问题

### Q: GPS 信号差

```bash
# 原因: 室内或遮挡
# 解决: 移到室外, 等待锁定

# 检查:
# Mission Planner → GPS Status
# 应该 > 10颗卫星, HDOP < 2.0
```

### Q: 起飞后翻车

```bash
# 原因:
# 1. 螺旋桨装反
# 2. 电机转向错误
# 3. 电调未校准

# 检查:
# 1. 确认 CW/CCW
# 2. 确认电机转向
# 3. 重新校准电调
```

### Q: 飞行中振荡

```bash
# 原因: PID 参数不合适
# 解决:
# 1. 降低角速率环 P 增益
# 2. 增加 D 增益
# 3. 或使用 Autotune
```

---

## 10. 安全提醒

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

## 下一步

→ [08 — 常见问题](08-common-pitfalls.md)
