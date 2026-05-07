# 04 — 源码阅读指南

> 目标: 理解ArduPilot核心模块的代码结构

---

## 1. 代码目录结构

```
ardupilot/
├── ArduCopter/        # 四旋翼
├── ArduPlane/         # 固定翼
├── Rover/             # 车辆
├── ArduSub/           # 潜艇
├── libraries/         # 公共库
│   ├── AP_HAL/        # 硬件抽象
│   ├── AP_AHRS/       # 姿态估计
│   ├── AP_InertialSensor/  # IMU
│   ├── AP_Baro/       # 气压计
│   ├── AP_GPS/        # GPS
│   ├── AP_Compass/    # 磁力计
│   ├── AC_PID/        # PID控制器
│   ├── AC_AttitudeControl/  # 姿态控制
│   ├── AC_PosControl/ # 位置控制
│   ├── AP_Motors/     # 电机混控
│   └── AP_Navigation/ # 导航
├── Tools/             # 工具
└── wscript            # 构建脚本
```

---

## 2. 追踪数据流

### 2.1 传感器 → AHRS

**关键文件**: `libraries/AP_AHRS/AP_AHRS_DCM.cpp`

```cpp
// DCM 姿态估计
void AP_AHRS_DCM::update(bool skip_ins_update)
{
    // 读取 IMU
    const Vector3f &gyro = get_gyro();
    const Vector3f &accel = get_accel();

    // 更新方向余弦矩阵
    _dcm_matrix.rotate(gyro * _G_Dt);

    // 重力修正
    drift_correction(accel);

    // 提取欧拉角
    roll = atan2f(_dcm_matrix.c.y, _dcm_matrix.c.z);
    pitch = -asinf(_dcm_matrix.c.x);
    yaw = atan2f(_dcm_matrix.b.x, _dcm_matrix.a.x);
}
```

### 2.2 AHRS → 飞行模式

**关键文件**: `ArduCopter/mode_loiter.cpp`

```cpp
// Loiter 模式主循环
void ModeLoiter::run()
{
    // 获取当前位置
    Vector3f pos = inertial_nav.get_position();

    // 位置控制
    float target_roll, target_pitch;
    loiter_nav.get_desired_velocity(target_roll, target_pitch);

    // 姿态控制
    attitude_control->input_euler_angle_roll_pitch_euler_rate_yaw(
        target_roll, target_pitch, target_yaw_rate);
}
```

### 2.3 飞行模式 → 姿态控制

**关键文件**: `libraries/AC_AttitudeControl/AC_AttitudeControl.cpp`

```cpp
// 姿态控制主函数
void AC_AttitudeControl::input_euler_angle_roll_pitch_euler_rate_yaw(
    float euler_roll_angle_cd,
    float euler_pitch_angle_cd,
    float euler_yaw_rate_cds)
{
    // 计算期望姿态
    Quaternion attitude_target;
    attitude_target.from_euler(radians(euler_roll_angle_cd * 0.01f),
                               radians(euler_pitch_angle_cd * 0.01f),
                               _attitude_target_euler_angle.z);

    // 姿态误差
    Quaternion attitude_error;
    attitude_error = attitude_target * attitude_target.inverse();

    // 角速率控制
    Vector3f target_ang_vel = attitude_error.to_axis_angle() * _p_angle_roll.kP();
}
```

### 2.4 姿态控制 → 角速率控制

**关键文件**: `libraries/AC_AttitudeControl/AC_AttitudeControl_Multi.cpp`

```cpp
// 角速率控制
void AC_AttitudeControl_Multi::rate_controller_run()
{
    // PID 计算
    _pid_rate_roll.update_all(_rate_target_ang_vel.x, gyro.x);
    _pid_rate_pitch.update_all(_rate_target_ang_vel.y, gyro.y);
    _pid_rate_yaw.update_all(_rate_target_ang_vel.z, gyro.z);

    // 输出力矩
    _motors.set_roll(_pid_rate_roll.get_pid());
    _motors.set_pitch(_pid_rate_pitch.get_pid());
    _motors.set_yaw(_pid_rate_yaw.get_pid());
}
```

### 2.5 力矩 → 电机输出

**关键文件**: `libraries/AP_Motors/AP_MotorsMatrix.cpp`

```cpp
// 电机混控
void AP_MotorsMatrix::output_armed_stabilizing()
{
    // 计算各电机输出
    for (uint8_t i = 0; i < AP_MOTORS_MAX_NUM_MOTORS; i++) {
        if (motor_enabled[i]) {
            _actuator[i] = _roll_factor[i] * _roll_in +
                           _pitch_factor[i] * _pitch_in +
                           _yaw_factor[i] * _yaw_in +
                           _throttle_in;
        }
    }

    // 限制输出
    limit_throttle_lower();
    limit_throttle_upper();

    // 输出到电调
    for (uint8_t i = 0; i < AP_MOTORS_MAX_NUM_MOTORS; i++) {
        if (motor_enabled[i]) {
            rc_write(i, output_to_pwm(_actuator[i]));
        }
    }
}
```

---

## 3. 主循环

### 3.1 任务调度表

**关键文件**: `ArduCopter/ArduCopter.cpp`

```cpp
// 任务调度表
const AP_Scheduler::Task Copter::scheduler_tasks[] = {
    FAST_TASK(update_ins),
    FAST_TASK(update_flight_mode),
    FAST_TASK(update_gps),
    FAST_TASK(update_batt),
    MED_TASK(update_compass),
    MED_TASK(update_altitude),
    SLOW_TASK(update_logging),
    SLOW_TASK(update_parachute),
};
```

### 3.2 主循环频率

| 任务 | 频率 | 说明 |
|------|------|------|
| INS | 400 Hz | IMU 读取 |
| 姿态控制 | 400 Hz | 角速率环 |
| 位置控制 | 50-100 Hz | 位置环 |
| GPS | 5-10 Hz | GPS 更新 |
| 日志 | 10 Hz | 数据记录 |

---

## 4. PID 控制器

### 4.1 AC_PID 结构

**关键文件**: `libraries/AC_PID/AC_PID.cpp`

```cpp
class AC_PID {
public:
    float update_all(float target, float measurement);
    float get_pid() const { return _pid_info.P + _pid_info.I + _pid_info.D; }

private:
    float _kp, _ki, _kd, _kff;  // 增益
    float _integrator;            // 积分项
    float _error;                 // 误差
    float _derivative;            // 微分项
    float _filt_E_rate;           // 误差微分滤波
    float _filt_T_rate;           // 目标微分滤波
};
```

### 4.2 PID 计算

```cpp
float AC_PID::update_all(float target, float measurement)
{
    _error = target - measurement;

    // P 项
    _pid_info.P = _kp * _error;

    // I 项 (带抗饱和)
    _integrator += _ki * _error * _dt;
    _integrator = constrain_float(_integrator, -_imax, _imax);
    _pid_info.I = _integrator;

    // D 项 (带滤波)
    _derivative = (_error - _error_last) / _dt;
    _derivative = _derivative_filter.apply(_derivative, _dt);
    _pid_info.D = _kd * _derivative;

    // FF 项
    _pid_info.FF = _kff * (target - _target_last) / _dt;

    _error_last = _error;
    _target_last = target;

    return _pid_info.P + _pid_info.I + _pid_info.D + _pid_info.FF;
}
```

---

## 5. 电机混控

### 5.1 X 型四旋翼

```cpp
// 电机布局 (X 型):
//     1(CCW)    2(CW)
//         \   /
//    ------+------
//         /   \
//     4(CW)    3(CCW)

// 混控因子:
// Motor  Roll   Pitch   Yaw
//   1    -1.0    1.0   -1.0
//   2     1.0    1.0    1.0
//   3     1.0   -1.0   -1.0
//   4    -1.0   -1.0    1.0
```

### 5.2 添加新构型

```cpp
// 在 AP_MotorsMatrix.cpp 中添加
void AP_MotorsMatrix::setup_quadcopter(const MatrixQuad frame_class)
{
    switch (frame_class) {
        case FRAME_TYPE_X:
            add_motor(AP_MOTORS_MOT_1, -1.0f,  1.0f, -1.0f);
            add_motor(AP_MOTORS_MOT_2,  1.0f,  1.0f,  1.0f);
            add_motor(AP_MOTORS_MOT_3,  1.0f, -1.0f, -1.0f);
            add_motor(AP_MOTORS_MOT_4, -1.0f, -1.0f,  1.0f);
            break;
    }
}
```

---

## 6. 阅读建议

### 6.1 入门路线

```
1. 先理解 AP_HAL 硬件抽象
2. 从 ArduCopter/ArduCopter.cpp 开始
3. 追踪 update_ins() → update_flight_mode()
4. 理解 Attitude.cpp 姿态控制
5. 最后看 libraries/ 中的库
```

### 6.2 重点文件

| 文件 | 重要性 | 说明 |
|------|--------|------|
| `ArduCopter/ArduCopter.cpp` | ★★★★★ | 主循环, 任务调度 |
| `ArduCopter/Attitude.cpp` | ★★★★★ | 姿态控制入口 |
| `libraries/AC_AttitudeControl/` | ★★★★★ | 姿态控制器 |
| `libraries/AP_Motors/` | ★★★★ | 电机混控 |
| `libraries/AC_PID/` | ★★★★ | PID 控制器 |
| `libraries/AP_AHRS/` | ★★★ | 姿态估计 |

---

## 下一步

→ [05 — Lua 脚本开发](05-lua-scripting.md)
