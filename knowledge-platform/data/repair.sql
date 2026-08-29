-- 查询坐标
# get_repair
SELECT service_station_name,
       address,
       phone,
       latitude,
       longitude,
       (
           6371 * acos
           (
                cos(radians(%s)) *
                cos(radians(latitude)) *
                cos(radians(longitude) - radians(%s)) +
                sin(radians(%s)) *
                sin(radians(latitude))
            )
    ) AS distance_km
FROM repair_shops
WHERE
    latitude IS NOT NULL
    AND longitude IS NOT NULL
ORDER BY distance_km ASC
LIMIT %s;
