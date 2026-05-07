# 01 — ArduPilot 架构解析

> 目标: 理解ArduPilot的分层架构、库设计、模块通信机制

---

## 1. 整体架构

ArduPilot 分为三个主要层次:

```
┌─────────────────────────────────────────────────┐
│                Vehicle Code                      │
│  ArduCopter / ArduPlane / Rover / ArduSub       │
├─────────────────────────────────────────────────┤
│                Libraries                         │
│  AP_AHRS / AP_Motors / AC_PID / AP_Navigation   │
├─────────────────────────────────────────────────┤
│                AP_HAL                           │
│  硬件抽象层 (Pixhawk/Linux/SITL)               │
└─────────────────────────────────────────────────┘
```

---

## 2. AP_HAL 硬件抽象层

### 2.1 什么是AP_HAL

AP_HAL (Hardware Abstraction Layer) 屏蔽硬件差异:

| 后端 | 说明 | 目录 |
|------|------|------|
| `AP_HAL_PX4` | Pixhawk 系列 | `libraries/AP_HAL_PX4/` |
| `AP_HAL_Linux` | Linux 板 | `libraries/AP_HAL_Linux/` |
| `AP_HAL_SITL` | SITL 仿真 | `libraries/AP_HAL_SITL/` |
| `AP_HAL_ChibiOS` | ChibiOS RTOS | `libraries/AP_HAL_ChibiOS/` |
| `AP_HAL_Empty` | 空实现 | `libraries/AP_HAL_Empty/` |

### 2.2 AP_HAL 接口

```cpp
// 统一接口示例
class HAL {
    UARTDriver* uartA;   // 串口1
    UARTDriver* uartB;   // 串口2
    AnalogIn*   analogin; // 模拟输入
    Storage*    storage;  // EEPROM
    GPIO*       gpio;     // GPIO
    RCInput*    rcin;     // 遥控器输入
    RCOutput*   rcout;    // 电机输出
};
```

---

## 3. Libraries 库

### 3.1 核心库

| 库 | 作用 | 关键文件 |
|------|------|----------|
| `AP_AHRS` | 姿态参考系统 | `AP_AHRS_DCM.cpp`, `AP_AHRS_NavEKF.cpp` |
| `AP_InertialSensor` | IMU 驱动 | `AP_InertialSensor.cpp` |
| `AP_Baro` | 气压计 | `AP_Baro.cpp` |
| `AP_GPS` | GPS | `AP_GPS.cpp` |
| `AP_Compass` | 磁力计 | `AP_Compass.cpp` |
| `AP_RangeFinder` | 测距仪 | `AP_RangeFinder.cpp` |

### 3.2 控制库

| 库 | 作用 | 关键文件 |
|------|------|----------|
| `AC_PID` | PID 控制器 | `AC_PID.cpp` |
| `AC_AttitudeControl` | 姿态控制 | `AC_AttitudeControl.cpp` |
| `AC_PosControl` | 位置控制 | `AC_PosControl.cpp` |
| `AP_Motors` | 电机混控 | `AP_MotorsMatrix.cpp` |
| `AP_L1_Control` | L1 导航 (固定翼) | `AP_L1_Control.cpp` |

### 3.3 导航库

| 库 | 作用 | 关键文件 |
|------|------|----------|
| `AP_Navigation` | 导航接口 | `AP_Navigation.h` |
| `AP_WPNav` | 航点导航 | `AP_WPNav.cpp` |
| `AP_Circle` | 圆形盘旋 | `AP_Circle.cpp` |
| `AP_Rally` | 集结点 | `AP_Rally.cpp` |
| `AP_Mission` | 任务管理 | `AP_Mission.cpp` |

---

## 4. Vehicle Code 载具代码

### 4.1 ArduCopter (四旋翼)

位置: `ArduCopter/`

```
ArduCopter/
├── ArduCopter.cpp          # 主文件, 任务调度表
├── Attitude.cpp            # 姿态控制
├── position_control.cpp    # 位置控制
├── mode_*.cpp              # 飞行模式
├── sensors.cpp             # 传感器读取
├── GCS_Mavlink.cpp         # MAVLink通信
└── Parameters.cpp          # 参数定义
```

### 4.2 飞行模式

| 模式 | 文件 | 说明 |
|------|------|------|
| Stabilize | `mode_stabilize.cpp` | 手动, 姿态稳定 |
| AltHold | `mode_althold.cpp` | 高度保持 |
| Loiter | `mode_loiter.cpp` | 位置保持 |
| Auto | `mode_auto.cpp` | 自动航线 |
| RTL | `mode_rtl.cpp` | 返航 |
| Guided | `mode_guided.cpp` | 外部引导 |
| Sport | `mode_sport.cpp` | 运动模式 |

### 4.3 ArduPlane (固定翼)

位置: `ArduPlane/`

```
ArduPlane/
├── ArduPlane.cpp           # 主文件
├── Attitude.cpp            # 姿态控制
├── navigation.cpp          # 导航逻辑
├── mode_*.cpp              # 飞行模式
└── quadplane.cpp           # 四旋翼模式 (VTOL)
```

---

## 5. 通信机制

### 5.1 直接函数调用

ArduPilot 使用直接函数调用, 不是消息总线:

```cpp
// 在 ArduCopter 中调用库
ahrs.get_euler_angles(&roll, &pitch, &yaw);
motors.set_roll(roll_output);
motors.set_pitch(pitch_output);
motors.output();
```

### 5.2 参数系统

参数通过 `Parameters.h` 定义:

```cpp
// Parameters.h
#define GSCALAR(v, name, def) type v{def}

GSCALAR(pilot_speed_up, "PILOT_SPEED_UP", 250),
GSCALAR(pilot_speed_dn, "PILOT_SPEED_DN", 150),

// 使用
g.pilot_speed_up  // 读取参数
```

### 5.3 MAVLink 通信

```cpp
// GCS_Mavlink.cpp
void Copter::send_heartbeat(mavlink_channel_t chan)
{
    mavlink_msg_heartbeat_send(
        chan,
        MAV_TYPE_QUADROTOR,
        MAV_AUTOPILOT_ARDUPILOTMEGA,
        base_mode,
        custom_mode,
        MAV_STATE_STANDBY
    );
}
```

---

## 6. 数据流

```
传感器 (IMU/GPS/Baro/Mag)
    ↓ AP_InertialSensor, AP_GPS, AP_Baro, AP_Compass
AHRS (姿态估计)
    ↓ roll, pitch, yaw, position
Flight Mode (飞行模式)
    ↓ 目标姿态/位置
Attitude Controller (姿态控制)
    ↓ 目标力矩
Motors (电机混控)
    ↓ PWM 输出
电调 → 电机
```

---

## 7. 构建系统

### 7.1 waf 构建

ArduPilot 使用 waf 构建系统:

```bash
# 配置
./waf configure --board sitl

# 编译四旋翼
./waf copter

# 编译固定翼
./waf plane

# 编译车辆
./waf rover

# 清除
./waf clean
```

### 7.2 板级支持

| 板子 | 命令 | 说明 |
|------|------|------|
| Pixhawk 1 | `--board px4-v2` | 旧款 |
| Pixhawk 4 | `--board px4-v4` | 常用 |
| Pixhawk 6C | `--board px4-v6c` | 新款 |
| CubeOrange | `--board CubeOrange` | 高端 |
| SITL | `--board sitl` | 仿真 |

---

## 8. 坐标系

### 8.1 ArduPilot 坐标系

- **NED** (北东地): 用于位置和速度
- **FRD** (前右下): 用于机体系
- **Euler angles**: ZYX 顺序 (yaw→pitch→roll)

### 8.2 与PX4的区别

| 方面 | ArduPilot | PX4 |
|------|-----------|-----|
| 位置坐标 | NED | NED |
| 四元数 | [w,x,y,z] | [w,x,y,z] |
| 角度单位 | 度 (参数) / 弧度 (内部) | 弧度 |
| 电机输出 | PWM (1000-2000) | 归一化 (0-1) |

---

## 9. 关键概念

### 9.1 时间系统

- 主循环: 400Hz (2.5ms)
- 传感器: 1kHz (IMU)
- 参数: 使用 `AP_HAL::millis()` 和 `AP_HAL::micros()`

### 9.2 参数系统

- 存储在 EEPROM/Flash
- 通过 MAVLink 可远程读写
- Mission Planner 可图形化修改
- 参数名: `GROUP_NAME` (如 `ATC_RAT_RLL_P`)

### 9.3 日志系统

- 自动记录到 SD 卡
- `.bin` 格式 (二进制)
- Mission Planner 可分析
- 关键日志: ATT, POS, CTUN, NTUN

---

## 下一步

→ [02 — SITL 仿真](02-sitl-simulation.md)
