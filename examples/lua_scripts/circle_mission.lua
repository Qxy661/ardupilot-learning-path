-- circle_mission.lua
-- 圆形轨迹脚本
-- 使用 Guided 模式飞圆形

local radius = 10.0   -- 半径 (米)
local height = 10.0   -- 高度 (米)
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
