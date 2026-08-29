---@module pl.Second

---@alias SourceFn fun(chunk:string):string|nil

---@class Second
local cls = {}
cls.__index = cls

---Create a new Second
---@param callback SourceFn
---@return Second
function cls.new(callback)
    return setmetatable({}, cls)
end
