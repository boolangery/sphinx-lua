---@class Class
---@field public some_public_field string This field is public
---@field private _some_private_field string This field is private
local cls = {}
cls.__index = cls

---Create a new Class
---@return Class
function cls.new()
    return setmetatable({
        some_public_field = "public",
        _some_private_field = "private",
    }, cls)
end

---Append the public field with `public`
---
---Example:
---```lua
---list:more_public()
---```
function cls:more_public()
    self.some_public_field = self.some_public_field .. "public"
end

---Append the private field with `private`
function cls:_more_private()
    self._some_private_field = self._some_private_field .. "private"
end

---Compare two instances for equality.
---@param self Class
---@param other Class
---@return boolean
function cls.__eq(self, other)
    return self.some_public_field == other.some_public_field
end