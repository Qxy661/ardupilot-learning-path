-- hello_world.lua
-- Hello World 示例脚本
-- 每秒打印一次消息

local count = 0

function update()
    count = count + 1
    gcs:send_text(0, string.format("Hello World! 计数: %d", count))
    return update, 1000  -- 每1000ms调用一次
end

return update, 0  -- 立即开始
