-- Takes a list of sorted set keys and return the ones that exist
-- and are not empty; which semantically filters the indexed ones
-- from a list of tokens.
local candidates = {}
for i,k in ipairs(KEYS) do
    if redis.call('ZCARD', k) > 0 then
        candidates[#candidates + 1] = k
    end
end
return candidates
