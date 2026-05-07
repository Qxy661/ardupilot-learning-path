# 05 — Lua 脚本开发

> 目标: 学会使用 Lua 脚本扩展 ArduPilot 功能

---

## 1. 什么是 Lua 脚本

ArduPilot 支持使用 Lua 脚本扩展功能:
- 不需要重新编译固件
- 运行在飞控上
- 可以访问传感器数据、发送命令
- 适合轻量级任务

---

## 2. 环境配置

### 2.1 启用 Lua 脚本

```bash
# 在 MAVProxy 中:
param set SCR_ENABLE 1
param set SCR_HEAP_SIZE 102400  # 内存分配 (字节)
```

### 2.2 脚本位置

脚本放在 SD 卡的 `APM/scripts/` 目录:

```
SD卡/
└── APM/
    └── scripts/
        ├── hello_world.lua
        ├── circle_mission.lua
        └── sensor_logger.lua
```

### 2.3 加载脚本

```bash
# 在 MAVProxy 中:
# 脚本会自动加载

# 手动重载
scripting reload

# 查看脚本状态
scripting status
```

---

## 3. Hello World 示例

**hello_world.lua**:

```lua
-- Hello World 示例
-- 每秒打印一次消息

local count = 0

function update()
    count = count + 1
    gcs:send_text(0, string.format("Hello World! 计数: %d", count))
    return update, 1000  -- 每1000ms调用一次
end

return update, 0  -- 立即开始
```

---

## 4. 传感器读取

**sensor_logger.lua**:

```lua
-- 传感器数据记录器
-- 读取并显示 IMU、GPS、电池数据

function update()
    -- 读取姿态
    local roll = math.deg(ahrs:get_roll())
    local pitch = math.deg(ahrs:get_pitch())
    local yaw = math.deg(ahrs:get_yaw())

    -- 读取位置
    local pos = ahrs:get_position()
    local lat = pos:lat() * 1e-7
    local lng = pos:lng() * 1e-7
    local alt = pos:alt() * 0.01

    -- 读取电池
    local voltage = battery:voltage(0)
    local current = battery:current_amps(0)
    local remaining = battery:capacity_remaining_pct(0)

    -- 发送到地面站
    gcs:send_text(6, string.format(
        "姿态: R=%.1f P=%.1f Y=%.1f | 位置: %.6f,%.6f,%.1fm | 电池: %.1fV %.1fA %d%%",
        roll, pitch, yaw, lat, lng, alt, voltage, current, remaining))

    return update, 1000  -- 每秒更新
end

return update, 5000  -- 延迟5秒开始
```

---

## 5. 任务脚本

**circle_mission.lua**:

```lua
-- 圆形轨迹脚本
-- 使用 Guided 模式飞圆形

local radius = 10.0   -- 半径 (米)
local height = 10.0   -- 高度 (米)
local speed = 5.0     -- 速度 (m/s)
local center_lat = 0  -- 中心纬度
local center_lng = 0  -- 中心经度
local angle = 0       -- 当前角度
local is_flying = false

function update()
    -- 检查是否解锁
    if not arming:is_armed() then
        return update, 1000
    end

    -- 首次运行, 记录中心点
    if not is_flying then
        local pos = ahrs:get_position()
        if pos then
            center_lat = pos:lat()
            center_lng = pos:lng()
            is_flying = true
            gcs:send_text(6, "开始圆形轨迹")
        end
        return update, 1000
    end

    -- 计算目标点
    angle = angle + 0.05  -- 约3度/步
    if angle >= 2 * math.pi then
        angle = angle - 2 * math.pi
    end

    local target_lat = center_lat + radius * math.cos(angle) * 1e-7 / 111320
    local target_lng = center_lng + radius * math.sin(angle) * 1e-7 / (111320 * math.cos(math.rad(center_lat * 1e-7)))

    -- 发送目标点
    local target = Location()
    target:lat(target_lat * 1e7)
    target:lng(target_lng * 1e7)
    target:alt(height * 100)

    vehicle:set_target_location(target)

    return update, 200  -- 5Hz 更新
end

return update, 5000  -- 延迟5秒开始
```

---

## 6. 传感器驱动示例

**custom_sensor.lua**:

```lua
-- 自定义传感器驱动示例
-- 读取串口数据并发布

-- 配置串口
local port = serial:find_serial(0)  -- 第一个串口
if not port then
    gcs:send_text(3, "找不到串口!")
    return
end

port:begin(115200)  -- 波特率
port:set_flow_control(0)

local buffer = ""

function update()
    -- 读取串口数据
    local available = port:available()
    if available > 0 then
        for i = 1, available do
            local byte = port:read()
            if byte > 0 then
                local char = string.char(byte)
                if char == "\n" then
                    -- 处理完整行
                    process_line(buffer)
                    buffer = ""
                else
                    buffer = buffer .. char
                end
            end
        end
    end

    return update, 10  -- 100Hz
end

function process_line(line)
    -- 解析数据 (示例: "DIST:123.4")
    local dist = string.match(line, "DIST:([%d%.]+)")
    if dist then
        -- 发送到地面站
        gcs:send_text(6, string.format("距离: %.1f m", tonumber(dist)))

        -- 可以存储到日志
        logger:write("CUST", "Dist", "f", tostring(dist))
    end
end

return update, 1000
```

---

## 7. 参数定义

**custom_params.lua**:

```lua
-- 自定义参数示例

-- 定义参数表
local params_table = {
    -- 参数名, 默认值, 最小值, 最大值
    {"SCR_TEST_P", 1.0, 0.0, 10.0},
    {"SCR_TEST_I", 0.5, 0.0, 5.0},
    {"SCR_TEST_D", 0.1, 0.0, 1.0},
}

-- 注册参数
assert(param:add_table(params_table), "参数注册失败")

-- 读取参数
local p = param:get("SCR_TEST_P") or 1.0
local i = param:get("SCR_TEST_I") or 0.5
local d = param:get("SCR_TEST_D") or 0.1

gcs:send_text(6, string.format("PID参数: P=%.2f I=%.2f D=%.2f", p, i, d))
```

---

## 8. 事件处理

**event_handler.lua**:

```lua
-- 事件处理示例
-- 模式切换时执行动作

local last_mode = -1

function update()
    -- 获取当前模式
    local mode = vehicle:get_mode()

    -- 检测模式切换
    if mode ~= last_mode then
        on_mode_change(last_mode, mode)
        last_mode = mode
    end

    return update, 100  -- 10Hz
end

function on_mode_change(old_mode, new_mode)
    -- 模式名称映射
    local mode_names = {
        [0] = "Stabilize",
        [2] = "AltHold",
        [5] = "Loiter",
        [6] = "RTL",
        [9] = "Land",
    }

    local old_name = mode_names[old_mode] or "Unknown"
    local new_name = mode_names[new_mode] or "Unknown"

    gcs:send_text(6, string.format("模式切换: %s → %s", old_name, new_name))

    -- 特定模式切换动作
    if new_mode == 6 then  -- RTL
        gcs:send_text(5, "返航中...")
        -- 可以执行额外动作, 如LED闪烁
    elseif new_mode == 9 then  -- Land
        gcs:send_text(5, "降落中...")
    end
end

return update, 1000
```

---

## 9. 调试技巧

### 9.1 打印消息

```lua
-- 不同级别
gcs:send_text(0, "Emergency")  -- 紧急
gcs:send_text(1, "Alert")      -- 警报
gcs:send_text(2, "Critical")   -- 严重
gcs:send_text(3, "Error")      -- 错误
gcs:send_text(4, "Warning")    -- 警告
gcs:send_text(5, "Notice")     -- 注意
gcs:send_text(6, "Info")       -- 信息
gcs:send_text(7, "Debug")      -- 调试
```

### 9.2 查看脚本状态

```bash
# 在 MAVProxy 中:
scripting status

# 查看脚本输出
# 在 Mission Planner 的 Messages 标签页
```

### 9.3 内存监控

```lua
-- 检查内存使用
local mem_used = collectgarbage("count")
gcs:send_text(6, string.format("内存使用: %.1f KB", mem_used))
```

---

## 10. 最佳实践

```
1. 脚本要简洁, 避免复杂逻辑
2. 使用 return update, interval 控制频率
3. 处理异常情况 (传感器故障等)
4. 不要在 update() 中做阻塞操作
5. 使用 param:get() 读取参数, 方便调整
6. 添加日志记录, 方便调试
7. 测试时使用仿真环境
```

---

## 下一步

→ [06 — ROS2 集成](06-ros2-integration.md)
