set names utf8mb4;
set FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for menu_items
-- ----------------------------
drop table if exists `menu_items`;
create table menu_items
(
    id               int                                                           not null AUTO_INCREMENT COMMENT '菜品ID，主键自增',
    dish_name        varchar(100) character set utf8mb4 collate utf8mb4_unicode_ci not null COMMENT '菜品名称',
    price            decimal(8, 2)                                                 not null COMMENT '价格（元）',
    description      text character set utf8mb4 collate utf8mb4_unicode_ci null COMMENT '菜品描述',
    category         varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci  not null COMMENT '菜品分类',
    spice_level      tinyint null default 0 COMMENT '辣度等级：0-不辣，1-微辣，2-中辣，3-重辣',
    flavor           varchar(100) character set utf8mb4 collate utf8mb4_unicode_ci null default null COMMENT '口味特点',
    main_ingredients text character set utf8mb4 collate utf8mb4_unicode_ci null COMMENT '主要食材，多个食材用逗号分隔',
    cooking_method   varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci null default null COMMENT '烹饪方法',
    is_vegetarian    tinyint(1) null default 0 COMMENT '是否素食：0-否，1-是',
    allergens        varchar(200) character set utf8mb4 collate utf8mb4_unicode_ci null default null COMMENT '过敏原信息，多个过敏原用逗号分隔',
    is_available     tinyint(1) null default 1 COMMENT '是否可供应：0-不可用，1-可用',
    created_at       timestamp null default current_timestamp COMMENT '创建时间',
    updated_at       timestamp null default current_timestamp on update current_timestamp COMMENT '更新时间',
    primary key (id) using BTREE,
    index            idx_category(`category`) using BTREE,
    index            idx_is_available(`is_available`) using BTREE,
    index            idx_is_vegetarian(`is_vegetarian`) using BTREE,
    index            idx_price(`price`) using BTREE,
    index            idx_spice_level(`spice_level`) using BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 character set = utf8mb4 collate = utf8mb4_unicode_ci COMMENT = '菜单表' ROW_FORMAT = dynamic;

-- ----------------------------
-- Records of menu_items
-- ----------------------------
insert into menu_items
values (1, '宫保鸡丁', 28.00, '经典川菜，鸡肉丁配花生米，酸甜微辣，口感丰富', '川菜', 2, '酸甜微辣',
        '鸡胸肉,花生米,青椒,红椒,葱段', '爆炒', 0, '花生,可能含有麸质', 1, '2025-07-01 10:45:02',
        '2025-07-01 10:45:02');
insert into menu_items
values (2, '麻婆豆腐', 18.00, '四川传统名菜，嫩滑豆腐配麻辣汤汁，下饭神器', '川菜', 3, '麻辣鲜香',
        '嫩豆腐,牛肉末,豆瓣酱,花椒', '烧炒', 0, '大豆,可能含有麸质', 1, '2025-07-01 10:45:02', '2025-09-26 14:43:58');
insert into menu_items
values (3, '清炒时蔬', 15.00, '新鲜时令蔬菜清炒，营养健康，口感清爽', '素食', 0, '清淡爽口', '时令蔬菜,蒜蓉', '清炒', 1,
        '', 1, '2025-07-01 10:45:02', '2025-09-26 14:53:33');
insert into menu_items
values (4, '红烧鲈鱼', 45.00, '新鲜鲈鱼红烧制作，肉质鲜美，营养丰富', '鲁菜', 1, '咸鲜微甜', '鲈鱼,生抽,老抽,冰糖,葱姜',
        '红烧', 0, '鱼类', 1, '2025-07-01 10:45:02', '2025-07-01 10:45:02');
insert into menu_items
values (5, '蒜蓉西兰花', 12.00, '新鲜西兰花配蒜蓉，营养丰富，适合减肥人群', '素食', 0, '蒜香清淡', '西兰花,大蒜,橄榄油',
        '蒸炒', 1, '无过敏源', 1, '2025-07-01 10:45:02', '2025-09-26 14:53:24');

-- ----------------------------
-- Table structure for order_items
-- ----------------------------
drop table if exists `order_items`;
create table order_items
(
    id         int                                                           not null AUTO_INCREMENT,
    order_id   int                                                           not null,
    dish_id    int                                                           not null,
    dish_name  varchar(200) character set utf8mb4 collate utf8mb4_general_ci not null,
    quantity   int                                                           not null,
    unit_price decimal(10, 2)                                                not null,
    subtotal   decimal(10, 2)                                                not null,
    primary key (id) using BTREE,
    index      dish_id(`dish_id`) using BTREE,
    index      order_id(`order_id`) using BTREE,
    constraint order_items_ibfk_1 foreign key (order_id) references orders (id) on delete cascade on update restrict,
    constraint order_items_ibfk_2 foreign key (dish_id) references menu_items (id) on delete restrict on update restrict
) ENGINE = InnoDB AUTO_INCREMENT = 13 character set = utf8mb4 collate = utf8mb4_general_ci ROW_FORMAT = dynamic;

-- ----------------------------
-- Records of order_items
-- ----------------------------
insert into order_items
values (1, 1, 2, '麻婆豆腐', 1, 18.00, 18.00);
insert into order_items
values (2, 2, 3, '清炒时蔬', 1, 15.00, 15.00);
insert into order_items
values (11, 6, 3, '清炒时蔬', 1, 15.00, 15.00);
insert into order_items
values (12, 7, 1, '宫保鸡丁', 1, 28.00, 28.00);
insert into order_items
values (13, 8, 1, '宫保鸡丁', 2, 28.00, 56.00);

-- ----------------------------
-- Table structure for orders
-- ----------------------------
drop table if exists `orders`;
create table orders
(
    id                int                                                           not null AUTO_INCREMENT,
    user_id           int                                                           not null,
    order_no          varchar(50) character set utf8mb4 collate utf8mb4_general_ci  not null,
    contact_name      varchar(100) character set utf8mb4 collate utf8mb4_general_ci not null,
    contact_phone     varchar(20) character set utf8mb4 collate utf8mb4_general_ci  not null,
    delivery_address  varchar(500) character set utf8mb4 collate utf8mb4_general_ci not null,
    total_amount      decimal(10, 2)                                                not null,
    total_quantity    int                                                           not null,
    status            tinyint                                                       not null default 0,
    delivery_distance decimal(8, 2) null default null,
    created_at        timestamp null default current_timestamp,
    updated_at        timestamp null default current_timestamp on update current_timestamp,
    primary key (id) using BTREE,
    unique index `order_no`(`order_no`) using BTREE,
    index             user_id(`user_id`) using BTREE,
    constraint orders_ibfk_1 foreign key (user_id) references users (id) on delete cascade on update restrict
) ENGINE = InnoDB AUTO_INCREMENT = 8 character set = utf8mb4 collate = utf8mb4_general_ci ROW_FORMAT = dynamic;

-- ----------------------------
-- Records of orders
-- ----------------------------
insert into orders
values (1, 2, '20250703105217285', '张三', '13812345678', '北京市海淀区中关村大街1号科技大厦A座1001室', 18.00, 1, 4,
        15.10, '2025-07-03 10:52:17', '2025-07-03 11:05:43');
insert into orders
values (2, 2, '20250703110344662', '尚硅谷', '13624017478', '北京市昌平区回龙观东大街', 15.00, 1, 0, 3.19,
        '2025-07-03 11:03:44', '2025-07-03 11:03:44');
insert into orders
values (6, 2, '20250703162549259', '123', '13423456789', '北京市昌平区温都水城', 15.00, 1, 0, 1.62,
        '2025-07-03 16:25:49', '2025-07-03 16:25:49');
insert into orders
values (7, 2, '20251016212342363', 'hzk', '18438592661', '北京市昌平区回龙观', 28.00, 1, 0, 7.19, '2025-10-16 21:23:42',
        '2025-10-16 21:23:42');
insert into orders
values (8, 2, '20251016214926730', 'test', '13812345678', '北京市昌平区回龙观', 56.00, 2, 0, 7.19,
        '2025-10-16 21:49:26', '2025-10-16 21:49:26');

-- ----------------------------
-- Table structure for shopping_cart
-- ----------------------------
drop table if exists `shopping_cart`;
create table shopping_cart
(
    id         int not null AUTO_INCREMENT,
    user_id    int not null,
    dish_id    int not null,
    quantity   int not null default 1,
    created_at timestamp null default current_timestamp,
    updated_at timestamp null default current_timestamp on update current_timestamp,
    primary key (id) using BTREE,
    unique index `unique_user_dish`(`user_id`, `dish_id`) using BTREE,
    index      dish_id(`dish_id`) using BTREE,
    constraint shopping_cart_ibfk_1 foreign key (user_id) references users (id) on delete cascade on update restrict,
    constraint shopping_cart_ibfk_2 foreign key (dish_id) references menu_items (id) on delete cascade on update restrict
) ENGINE = InnoDB AUTO_INCREMENT = 25 character set = utf8mb4 collate = utf8mb4_unicode_ci ROW_FORMAT = dynamic;

-- ----------------------------
-- Records of shopping_cart
-- ----------------------------
insert into shopping_cart
values (19, 5, 1, 4, '2025-07-03 16:01:29', '2025-07-03 16:10:40');
insert into shopping_cart
values (20, 5, 2, 3, '2025-07-03 16:01:48', '2025-07-03 16:02:13');
insert into shopping_cart
values (21, 5, 3, 2, '2025-07-03 16:01:50', '2025-07-03 16:01:50');
insert into shopping_cart
values (22, 5, 4, 1, '2025-07-03 16:02:10', '2025-07-03 16:02:10');
insert into shopping_cart
values (23, 5, 5, 1, '2025-07-03 16:02:15', '2025-07-03 16:02:15');

-- ----------------------------
-- Table structure for users
-- ----------------------------
drop table if exists `users`;
create table users
(
    id         int                                                           not null AUTO_INCREMENT,
    username   varchar(50) character set utf8mb4 collate utf8mb4_unicode_ci  not null,
    password   varchar(255) character set utf8mb4 collate utf8mb4_unicode_ci not null,
    email      varchar(100) character set utf8mb4 collate utf8mb4_unicode_ci null default null,
    phone      varchar(20) character set utf8mb4 collate utf8mb4_unicode_ci null default null,
    created_at timestamp null default current_timestamp,
    last_login timestamp null default null,
    is_active  tinyint(1) null default 1,
    primary key (id) using BTREE,
    unique index `username`(`username`) using BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 character set = utf8mb4 collate = utf8mb4_unicode_ci ROW_FORMAT = dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
insert into users
values (1, 'admin', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'admin@example.com', null,
        '2025-07-02 09:46:39', null, 1);
insert into users
values (2, 'test', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'test@example.com',
        '13812345678', '2025-07-02 09:46:39', '2025-10-16 21:21:16', 1);
insert into users
values (3, 'testuser1', '85777f270ad7cf2a790981bbae3c4e484a1dc55e24a77390d692fbf1cffa12fa', 'testuser1@example.com',
        '13800138000', '2025-07-02 10:10:31', '2025-07-03 09:17:04', 1);
insert into users
values (4, 'test2', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', '123@qq.com', '13624007576',
        '2025-07-02 13:54:00', '2025-07-02 13:54:06', 1);
insert into users
values (5, 'testuser', '7e6e0c3079a08c5cc6036789b57e951f65f82383913ba1a49ae992544f1b4b6e', 'test@example.com',
        '13812345678', '2025-07-03 15:45:35', '2025-07-03 15:52:29', 1);

set FOREIGN_KEY_CHECKS = 1;
