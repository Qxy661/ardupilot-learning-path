# ArduPilot 常用参数列表

> 按功能分类的常用参数速查

---

## 姿态控制 (ATC_)

### 角速率环

| 参数 | 默认值 | 作用 | 调参范围 |
|------|--------|------|----------|
| `ATC_RAT_RLL_P` | 0.135 | 滚转角速率P | 0.08-0.25 |
| `ATC_RAT_RLL_I` | 0.135 | 滚转角速率I | 0.08-0.3 |
| `ATC_RAT_RLL_D` | 0.0036 | 滚转角速率D | 0.001-0.01 |
| `ATC_RAT_PIT_P` | 0.135 | 俯仰角速率P | 同滚转 |
| `ATC_RAT_PIT_I` | 0.135 | 俯仰角速率I | 同滚转 |
| `ATC_RAT_PIT_D` | 0.0036 | 俯仰角速率D | 同滚转 |
| `ATC_RAT_YAW_P` | 0.18 | 偏航角速率P | 0.1-0.4 |
| `ATC_RAT_YAW_I` | 0.018 | 偏航角速率I | 0.01-0.05 |

### 姿态环

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `ATC_ANG_RLL_P` | 4.5 | 滚转角P |
| `ATC_ANG_PIT_P` | 4.5 | 俯仰角P |
| `ATC_ANG_YAW_P` | 4.5 | 偏航角P |
| `ATC_ANG_LIM_TC` | 0.5 | 姿态限制时间常数 |

---

## 位置控制 (PSC_)

### 水平位置

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `PSC_POSXY_P` | 1.0 | 水平位置P |
| `PSC_VELXY_P` | 2.0 | 水平速度P |
| `PSC_VELXY_I` | 1.0 | 水平速度I |
| `PSC_VELXY_D` | 0.5 | 水平速度D |

### 垂直位置

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `PSC_POSZ_P` | 1.0 | 垂直位置P |
| `PSC_VELZ_P` | 5.0 | 垂直速度P |
| `PSC_VELZ_I` | 2.0 | 垂直速度I |

---

## 电机 (MOT_)

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `MOT_THST_EXPO` | 0.65 | 推力曲线指数 |
| `MOT_THST_HOVER` | 0.35 | 悬停油门 |
| `MOT_SPIN_MIN` | 0.15 | 最小油门 |
| `MOT_SPIN_MAX` | 0.95 | 最大油门 |
| `MOT_PWM_TYPE` | 0 | PWM 类型 |
| `MOT_SAFE_DISARM` | 0 | 上锁时电机行为 |

---

## 电池 (BATT_)

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `BATT_MONITOR` | 0 | 电池监控类型 |
| `BATT_CAPACITY` | 0 | 电池容量 (mAh) |
| `BATT_LOW_VOLT` | 0 | 低压阈值 (V) |
| `BATT_LOW_MAH` | 0 | 低容量阈值 (mAh) |
| `BATT_CRT_VOLT` | 0 | 危险电压 (V) |
| `BATT_CRT_MAH` | 0 | 危险容量 (mAh) |
| `BATT_FS_LOW_ACT` | 0 | 低压保护动作 |
| `BATT_FS_CRT_ACT` | 0 | 危险电压动作 |

---

## GPS (GPS_)

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `GPS_TYPE` | 1 | GPS 类型 |
| `GPS_TYPE2` | 0 | 第二 GPS 类型 |
| `GPS_AUTO_SWITCH` | 1 | 自动切换 |
| `GPS_MIN_ELEV` | 10 | 最小仰角 |
| `GPS_SBAS_MODE` | 0 | SBAS 模式 |

---

## EKF3 (EK3_)

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `EK3_IMU_MASK` | 7 | 使用的 IMU |
| `EK3_GPS_CHECK` | 31 | GPS 检查 |
| `EK3_MAG_CAL` | 3 | 磁力计校准 |
| `EK3_SRC1_POSXY` | 0 | 水平位置源 |
| `EK3_SRC1_POSZ` | 0 | 垂直位置源 |

---

## 地理围栏 (FENCE_)

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `FENCE_ENABLE` | 0 | 启用围栏 |
| `FENCE_TYPE` | 7 | 围栏类型 |
| `FENCE_RADIUS` | 0 | 半径 (m) |
| `FENCE_ALT_MAX` | 0 | 最大高度 (m) |
| `FENCE_ACTION` | 0 | 超出动作 |
| `FENCE_MARGIN` | 0 | 边距 (m) |

---

## 失控保护 (FS_)

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `FS_THR_ENABLE` | 0 | 油门失控保护 |
| `FS_THR_VALUE` | 975 | 油门阈值 |
| `FS_GCS_ENABLE` | 0 | 地面站丢失保护 |
| `FS_EKF_THRESH` | 0.8 | EKF 阈值 |

---

## 日志 (LOG_)

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `LOG_BITMASK` | 830 | 日志掩码 |
| `LOG_DISARMED` | 0 | 上锁时记录 |
| `LOG_REPLAY` | 0 | 重放模式 |
| `LOG_FILE_BUFSIZE` | 20 | 缓冲区大小 |

---

## 通道 (RC_)

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `RC1_MIN` | 1100 | 通道1最小值 |
| `RC1_MAX` | 1900 | 通道1最大值 |
| `RC1_TRIM` | 1500 | 通道1中位值 |
| `RC1_REV` | 1 | 通道1反转 |
| `RC1_DZ` | 30 | 通道1死区 |

---

## 飞行模式

| 模式 | 说明 | MAVProxy 命令 |
|------|------|---------------|
| Stabilize | 手动, 姿态稳定 | `mode stabilize` |
| Acro | 手动, 角速率 | `mode acro` |
| AltHold | 高度保持 | `mode althold` |
| Loiter | 位置保持 | `mode loiter` |
| Auto | 自动航线 | `mode auto` |
| RTL | 返航 | `mode rtl` |
| Land | 降落 | `mode land` |
| Guided | 外部引导 | `mode guided` |
| Sport | 运动模式 | `mode sport` |
| Flip | 翻滚 | `mode flip` |
| AutoTune | 自动调参 | `mode autotune` |
| PosHold | 位置保持 | `mode poshold` |
