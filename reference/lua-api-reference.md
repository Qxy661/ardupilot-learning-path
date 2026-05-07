# ArduPilot Lua API 参考

> 常用 Lua API 速查

---

## 全局对象

| 对象 | 说明 | 示例 |
|------|------|------|
| `ahrs` | 姿态参考 | `ahrs:get_roll()` |
| `arming` | 解锁控制 | `arming:is_armed()` |
| `battery` | 电池状态 | `battery:voltage(0)` |
| `gcs` | 地面站通信 | `gcs:send_text(0, "msg")` |
| `gps` | GPS | `gps:num_sats()` |
| `ins` | IMU | `ins:get_accel()` |
| `logger` | 日志 | `logger:write("TEST", "Val", "f", "1.0")` |
| `mission` | 任务 | `mission:get_current_do_cmd_id()` |
| `param` | 参数 | `param:get("SCR_TEST")` |
| `rc` | 遥控器 | `rc:get_pwm(1)` |
| `serial` | 串口 | `serial:find_serial(0)` |
| `vehicle` | 载具控制 | `vehicle:set_mode(0)` |

---

## ahrs (姿态参考)

```lua
-- 获取姿态 (弧度)
local roll = ahrs:get_roll()      -- 滚转角
local pitch = ahrs:get_pitch()    -- 俯仰角
local yaw = ahrs:get_yaw()        -- 偏航角

-- 获取位置
local pos = ahrs:get_position()   -- Location 对象
local lat = pos:lat() * 1e-7      -- 纬度
local lng = pos:lng() * 1e-7      -- 经度
local alt = pos:alt() * 0.01      -- 高度 (m)

-- 获取速度
local vel = ahrs:get_velocity_NED()  -- NED 速度
local vn = vel:x()                   -- 北向速度
local ve = vel:y()                   -- 东向速度
local vd = vel:z()                   -- 地向速度

-- 获取地面航向
local ground_track = ahrs:ground_track()  -- 弧度

-- 获取地速
local groundspeed = ahrs:groundspeed()    -- m/s

-- 获取空速
local airspeed = ahrs:airspeed_estimate()  -- m/s
```

---

## arming (解锁控制)

```lua
-- 检查是否解锁
if arming:is_armed() then
    gcs:send_text(6, "已解锁")
end

-- 解锁
arming:arm()

-- 上锁
arming:disarm()

-- 检查是否可以解锁
if arming:pre_arm_checks(true) then
    gcs:send_text(6, "预检通过")
end
```

---

## battery (电池)

```lua
-- 获取电压
local voltage = battery:voltage(0)  -- 第一个电池, 伏特

-- 获取电流
local current = battery:current_amps(0)  -- 安培

-- 获取剩余百分比
local remaining = battery:capacity_remaining_pct(0)  -- 0-100

-- 获取消耗容量
local consumed = battery:consumed_mah(0)  -- mAh

-- 检查电池是否存在
if battery:has_cell_voltages(0) then
    local cells = battery:get_cell_voltages(0)
end
```

---

## gcs (地面站通信)

```lua
-- 发送文本消息
gcs:send_text(severity, message)

-- 严重级别:
-- 0: Emergency
-- 1: Alert
-- 2: Critical
-- 3: Error
-- 4: Warning
-- 5: Notice
-- 6: Info
-- 7: Debug

-- 发送遥测值
gcs:send_named_float("name", value)

-- 获取协议版本
local protocol = gcs:link_type(0)
```

---

## gps (GPS)

```lua
-- 获取卫星数
local sats = gps:num_sats()

-- 获取 HDOP
local hdop = gps:get_hdop()  -- 0.01 单位

-- 获取 GPS 状态
local status = gps:status()
-- 0: NO_GPS
-- 1: NO_FIX
-- 2: FIX_2D
-- 3: FIX_3D
-- 4: FIX_3D_DGPS
-- 5: FIX_3D_RTK_FLOAT
-- 6: FIX_3D_RTK_FIXED

-- 获取位置
local pos = gps:location()
local lat = pos:lat() * 1e-7
local lng = pos:lng() * 1e-7
```

---

## ins (IMU)

```lua
-- 获取加速度
local accel = ins:get_accel(0)  -- 第一个 IMU
local ax = accel:x()
local ay = accel:y()
local az = accel:z()

-- 获取角速度
local gyro = ins:get_gyro(0)
local gx = gyro:x()
local gy = gyro:y()
local gz = gyro:z()

-- 获取温度
local temp = ins:get_temperature(0)

-- 检查 IMU 数量
local count = ins:get_accel_count()
```

---

## rc (遥控器)

```lua
-- 获取通道 PWM 值
local ch1 = rc:get_pwm(1)  -- 通道1, 1000-2000
local ch2 = rc:get_pwm(2)  -- 通道2

-- 获取通道数
local num_channels = rc:get_valid_chan_count()

-- 检查是否有新数据
if rc:has_valid_input() then
    -- 处理遥控器输入
end
```

---

## serial (串口)

```lua
-- 查找串口
local port = serial:find_serial(0)  -- 第一个串口

-- 配置串口
port:begin(115200)  -- 波特率
port:set_flow_control(0)  -- 无流控

-- 读取数据
local available = port:available()
if available > 0 then
    local byte = port:read()
end

-- 写入数据
port:write(byte)
port:write_string("Hello")

-- 设置超时
port:set_timeout(100)  -- ms
```

---

## vehicle (载具控制)

```lua
-- 获取模式
local mode = vehicle:get_mode()

-- 设置模式
vehicle:set_mode(0)  -- Stabilize
vehicle:set_mode(5)  -- Loiter
vehicle:set_mode(6)  -- RTL

-- 获取目标位置
local target = vehicle:get_target_location()

-- 设置目标位置
local loc = Location()
loc:lat(377749000)  -- 纬度 * 1e7
loc:lng(-1224194000) -- 经度 * 1e7
loc:alt(1000)        -- 高度 * 100 (cm)
vehicle:set_target_location(loc)

-- 起飞
vehicle:start_takeoff(10)  -- 10米

-- 降落
vehicle:set_mode(9)  -- LAND

-- 获取高度
local alt = vehicle:get_altitude()  -- m
```

---

## Location 对象

```lua
-- 创建位置
local loc = Location()

-- 设置坐标
loc:lat(lat * 1e7)   -- 纬度
loc:lng(lng * 1e7)   -- 经度
loc:alt(alt * 100)   -- 高度 (cm)

-- 获取坐标
local lat = loc:lat() * 1e-7
local lng = loc:lng() * 1e-7
local alt = loc:alt() * 0.01

-- 计算距离
local distance = loc:get_distance(other_loc)  -- 米

-- 计算方位
local bearing = loc:get_bearing(other_loc)  -- 弧度

-- 偏移
local new_loc = loc:offset(dx, dy)  -- 偏移量 (米)
```

---

## logger (日志)

```lua
-- 写入日志
logger:write("TEST", "Val,Name", "fB", value, name)

-- 类型码:
-- f: float
-- d: double
-- B: uint8_t
-- H: uint16_t
-- I: uint32_t
-- b: int8_t
-- h: int16_t
-- i: int32_t
-- Q: uint64_t
-- q: int64_t
-- n: char[4]
-- N: char[16]
-- Z: char[64]
```

---

## param (参数)

```lua
-- 获取参数值
local p = param:get("ATC_RAT_RLL_P")

-- 设置参数值
param:set("ATC_RAT_RLL_P", 0.15)

-- 添加自定义参数
local params_table = {
    {"SCR_TEST_P", 1.0, 0.0, 10.0},
}
assert(param:add_table(params_table), "参数注册失败")
```

---

## mission (任务)

```lua
-- 获取当前航点
local seq = mission:get_current_nav_cmd().index

-- 获取航点数量
local count = mission:num_commands()

-- 获取当前模式
local mode = mission:state()
-- 0: 不活动
-- 1: 活动
-- 2: 暂停
-- 3: 完成
```

---

## 定时器和回调

```lua
-- 主循环 (必须)
function update()
    -- 你的代码
    return update, 1000  -- 1000ms 后再次调用
end

return update, 0  -- 立即开始
```

---

## 模式名称映射 (ArduCopter)

| 模式号 | 名称 | 说明 |
|--------|------|------|
| 0 | Stabilize | 手动, 姿态稳定 |
| 1 | Acro | 手动, 角速率 |
| 2 | AltHold | 高度保持 |
| 3 | Auto | 自动航线 |
| 4 | Guided | 外部引导 |
| 5 | Loiter | 位置保持 |
| 6 | RTL | 返航 |
| 7 | Circle | 盘旋 |
| 9 | Land | 降落 |
| 11 | Drift | 漂移模式 |
| 13 | Sport | 运动模式 |
| 14 | Flip | 翻滚 |
| 15 | AutoTune | 自动调参 |
| 16 | PosHold | 位置保持 |
| 17 | Brake | 刹车 |
| 18 | Throw | 抛飞 |
| 19 | Avoid_ADSB | ADSB 避障 |
| 20 | Guided_NoGPS | 无GPS引导 |
