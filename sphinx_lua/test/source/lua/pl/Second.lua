---@module pl.Second

---@class Second
local cls = {}
cls.__index = cls

---Create a new Second
---@return Second
function cls.new()
    return setmetatable({}, cls)
end
