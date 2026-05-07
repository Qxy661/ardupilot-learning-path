-- sensor_logger.lua
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
