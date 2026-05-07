# ArduPilot 快速参考卡

> 一页纸速查, 打印出来贴在工位上

---

## SITL 启动

```bash
cd ~/ardupilot/Tools/autotest
sim_vehicle.py -v ArduCopter --console --map      # 四旋翼
sim_vehicle.py -v ArduPlane --console --map        # 固定翼
sim_vehicle.py -v Rover --console --map            # 车辆
sim_vehicle.py -v ArduCopter --console --no-map    # 无GUI
sim_vehicle.py -v ArduCopter --speedup 4           # 加速仿真
```

## MAVProxy 命令

```bash
arm throttle                   # 解锁
disarm                         # 上锁
takeoff 10                     # 起飞到10m
mode loiter                    # 位置保持
mode rtl                       # 返航
mode land                      # 降落
mode auto                      # 自动航线
mode guided                    # 外部引导
mode autotune                  # 自动调参
status                         # 查看状态
wp list                        # 查看航点
wp load mission.txt            # 加载航点
```

## 参数操作

```bash
param show ATC_RAT_RLL_P       # 查看参数
param show *RLL*               # 搜索参数
param set ATC_RAT_RLL_P 0.15   # 设置参数
param save                     # 保存参数
param load my_params.parm      # 加载参数文件
```

## 模块加载

```bash
module load map                # 加载地图
module load console            # 加载控制台
module load graph              # 加载图形
module list                    # 查看模块
```

## PID 调参速查

```
调参顺序: 角速率环 → 姿态环 → 位置环

角速率环 (内环):
  ATC_RAT_RLL_P   0.08-0.25   (振荡→减小, 迟钝→增大)
  ATC_RAT_RLL_D   0.001-0.01  (抖动→减小)
  ATC_RAT_RLL_I   0.08-0.3    (稳态误差→增大)

姿态环 (中环):
  ATC_ANG_RLL_P   3.0-6.0     (超调→减小)

位置环 (外环):
  PSC_POSXY_P     0.5-2.0     (跟踪慢→增大)
  PSC_VELXY_P     1.0-4.0     (响应刚度)
  PSC_POSZ_P      0.5-2.0     (高度跟踪)
```

## 关键参数速查

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `ATC_RAT_RLL_P` | 0.135 | 滚转角速率P |
| `ATC_RAT_PIT_P` | 0.135 | 俯仰角速率P |
| `ATC_RAT_YAW_P` | 0.18 | 偏航角速率P |
| `ATC_ANG_RLL_P` | 4.5 | 滚转角P |
| `PSC_POSXY_P` | 1.0 | 水平位置P |
| `PSC_VELZ_P` | 5.0 | 垂直速度P |
| `MOT_THST_EXPO` | 0.65 | 推力曲线指数 |
| `MOT_THST_HOVER` | 0.35 | 悬停油门 |
| `FENCE_ENABLE` | 0 | 地理围栏 |

## 飞行模式

| 模式 | 说明 | 命令 |
|------|------|------|
| Stabilize | 手动, 姿态稳定 | `mode stabilize` |
| AltHold | 高度保持 | `mode althold` |
| Loiter | 位置保持 | `mode loiter` |
| Auto | 自动航线 | `mode auto` |
| RTL | 返航 | `mode rtl` |
| Land | 降落 | `mode land` |
| Guided | 外部引导 | `mode guided` |
| AutoTune | 自动调参 | `mode autotune` |

## 坐标系

```
ArduPilot 使用 NED (北东地):
  X = 北 (North)
  Y = 东 (East)
  Z = 地 (Down, 向下为正)

ROS2 使用 ENU (东北天):
  X = 东 (East)
  Y = 北 (North)
  Z = 天 (Up, 向上为正)

转换: NED[x,y,z] → ENU[y,x,-z]
```

## 数据流

```
传感器 → AHRS → 飞行模式 → 姿态控制 → 角速率控制 → 电机混控 → 电机
```

## 日志分析

```bash
# 日志位置
~/ardupilot/logs/

# 关键日志字段
ATT     - 姿态 (Roll/Pitch/Yaw)
CTUN    - 控制 (NavRoll/NavPitch/Throttle)
NTUN    - 导航 (WpDist/NavBrg)
POS     - 位置 (Lat/Lng/Alt)
BAT     - 电池 (Volt/Curr)
IMU     - IMU (AccX/AccY/AccZ)
```

## 故障排查

```
高频振荡 (10-20Hz) → 减小 ATC_RAT_RLL_P/D
低频摆动 (1-5Hz)   → 减小 ATC_ANG_RLL_P
位置漂移           → 增大 PSC_POSXY_P
转弯掉高           → 增大 PSC_VELZ_I
GPS不锁定          → 移到室外, 等待2分钟
起飞翻车           → 检查螺旋桨/电机转向
遥控器无响应       → 重新对频+校准
```

## Lua 脚本

```bash
# 启用脚本
param set SCR_ENABLE 1
param set SCR_HEAP_SIZE 102400

# 脚本位置
SD卡/APM/scripts/

# 重载脚本
scripting reload
```

## ROS2 + MAVROS

```bash
# 启动 MAVROS
ros2 launch mavros apm.launch fcu_url:=tcp://127.0.0.1:5760

# 查看话题
ros2 topic list
ros2 topic echo /mavros/state

# 检查连接
ros2 topic echo /mavros/local_position/pose
```
