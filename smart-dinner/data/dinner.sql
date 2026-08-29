-- 测试内容
# test
select count(*) as c from menu_items;

-- 查询所有可用的菜品信息
# get_menu_items
select id,
       dish_name,
       price,
       description,
       category,
       spice_level,
       flavor,
       main_ingredients,
       cooking_method,
       is_vegetarian,
       allergens,
       is_available
from menu_items
where is_available = 1
order by category, dish_name;
