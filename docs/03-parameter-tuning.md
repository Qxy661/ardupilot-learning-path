# 03 — 参数调优指南

> 目标: 掌握ArduPilot PID调参方法论

---

## 1. 参数系统

### 1.1 参数存储

- 存储在 EEPROM/Flash
- 通过 MAVLink 远程读写
- Mission Planner 图形化修改
- 参数文件 `.parm` 批量导入/导出

### 1.2 查看和修改参数

```bash
# 在 MAVProxy 中:

# 查看参数
param show ATC_RAT_RLL_P

# 搜索参数
param show *RLL*

# 修改参数
param set ATC_RAT_RLL_P 0.15

# 保存参数
param save

# 加载参数文件
param load my_params.parm
```

### 1.3 参数分组

| 前缀 | 类别 | 示例 |
|------|------|------|
| `ATC_` | 姿态控制 | `ATC_RAT_RLL_P` |
| `PSC_` | 位置控制 | `PSC_POSXY_P` |
| `MOT_` | 电机 | `MOT_THST_EXPO` |
| `GPS_` | GPS | `GPS_TYPE` |
| `COMPASS_` | 磁力计 | `COMPASS_OFS_X` |
| `BATT_` | 电池 | `BATT_MONITOR` |
| `EK3_` | EKF3 | `EK3_IMU_MASK` |
| `RC_` | 遥控器 | `RC1_MIN` |
| `FENCE_` | 地理围栏 | `FENCE_ENABLE` |
| `RALLY_` | 集结点 | `RALLY_LIMIT_KM` |

---

## 2. PID 调参方法论

### 2.1 调参原则

**核心规则**: 从内环到外环, 从P开始再加D, 最后加I

```
位置环 (外环)
    ↓ 期望姿态
姿态环 (中环)
    ↓ 期望角速率
角速率环 (内环)
    ↓ 电机输出
```

### 2.2 调参顺序

```
1. 角速率环 (ATC_RAT_RLL / ATC_RAT_PIT / ATC_RAT_YAW)
   - 先调 P, 看响应速度
   - 再加 D, 抑制振荡
   - 最后加 I, 消除稳态误差

2. 姿态环 (ATC_ANG_RLL / ATC_ANG_PIT / ATC_ANG_YAW)
   - 只需调 P
   - 不要太大, 否则超调

3. 位置环 (PSC_POSXY / PSC_POSZ / PSC_VELXY / PSC_VELZ)
   - 位置 P 决定跟踪速度
   - 速度 P 决定响应刚度
```

---

## 3. 角速率环调参

### 3.1 关键参数

| 参数 | 默认值 | 作用 | 调参范围 |
|------|--------|------|----------|
| `ATC_RAT_RLL_P` | 0.135 | 比例增益 | 0.08-0.25 |
| `ATC_RAT_RLL_I` | 0.135 | 积分增益 | 0.08-0.3 |
| `ATC_RAT_RLL_D` | 0.0036 | 微分增益 | 0.001-0.01 |
| `ATC_RAT_PIT_P` | 0.135 | 俯仰P | 同滚转 |
| `ATC_RAT_YAW_P` | 0.18 | 偏航P | 0.1-0.4 |
| `ATC_RAT_YAW_I` | 0.018 | 偏航I | 0.01-0.05 |

### 3.2 调参步骤

```bash
# Step 1: 设置安全参数
param set ATC_RAT_RLL_P 0.1
param set ATC_RAT_RLL_I 0
param set ATC_RAT_RLL_D 0

# Step 2: 起飞悬停
arm throttle
takeoff 5

# Step 3: 观察日志 (用 Mission Planner)
# 如果振荡 → P 太大, 减小
# 如果响应慢 → P 太小, 增大

# Step 4: 加入 D (抑制振荡)
param set ATC_RAT_RLL_D 0.003

# Step 5: 加入 I (消除稳态误差)
param set ATC_RAT_RLL_I 0.135
```

### 3.3 调参技巧

**P 增益过大**: 高频振荡 (10-20Hz), 电机声音尖锐
**P 增益过小**: 响应迟钝, 位置跟踪差
**D 增益过大**: 低频抖动 (1-5Hz)
**D 增益过小**: 振荡衰减慢
**I 增益过大**: 低频大幅摆动
**I 增益过小**: 存在稳态误差

---

## 4. 姿态环调参

### 4.1 关键参数

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `ATC_ANG_RLL_P` | 4.5 | 滚转角P增益 |
| `ATC_ANG_PIT_P` | 4.5 | 俯仰角P增益 |
| `ATC_ANG_YAW_P` | 4.5 | 偏航角P增益 |

### 4.2 调参方法

```bash
# 姿态环 P 通常不需要大幅调整
# 如果振荡: 减小 ATC_ANG_RLL_P
# 如果跟踪慢: 增大 ATC_ANG_RLL_P

# 测试方法: Mission Planner 中做阶跃输入
# 观察: 超调 < 20%, 调节时间 < 1s
```

---

## 5. 位置环调参

### 5.1 关键参数

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `PSC_POSXY_P` | 1.0 | 水平位置P |
| `PSC_VELXY_P` | 2.0 | 水平速度P |
| `PSC_VELXY_I` | 1.0 | 水平速度I |
| `PSC_VELXY_D` | 0.5 | 水平速度D |
| `PSC_POSZ_P` | 1.0 | 垂直位置P |
| `PSC_VELZ_P` | 5.0 | 垂直速度P |
| `PSC_VELZ_I` | 2.0 | 垂直速度I |

### 5.2 位置环结构

```
位置误差 → PSC_POSXY_P → 期望速度
    ↓
速度误差 → PSC_VELXY_P → 期望加速度
    ↓
加速度 → 姿态控制器
```

### 5.3 调参方法

```bash
# 水平位置跟踪
param set PSC_POSXY_P 1.0
param set PSC_VELXY_P 2.0
param set PSC_VELXY_D 0.5

# 垂直位置跟踪
param set PSC_POSZ_P 1.0
param set PSC_VELZ_P 5.0

# 测试: Mission Planner 中拖动位置
# 观察: 跟踪误差、超调、振荡
```

---

## 6. 推力模型

### 6.1 关键参数

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `MOT_THST_EXPO` | 0.65 | 推力曲线指数 |
| `MOT_THST_HOVER` | 0.35 | 悬停油门 |
| `MOT_SPIN_MIN` | 0.15 | 最小油门 |
| `MOT_SPIN_MAX` | 0.95 | 最大油门 |

### 6.2 推力模型

```
实际推力 = 油门^MOT_THST_EXPO
```

- `MOT_THST_EXPO = 0`: 线性关系
- `MOT_THST_EXPO = 0.65`: 默认 (推荐)
- `MOT_THST_EXPO = 1.0`: 完全二次关系

```bash
# 设置推力模型
param set MOT_THST_EXPO 0.65

# 调整悬停油门
param set MOT_THST_HOVER 0.35
```

---

## 7. Autotune (自动调参)

### 7.1 使用 Autotune

```bash
# 1. 起飞到安全高度
arm throttle
takeoff 10

# 2. 切换到 Autotune 模式
mode autotune

# 3. 等待完成 (约2-5分钟)
# 飞机会自动做振荡测试

# 4. 保存参数
param save
```

### 7.2 Autotune 注意事项

```
1. 在无风环境下进行
2. 电池电量充足 (> 50%)
3. 场地空旷 (> 20m × 20m)
4. 随时准备切换手动模式
5. Autotune 后手动验证
```

---

## 8. 电池参数

### 8.1 关键参数

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `BATT_MONITOR` | 0 | 电池监控类型 |
| `BATT_CAPACITY` | 0 | 电池容量 (mAh) |
| `BATT_LOW_VOLT` | 0 | 低压阈值 |
| `BATT_LOW_MAH` | 0 | 低容量阈值 |
| `BATT_CRT_VOLT` | 0 | 危险电压阈值 |
| `BATT_CRT_MAH` | 0 | 危险容量阈值 |

### 8.2 配置示例

```bash
# 启用电压和电流监控
param set BATT_MONITOR 4

# 4S LiPo 电池
param set BATT_CAPACITY 2200
param set BATT_LOW_VOLT 14.0
param set BATT_LOW_MAH 440
param set BATT_CRT_VOLT 13.6
param set BATT_CRT_MAH 220
```

---

## 9. 安全参数

### 9.1 地理围栏

```bash
# 启用围栏
param set FENCE_ENABLE 1

# 设置围栏类型
param set FENCE_TYPE 7  # 圆形+多边形+高度

# 设置围栏半径
param set FENCE_RADIUS 500  # 米

# 设置最大高度
param set FENCE_ALT_MAX 100  # 米

# 超出围栏动作
param set FENCE_ACTION 1  # RTL
```

### 9.2 失控保护

```bash
# 遥控器丢失动作
param set FS_THR_ENABLE 1  # 启用
param set FS_THR_VALUE 975  # 油门阈值
param set FS_GCS_ENABLE 1  # 地面站丢失
```

---

## 10. 常见调参问题

### Q: 悬停时高频振荡

```bash
# 原因: 角速率环 P 或 D 太大
param set ATC_RAT_RLL_P 0.1
param set ATC_RAT_RLL_D 0.002
```

### Q: 转弯时掉高

```bash
# 原因: 垂直速度环 I 不够
param set PSC_VELZ_I 2.0
```

### Q: 位置跟踪有稳态误差

```bash
# 原因: 速度环 I 不够
param set PSC_VELXY_I 1.0
```

### Q: 松杆后飞机漂移

```bash
# 原因: 位置环增益太小
param set PSC_POSXY_P 1.5
```

---

## 下一步

→ [04 — 源码阅读指南](04-code-reading.md)
