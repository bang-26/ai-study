-- 创建数据库 gmail
create database if not exists gmail default charset utf8mb4 collate utf8mb4_general_ci;

# 将 gmail 数据库授权给 test
-- grant all privileges on gmail.* to 'study'@'%';
-- flush privileges;

use gmail;

-- ----------------------------
-- Table structure for activity_info
-- ----------------------------
drop table if exists activity_info;
create table if not exists activity_info
(
    id            bigint not null auto_increment comment '活动id',
    activity_name varchar(200) comment '活动名称',
    activity_type varchar(10) comment '活动类型（1：满减，2：折扣）',
    activity_desc varchar(2000) comment '活动描述',
    start_time    datetime comment '开始时间',
    end_time      datetime comment '结束时间',
    create_time   datetime comment '创建时间',
    operate_time  datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 4
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '活动表'
  row_format = dynamic;

-- ----------------------------
-- Records of activity_info
-- ----------------------------
insert into activity_info
values (1, '小米手机专场', '3101', '小米手机满减2', '2022-01-13 01:01:54', '2023-06-19 00:00:00', '2022-05-27 00:00:00',
        null);
insert into activity_info
values (2, 'CAREMiLLE口红满两个8折', '3102', 'CAREMiLLE口红满两个8折', '2022-01-13 01:01:54', '2023-06-19 00:00:00',
        '2022-05-27 00:00:00', null);
insert into activity_info
values (3, '联想活动专场满减', '3101', '联想活动专场满减', '2022-01-13 01:01:54', '2023-06-19 00:00:00',
        '2022-05-27 00:00:00', null);
insert into activity_info
values (4, 'TCL全场9折', '3103', 'TCL全场9折', '2022-01-13 01:01:54', '2023-06-19 00:00:00', '2022-05-27 00:00:00',
        null);

-- ----------------------------
-- Table structure for activity_rule
-- ----------------------------
drop table if exists activity_rule;
create table if not exists activity_rule
(
    id               int not null auto_increment comment '编号',
    activity_id      int comment '活动id',
    activity_type    varchar(20) comment '活动类型',
    condition_amount decimal(16, 2) comment '满减金额',
    condition_num    bigint comment '满减件数',
    benefit_amount   decimal(16, 2) comment '优惠金额',
    benefit_discount decimal(10, 2) comment '优惠折扣',
    benefit_level    bigint comment '优惠级别',
    create_time      datetime comment '创建时间',
    operate_time     datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 5
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '活动规则表'
  row_format = dynamic;

-- ----------------------------
-- Records of activity_rule
-- ----------------------------
insert into activity_rule
values (1, 1, '3101', 5000.00, null, 500.00, null, 1, '2022-02-13 01:08:32', null);
insert into activity_rule
values (2, 1, '3101', 8000.00, null, 900.00, null, 2, '2022-02-13 01:08:32', null);
insert into activity_rule
values (3, 2, '3102', null, 2, null, 8.50, 1, '2022-02-13 01:08:32', null);
insert into activity_rule
values (4, 3, '3101', 5000.00, null, 250.00, null, 1, '2022-02-13 01:08:32', null);
insert into activity_rule
values (5, 4, '3103', null, null, null, 9.00, 1, '2022-02-13 01:08:32', null);

-- ----------------------------
-- Table structure for activity_sku
-- ----------------------------
drop table if exists activity_sku;
create table if not exists activity_sku
(
    id           bigint not null auto_increment comment '编号',
    activity_id  bigint comment '活动id ',
    sku_id       bigint comment 'sku_id',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 13
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '活动商品关联表'
  row_format = dynamic;

-- ----------------------------
-- Records of activity_sku
-- ----------------------------
insert into activity_sku
values (1, 1, 1, '2021-12-14 00:00:00', null);
insert into activity_sku
values (2, 1, 2, '2021-12-14 00:00:00', null);
insert into activity_sku
values (3, 1, 3, '2021-12-14 00:00:00', null);
insert into activity_sku
values (4, 2, 26, '2021-12-14 00:00:00', null);
insert into activity_sku
values (5, 2, 27, '2021-12-14 00:00:00', null);
insert into activity_sku
values (6, 2, 28, '2021-12-14 00:00:00', null);
insert into activity_sku
values (7, 3, 13, '2021-12-14 00:00:00', null);
insert into activity_sku
values (8, 3, 14, '2021-12-14 00:00:00', null);
insert into activity_sku
values (9, 3, 15, '2021-12-14 00:00:00', null);
insert into activity_sku
values (10, 3, 16, '2021-12-14 00:00:00', null);
insert into activity_sku
values (11, 4, 17, '2021-12-14 00:00:00', null);
insert into activity_sku
values (12, 4, 18, '2021-12-14 00:00:00', null);
insert into activity_sku
values (13, 4, 19, '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for base_attr_info
-- ----------------------------
drop table if exists base_attr_info;
create table if not exists base_attr_info
(
    id             bigint       not null auto_increment comment '编号',
    attr_name      varchar(100) not null comment '属性名称',
    category_id    bigint comment '分类id',
    category_level int comment '分类层级',
    create_time    datetime comment '创建时间',
    operate_time   datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 114
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '属性表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_attr_info
-- ----------------------------
insert into base_attr_info
values (23, '运行内存', 61, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (24, '机身内存', 61, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (25, '处理器', 287, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (26, '显卡', 287, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (37, '分类', 1, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (45, '产地', 371, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (46, '运行内存', 63, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (65, '品牌', 65, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (66, '硬盘', 287, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (67, '内存', 287, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (73, '像素', 178, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (74, '传感器尺寸', 178, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (76, '镜头', 178, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (81, '机身内存', 63, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (83, '价格', 100, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (84, '价格', 100, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (85, '价格3', 100, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (86, '价格', 102, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (87, '价格', 841, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (89, '电视类型', 86, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (90, '价格', 930, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (91, '价格', 598, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (92, '价格', 598, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (93, '价格', 598, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (94, '价格', 598, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (95, '价格', 997, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (96, '屏幕尺寸', 86, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (97, '分辨率', 86, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (98, '观看距离', 86, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (99, '画幅', 180, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (103, '面料', 233, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (105, '品牌', 62, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (106, '手机一级', 2, 1, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (107, '二级手机', 13, 2, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (108, '粮食调味', 803, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (109, '是否有机', 803, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (110, '分类', 803, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (111, '功效', 477, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (112, '香水彩妆', 477, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (113, '面部护肤', 477, 3, '2021-12-14 00:00:00', null);
insert into base_attr_info
values (114, '香调', 473, 3, '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for base_attr_value
-- ----------------------------
drop table if exists base_attr_value;
create table if not exists base_attr_value
(
    id           bigint       not null auto_increment comment '编号',
    value_name   varchar(100) not null comment '属性值名称',
    attr_id      bigint comment '属性id',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 218
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '属性值表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_attr_value
-- ----------------------------
insert into base_attr_value
values (1, '红色', 18, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (2, '白色', 18, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (3, '红色', 19, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (4, '白色', 19, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (5, '华为', 20, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (6, '联想', 20, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (7, 'X5', 21, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (8, 'X6', 21, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (9, 'X7', 21, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (10, '3.0', 22, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (11, '4.0', 22, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (12, '5.0', 22, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (13, '3G', 23, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (14, '4G', 23, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (19, 'i7', 25, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (20, 'i9', 25, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (21, 'RTX3070Ti', 26, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (22, 'RTX30760', 26, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (35, '123123', 38, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (36, '222222', 38, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (37, '红色', 39, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (38, '白色', 39, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (39, '红色', 40, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (40, '白色', 40, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (41, '南非', 41, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (64, '16G', 46, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (69, '10', 57, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (71, '10', 59, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (72, '10', 60, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (73, '10', 61, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (78, '国内', 65, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (79, '南非', 65, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (83, '8G', 23, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (84, '512GB', 66, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (85, '512GB+2T', 66, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (86, '16G', 67, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (87, '32G', 67, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (89, '3434', 68, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (90, '5.0', 69, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (91, '5.6', 69, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (93, '国内', 70, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (94, '国外', 70, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (95, '国内', 71, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (96, '国外', 71, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (97, '100W', 72, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (99, '2000万', 73, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (100, '3000万', 73, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (101, '1英寸', 74, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (102, '2.3英寸', 74, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (115, '1000G', 81, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (120, '12G', 23, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (121, '5.5', 82, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (122, '6.5', 82, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (123, '123', 83, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (124, '123', 85, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (125, '123', 84, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (126, '234', 83, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (128, '234', 84, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (129, '2000', 86, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (130, '4000', 86, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (132, '2000', 87, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (133, '88888', 87, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (135, '200', 88, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (136, '4K超清', 89, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (139, '2000', 90, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (140, '2000', 91, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (141, '3000', 91, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (143, '400', 95, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (144, '70-75', 96, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (145, '75以上', 96, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (146, '8K超高清', 97, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (147, '4K超高清', 97, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (148, '12K超高清', 97, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (149, '3.5m', 98, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (150, '3m', 98, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (151, 'APS-C画幅全画', 99, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (152, '全画幅', 99, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (162, '棉', 103, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (163, '麻', 103, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (164, '200W', 72, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (165, '2000', 88, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (169, '6G', 23, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (170, '128G', 23, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (171, '256G', 23, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (172, '国内', 105, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (174, '国外', 105, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (175, '苹果手机', 106, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (176, '安卓手机', 106, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (177, '小米', 107, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (178, '华为', 107, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (179, '苹果', 107, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (180, '32G', 24, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (181, '64G', 24, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (182, '128G', 24, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (183, '256G', 24, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (184, '512G', 24, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (185, '1T', 24, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (187, 'Java', 37, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (188, 'C#', 37, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (189, 'JavaScript', 37, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (190, 'rtrt', 37, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (191, '曲面', 89, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (192, '超薄', 89, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (193, '人工智能', 89, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (194, '60以下', 96, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (195, '60-70', 96, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (196, '杂粮', 108, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (197, '大米', 108, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (198, '面食', 108, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (199, '调味品', 108, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (200, '有机食品', 109, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (201, '非有机食品', 109, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (202, '杂粮组合', 110, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (203, '米', 110, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (204, '面', 110, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (205, '黑米', 110, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (206, '滋润', 111, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (207, '保湿', 111, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (208, '防水', 111, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (209, '防晒', 111, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (210, '口红', 112, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (211, '香水', 112, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (212, '润唇膏', 113, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (213, '乳液/面霜', 113, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (214, '面部精华', 113, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (215, '花果香调', 114, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (216, '海洋香调', 114, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (217, '古龙香调', 114, '2021-12-14 00:00:00', null);
insert into base_attr_value
values (218, '花香调', 114, '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for base_category1
-- ----------------------------
drop table if exists base_category1;
create table if not exists base_category1
(
    id           bigint      not null auto_increment comment '一级品类id',
    name         varchar(10) not null comment '一级品类名称',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 17
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '一级品类表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_category1
-- ----------------------------
insert into base_category1
values (1, '图书、音像、电子书刊', '2021-12-14 00:00:00', null);
insert into base_category1
values (2, '手机', '2021-12-14 00:00:00', null);
insert into base_category1
values (3, '家用电器', '2021-12-14 00:00:00', null);
insert into base_category1
values (4, '数码', '2021-12-14 00:00:00', null);
insert into base_category1
values (5, '家居家装', '2021-12-14 00:00:00', null);
insert into base_category1
values (6, '电脑办公', '2021-12-14 00:00:00', null);
insert into base_category1
values (7, '厨具', '2021-12-14 00:00:00', null);
insert into base_category1
values (8, '个护化妆', '2021-12-14 00:00:00', null);
insert into base_category1
values (9, '服饰内衣', '2021-12-14 00:00:00', null);
insert into base_category1
values (10, '钟表', '2021-12-14 00:00:00', null);
insert into base_category1
values (11, '鞋靴', '2021-12-14 00:00:00', null);
insert into base_category1
values (12, '母婴', '2021-12-14 00:00:00', null);
insert into base_category1
values (13, '礼品箱包', '2021-12-14 00:00:00', null);
insert into base_category1
values (14, '食品饮料、保健食品', '2021-12-14 00:00:00', null);
insert into base_category1
values (15, '珠宝', '2021-12-14 00:00:00', null);
insert into base_category1
values (16, '汽车用品', '2021-12-14 00:00:00', null);
insert into base_category1
values (17, '运动健康', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for base_category2
-- ----------------------------
drop table if exists base_category2;
create table if not exists base_category2
(
    id           bigint       not null auto_increment comment '二级品类id',
    name         varchar(200) not null comment '二级品类名称',
    category1_id bigint comment '一级品类编号',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 113
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '二级品类表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_category2
-- ----------------------------
insert into base_category2
values (1, '电子书刊', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (2, '音像', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (3, '英文原版', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (4, '文艺', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (5, '少儿', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (6, '人文社科', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (7, '经管励志', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (8, '生活', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (9, '科技', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (10, '教育', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (11, '港台图书', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (12, '其他', 1, '2021-12-14 00:00:00', null);
insert into base_category2
values (13, '手机通讯', 2, '2021-12-14 00:00:00', null);
insert into base_category2
values (14, '运营商', 2, '2021-12-14 00:00:00', null);
insert into base_category2
values (15, '手机配件', 2, '2021-12-14 00:00:00', null);
insert into base_category2
values (16, '大 家 电', 3, '2021-12-14 00:00:00', null);
insert into base_category2
values (17, '厨卫大电', 3, '2021-12-14 00:00:00', null);
insert into base_category2
values (18, '厨房小电', 3, '2021-12-14 00:00:00', null);
insert into base_category2
values (19, '生活电器', 3, '2021-12-14 00:00:00', null);
insert into base_category2
values (20, '个护健康', 3, '2021-12-14 00:00:00', null);
insert into base_category2
values (21, '五金家装', 3, '2021-12-14 00:00:00', null);
insert into base_category2
values (22, '摄影摄像', 4, '2021-12-14 00:00:00', null);
insert into base_category2
values (23, '数码配件', 4, '2021-12-14 00:00:00', null);
insert into base_category2
values (24, '智能设备', 4, '2021-12-14 00:00:00', null);
insert into base_category2
values (25, '影音娱乐', 4, '2021-12-14 00:00:00', null);
insert into base_category2
values (26, '电子教育', 4, '2021-12-14 00:00:00', null);
insert into base_category2
values (27, '虚拟商品', 4, '2021-12-14 00:00:00', null);
insert into base_category2
values (28, '家纺', 5, '2021-12-14 00:00:00', null);
insert into base_category2
values (29, '灯具', 5, '2021-12-14 00:00:00', null);
insert into base_category2
values (30, '生活日用', 5, '2021-12-14 00:00:00', null);
insert into base_category2
values (31, '家装软饰', 5, '2021-12-14 00:00:00', null);
insert into base_category2
values (32, '宠物生活', 5, '2021-12-14 00:00:00', null);
insert into base_category2
values (33, '电脑整机', 6, '2021-12-14 00:00:00', null);
insert into base_category2
values (34, '电脑配件', 6, '2021-12-14 00:00:00', null);
insert into base_category2
values (35, '外设产品', 6, '2021-12-14 00:00:00', null);
insert into base_category2
values (36, '游戏设备', 6, '2021-12-14 00:00:00', null);
insert into base_category2
values (37, '网络产品', 6, '2021-12-14 00:00:00', null);
insert into base_category2
values (38, '办公设备', 6, '2021-12-14 00:00:00', null);
insert into base_category2
values (39, '文具/耗材', 6, '2021-12-14 00:00:00', null);
insert into base_category2
values (40, '服务产品', 6, '2021-12-14 00:00:00', null);
insert into base_category2
values (41, '烹饪锅具', 7, '2021-12-14 00:00:00', null);
insert into base_category2
values (42, '刀剪菜板', 7, '2021-12-14 00:00:00', null);
insert into base_category2
values (43, '厨房配件', 7, '2021-12-14 00:00:00', null);
insert into base_category2
values (44, '水具酒具', 7, '2021-12-14 00:00:00', null);
insert into base_category2
values (45, '餐具', 7, '2021-12-14 00:00:00', null);
insert into base_category2
values (46, '酒店用品', 7, '2021-12-14 00:00:00', null);
insert into base_category2
values (47, '茶具/咖啡具', 7, '2021-12-14 00:00:00', null);
insert into base_category2
values (48, '清洁用品', 8, '2021-12-14 00:00:00', null);
insert into base_category2
values (49, '面部护肤', 8, '2021-12-14 00:00:00', null);
insert into base_category2
values (50, '身体护理', 8, '2021-12-14 00:00:00', null);
insert into base_category2
values (51, '口腔护理', 8, '2021-12-14 00:00:00', null);
insert into base_category2
values (52, '女性护理', 8, '2021-12-14 00:00:00', null);
insert into base_category2
values (53, '洗发护发', 8, '2021-12-14 00:00:00', null);
insert into base_category2
values (54, '香水彩妆', 8, '2021-12-14 00:00:00', null);
insert into base_category2
values (55, '女装', 9, '2021-12-14 00:00:00', null);
insert into base_category2
values (56, '男装', 9, '2021-12-14 00:00:00', null);
insert into base_category2
values (57, '内衣', 9, '2021-12-14 00:00:00', null);
insert into base_category2
values (58, '洗衣服务', 9, '2021-12-14 00:00:00', null);
insert into base_category2
values (59, '服饰配件', 9, '2021-12-14 00:00:00', null);
insert into base_category2
values (60, '钟表', 10, '2021-12-14 00:00:00', null);
insert into base_category2
values (61, '流行男鞋', 11, '2021-12-14 00:00:00', null);
insert into base_category2
values (62, '时尚女鞋', 11, '2021-12-14 00:00:00', null);
insert into base_category2
values (63, '奶粉', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (64, '营养辅食', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (65, '尿裤湿巾', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (66, '喂养用品', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (67, '洗护用品', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (68, '童车童床', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (69, '寝居服饰', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (70, '妈妈专区', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (71, '童装童鞋', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (72, '安全座椅', 12, '2021-12-14 00:00:00', null);
insert into base_category2
values (73, '潮流女包', 13, '2021-12-14 00:00:00', null);
insert into base_category2
values (74, '精品男包', 13, '2021-12-14 00:00:00', null);
insert into base_category2
values (75, '功能箱包', 13, '2021-12-14 00:00:00', null);
insert into base_category2
values (76, '礼品', 13, '2021-12-14 00:00:00', null);
insert into base_category2
values (77, '奢侈品', 13, '2021-12-14 00:00:00', null);
insert into base_category2
values (78, '婚庆', 13, '2021-12-14 00:00:00', null);
insert into base_category2
values (79, '进口食品', 14, '2021-12-14 00:00:00', null);
insert into base_category2
values (80, '地方特产', 14, '2021-12-14 00:00:00', null);
insert into base_category2
values (81, '休闲食品', 14, '2021-12-14 00:00:00', null);
insert into base_category2
values (82, '粮油调味', 14, '2021-12-14 00:00:00', null);
insert into base_category2
values (83, '饮料冲调', 14, '2021-12-14 00:00:00', null);
insert into base_category2
values (84, '食品礼券', 14, '2021-12-14 00:00:00', null);
insert into base_category2
values (85, '茗茶', 14, '2021-12-14 00:00:00', null);
insert into base_category2
values (86, '时尚饰品', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (87, '黄金', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (88, 'K金饰品', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (89, '金银投资', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (90, '银饰', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (91, '钻石', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (92, '翡翠玉石', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (93, '水晶玛瑙', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (94, '彩宝', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (95, '铂金', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (96, '木手串/把件', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (97, '珍珠', 15, '2021-12-14 00:00:00', null);
insert into base_category2
values (98, '维修保养', 16, '2021-12-14 00:00:00', null);
insert into base_category2
values (99, '车载电器', 16, '2021-12-14 00:00:00', null);
insert into base_category2
values (100, '美容清洗', 16, '2021-12-14 00:00:00', null);
insert into base_category2
values (101, '汽车装饰', 16, '2021-12-14 00:00:00', null);
insert into base_category2
values (102, '安全自驾', 16, '2021-12-14 00:00:00', null);
insert into base_category2
values (103, '汽车服务', 16, '2021-12-14 00:00:00', null);
insert into base_category2
values (104, '赛事改装', 16, '2021-12-14 00:00:00', null);
insert into base_category2
values (105, '运动鞋包', 17, '2021-12-14 00:00:00', null);
insert into base_category2
values (106, '运动服饰', 17, '2021-12-14 00:00:00', null);
insert into base_category2
values (107, '骑行运动', 17, '2021-12-14 00:00:00', null);
insert into base_category2
values (108, '垂钓用品', 17, '2021-12-14 00:00:00', null);
insert into base_category2
values (109, '游泳用品', 17, '2021-12-14 00:00:00', null);
insert into base_category2
values (110, '户外鞋服', 17, '2021-12-14 00:00:00', null);
insert into base_category2
values (111, '户外装备', 17, '2021-12-14 00:00:00', null);
insert into base_category2
values (112, '健身训练', 17, '2021-12-14 00:00:00', null);
insert into base_category2
values (113, '体育用品', 17, '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for base_category3
-- ----------------------------
drop table if exists base_category3;
create table if not exists base_category3
(
    id           bigint       not null auto_increment comment '三级品类id',
    name         varchar(200) not null comment '三级品类名称',
    category2_id bigint comment '二级品类编号',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 1099
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '三级品类表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_category3
-- ----------------------------
insert into base_category3
values (1, '电子书', 1, '2021-12-14 00:00:00', null);
insert into base_category3
values (2, '网络原创', 1, '2021-12-14 00:00:00', null);
insert into base_category3
values (3, '数字杂志', 1, '2021-12-14 00:00:00', null);
insert into base_category3
values (4, '多媒体图书', 1, '2021-12-14 00:00:00', null);
insert into base_category3
values (5, '音乐', 2, '2021-12-14 00:00:00', null);
insert into base_category3
values (6, '影视', 2, '2021-12-14 00:00:00', null);
insert into base_category3
values (7, '教育音像', 2, '2021-12-14 00:00:00', null);
insert into base_category3
values (8, '少儿', 3, '2021-12-14 00:00:00', null);
insert into base_category3
values (9, '商务投资', 3, '2021-12-14 00:00:00', null);
insert into base_category3
values (10, '英语学习与考试', 3, '2021-12-14 00:00:00', null);
insert into base_category3
values (11, '文学', 3, '2021-12-14 00:00:00', null);
insert into base_category3
values (12, '传记', 3, '2021-12-14 00:00:00', null);
insert into base_category3
values (13, '励志', 3, '2021-12-14 00:00:00', null);
insert into base_category3
values (14, '小说', 4, '2021-12-14 00:00:00', null);
insert into base_category3
values (15, '文学', 4, '2021-12-14 00:00:00', null);
insert into base_category3
values (16, '青春文学', 4, '2021-12-14 00:00:00', null);
insert into base_category3
values (17, '传记', 4, '2021-12-14 00:00:00', null);
insert into base_category3
values (18, '艺术', 4, '2021-12-14 00:00:00', null);
insert into base_category3
values (19, '少儿', 5, '2021-12-14 00:00:00', null);
insert into base_category3
values (20, '0-2岁', 5, '2021-12-14 00:00:00', null);
insert into base_category3
values (21, '3-6岁', 5, '2021-12-14 00:00:00', null);
insert into base_category3
values (22, '7-10岁', 5, '2021-12-14 00:00:00', null);
insert into base_category3
values (23, '11-14岁', 5, '2021-12-14 00:00:00', null);
insert into base_category3
values (24, '历史', 6, '2021-12-14 00:00:00', null);
insert into base_category3
values (25, '哲学', 6, '2021-12-14 00:00:00', null);
insert into base_category3
values (26, '国学', 6, '2021-12-14 00:00:00', null);
insert into base_category3
values (27, '政治/军事', 6, '2021-12-14 00:00:00', null);
insert into base_category3
values (28, '法律', 6, '2021-12-14 00:00:00', null);
insert into base_category3
values (29, '人文社科', 6, '2021-12-14 00:00:00', null);
insert into base_category3
values (30, '心理学', 6, '2021-12-14 00:00:00', null);
insert into base_category3
values (31, '文化', 6, '2021-12-14 00:00:00', null);
insert into base_category3
values (32, '社会科学', 6, '2021-12-14 00:00:00', null);
insert into base_category3
values (33, '经济', 7, '2021-12-14 00:00:00', null);
insert into base_category3
values (34, '金融与投资', 7, '2021-12-14 00:00:00', null);
insert into base_category3
values (35, '管理', 7, '2021-12-14 00:00:00', null);
insert into base_category3
values (36, '励志与成功', 7, '2021-12-14 00:00:00', null);
insert into base_category3
values (37, '生活', 8, '2021-12-14 00:00:00', null);
insert into base_category3
values (38, '健身与保健', 8, '2021-12-14 00:00:00', null);
insert into base_category3
values (39, '家庭与育儿', 8, '2021-12-14 00:00:00', null);
insert into base_category3
values (40, '旅游', 8, '2021-12-14 00:00:00', null);
insert into base_category3
values (41, '烹饪美食', 8, '2021-12-14 00:00:00', null);
insert into base_category3
values (42, '工业技术', 9, '2021-12-14 00:00:00', null);
insert into base_category3
values (43, '科普读物', 9, '2021-12-14 00:00:00', null);
insert into base_category3
values (44, '建筑', 9, '2021-12-14 00:00:00', null);
insert into base_category3
values (45, '医学', 9, '2021-12-14 00:00:00', null);
insert into base_category3
values (46, '科学与自然', 9, '2021-12-14 00:00:00', null);
insert into base_category3
values (47, '计算机与互联网', 9, '2021-12-14 00:00:00', null);
insert into base_category3
values (48, '电子通信', 9, '2021-12-14 00:00:00', null);
insert into base_category3
values (49, '中小学教辅', 10, '2021-12-14 00:00:00', null);
insert into base_category3
values (50, '教育与考试', 10, '2021-12-14 00:00:00', null);
insert into base_category3
values (51, '外语学习', 10, '2021-12-14 00:00:00', null);
insert into base_category3
values (52, '大中专教材', 10, '2021-12-14 00:00:00', null);
insert into base_category3
values (53, '字典词典', 10, '2021-12-14 00:00:00', null);
insert into base_category3
values (54, '艺术/设计/收藏', 11, '2021-12-14 00:00:00', null);
insert into base_category3
values (55, '经济管理', 11, '2021-12-14 00:00:00', null);
insert into base_category3
values (56, '文化/学术', 11, '2021-12-14 00:00:00', null);
insert into base_category3
values (57, '少儿', 11, '2021-12-14 00:00:00', null);
insert into base_category3
values (58, '工具书', 12, '2021-12-14 00:00:00', null);
insert into base_category3
values (59, '杂志/期刊', 12, '2021-12-14 00:00:00', null);
insert into base_category3
values (60, '套装书', 12, '2021-12-14 00:00:00', null);
insert into base_category3
values (61, '手机', 13, '2021-12-14 00:00:00', null);
insert into base_category3
values (62, '对讲机', 13, '2021-12-14 00:00:00', null);
insert into base_category3
values (63, '合约机', 14, '2021-12-14 00:00:00', null);
insert into base_category3
values (64, '选号中心', 14, '2021-12-14 00:00:00', null);
insert into base_category3
values (65, '装宽带', 14, '2021-12-14 00:00:00', null);
insert into base_category3
values (66, '办套餐', 14, '2021-12-14 00:00:00', null);
insert into base_category3
values (67, '移动电源', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (68, '电池/移动电源', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (69, '蓝牙耳机', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (70, '充电器/数据线', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (71, '苹果周边', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (72, '手机耳机', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (73, '手机贴膜', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (74, '手机存储卡', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (75, '充电器', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (76, '数据线', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (77, '手机保护套', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (78, '车载配件', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (79, 'iPhone 配件', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (80, '手机电池', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (81, '创意配件', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (82, '便携/无线音响', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (83, '手机饰品', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (84, '拍照配件', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (85, '手机支架', 15, '2021-12-14 00:00:00', null);
insert into base_category3
values (86, '平板电视', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (87, '空调', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (88, '冰箱', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (89, '洗衣机', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (90, '家庭影院', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (91, 'DVD/电视盒子', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (92, '迷你音响', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (93, '冷柜/冰吧', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (94, '家电配件', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (95, '功放', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (96, '回音壁/Soundbar', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (97, 'Hi-Fi专区', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (98, '电视盒子', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (99, '酒柜', 16, '2021-12-14 00:00:00', null);
insert into base_category3
values (100, '燃气灶', 17, '2021-12-14 00:00:00', null);
insert into base_category3
values (101, '油烟机', 17, '2021-12-14 00:00:00', null);
insert into base_category3
values (102, '热水器', 17, '2021-12-14 00:00:00', null);
insert into base_category3
values (103, '消毒柜', 17, '2021-12-14 00:00:00', null);
insert into base_category3
values (104, '洗碗机', 17, '2021-12-14 00:00:00', null);
insert into base_category3
values (105, '料理机', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (106, '榨汁机', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (107, '电饭煲', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (108, '电压力锅', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (109, '豆浆机', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (110, '咖啡机', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (111, '微波炉', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (112, '电烤箱', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (113, '电磁炉', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (114, '面包机', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (115, '煮蛋器', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (116, '酸奶机', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (117, '电炖锅', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (118, '电水壶/热水瓶', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (119, '电饼铛', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (120, '多用途锅', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (121, '电烧烤炉', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (122, '果蔬解毒机', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (123, '其它厨房电器', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (124, '养生壶/煎药壶', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (125, '电热饭盒', 18, '2021-12-14 00:00:00', null);
insert into base_category3
values (126, '取暖电器', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (127, '净化器', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (128, '加湿器', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (129, '扫地机器人', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (130, '吸尘器', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (131, '挂烫机/熨斗', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (132, '插座', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (133, '电话机', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (134, '清洁机', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (135, '除湿机', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (136, '干衣机', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (137, '收录/音机', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (138, '电风扇', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (139, '冷风扇', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (140, '其它生活电器', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (141, '生活电器配件', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (142, '净水器', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (143, '饮水机', 19, '2021-12-14 00:00:00', null);
insert into base_category3
values (144, '剃须刀', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (145, '剃/脱毛器', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (146, '口腔护理', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (147, '电吹风', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (148, '美容器', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (149, '理发器', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (150, '卷/直发器', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (151, '按摩椅', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (152, '按摩器', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (153, '足浴盆', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (154, '血压计', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (155, '电子秤/厨房秤', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (156, '血糖仪', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (157, '体温计', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (158, '其它健康电器', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (159, '计步器/脂肪检测仪', 20, '2021-12-14 00:00:00', null);
insert into base_category3
values (160, '电动工具', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (161, '手动工具', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (162, '仪器仪表', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (163, '浴霸/排气扇', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (164, '灯具', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (165, 'LED灯', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (166, '洁身器', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (167, '水槽', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (168, '龙头', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (169, '淋浴花洒', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (170, '厨卫五金', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (171, '家具五金', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (172, '门铃', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (173, '电气开关', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (174, '插座', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (175, '电工电料', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (176, '监控安防', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (177, '电线/线缆', 21, '2021-12-14 00:00:00', null);
insert into base_category3
values (178, '数码相机', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (179, '单电/微单相机', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (180, '单反相机', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (181, '摄像机', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (182, '拍立得', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (183, '运动相机', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (184, '镜头', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (185, '户外器材', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (186, '影棚器材', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (187, '冲印服务', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (188, '数码相框', 22, '2021-12-14 00:00:00', null);
insert into base_category3
values (189, '存储卡', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (190, '读卡器', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (191, '滤镜', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (192, '闪光灯/手柄', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (193, '相机包', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (194, '三脚架/云台', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (195, '相机清洁/贴膜', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (196, '机身附件', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (197, '镜头附件', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (198, '电池/充电器', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (199, '移动电源', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (200, '数码支架', 23, '2021-12-14 00:00:00', null);
insert into base_category3
values (201, '智能手环', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (202, '智能手表', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (203, '智能眼镜', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (204, '运动跟踪器', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (205, '健康监测', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (206, '智能配饰', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (207, '智能家居', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (208, '体感车', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (209, '其他配件', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (210, '智能机器人', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (211, '无人机', 24, '2021-12-14 00:00:00', null);
insert into base_category3
values (212, 'MP3/MP4', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (213, '智能设备', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (214, '耳机/耳麦', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (215, '便携/无线音箱', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (216, '音箱/音响', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (217, '高清播放器', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (218, '收音机', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (219, 'MP3/MP4配件', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (220, '麦克风', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (221, '专业音频', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (222, '苹果配件', 25, '2021-12-14 00:00:00', null);
insert into base_category3
values (223, '学生平板', 26, '2021-12-14 00:00:00', null);
insert into base_category3
values (224, '点读机/笔', 26, '2021-12-14 00:00:00', null);
insert into base_category3
values (225, '早教益智', 26, '2021-12-14 00:00:00', null);
insert into base_category3
values (226, '录音笔', 26, '2021-12-14 00:00:00', null);
insert into base_category3
values (227, '电纸书', 26, '2021-12-14 00:00:00', null);
insert into base_category3
values (228, '电子词典', 26, '2021-12-14 00:00:00', null);
insert into base_category3
values (229, '复读机', 26, '2021-12-14 00:00:00', null);
insert into base_category3
values (230, '延保服务', 27, '2021-12-14 00:00:00', null);
insert into base_category3
values (231, '杀毒软件', 27, '2021-12-14 00:00:00', null);
insert into base_category3
values (232, '积分商品', 27, '2021-12-14 00:00:00', null);
insert into base_category3
values (233, '桌布/罩件', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (234, '地毯地垫', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (235, '沙发垫套/椅垫', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (236, '床品套件', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (237, '被子', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (238, '枕芯', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (239, '床单被罩', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (240, '毯子', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (241, '床垫/床褥', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (242, '蚊帐', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (243, '抱枕靠垫', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (244, '毛巾浴巾', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (245, '电热毯', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (246, '窗帘/窗纱', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (247, '布艺软饰', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (248, '凉席', 28, '2021-12-14 00:00:00', null);
insert into base_category3
values (249, '台灯', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (250, '节能灯', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (251, '装饰灯', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (252, '落地灯', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (253, '应急灯/手电', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (254, 'LED灯', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (255, '吸顶灯', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (256, '五金电器', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (257, '筒灯射灯', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (258, '吊灯', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (259, '氛围照明', 29, '2021-12-14 00:00:00', null);
insert into base_category3
values (260, '保暖防护', 30, '2021-12-14 00:00:00', null);
insert into base_category3
values (261, '收纳用品', 30, '2021-12-14 00:00:00', null);
insert into base_category3
values (262, '雨伞雨具', 30, '2021-12-14 00:00:00', null);
insert into base_category3
values (263, '浴室用品', 30, '2021-12-14 00:00:00', null);
insert into base_category3
values (264, '缝纫/针织用品', 30, '2021-12-14 00:00:00', null);
insert into base_category3
values (265, '洗晒/熨烫', 30, '2021-12-14 00:00:00', null);
insert into base_category3
values (266, '净化除味', 30, '2021-12-14 00:00:00', null);
insert into base_category3
values (267, '相框/照片墙', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (268, '装饰字画', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (269, '节庆饰品', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (270, '手工/十字绣', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (271, '装饰摆件', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (272, '帘艺隔断', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (273, '墙贴/装饰贴', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (274, '钟饰', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (275, '花瓶花艺', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (276, '香薰蜡烛', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (277, '创意家居', 31, '2021-12-14 00:00:00', null);
insert into base_category3
values (278, '宠物主粮', 32, '2021-12-14 00:00:00', null);
insert into base_category3
values (279, '宠物零食', 32, '2021-12-14 00:00:00', null);
insert into base_category3
values (280, '医疗保健', 32, '2021-12-14 00:00:00', null);
insert into base_category3
values (281, '家居日用', 32, '2021-12-14 00:00:00', null);
insert into base_category3
values (282, '宠物玩具', 32, '2021-12-14 00:00:00', null);
insert into base_category3
values (283, '出行装备', 32, '2021-12-14 00:00:00', null);
insert into base_category3
values (284, '洗护美容', 32, '2021-12-14 00:00:00', null);
insert into base_category3
values (285, '笔记本', 33, '2021-12-14 00:00:00', null);
insert into base_category3
values (286, '超极本', 33, '2021-12-14 00:00:00', null);
insert into base_category3
values (287, '游戏本', 33, '2021-12-14 00:00:00', null);
insert into base_category3
values (288, '平板电脑', 33, '2021-12-14 00:00:00', null);
insert into base_category3
values (289, '平板电脑配件', 33, '2021-12-14 00:00:00', null);
insert into base_category3
values (290, '台式机', 33, '2021-12-14 00:00:00', null);
insert into base_category3
values (291, '服务器/工作站', 33, '2021-12-14 00:00:00', null);
insert into base_category3
values (292, '笔记本配件', 33, '2021-12-14 00:00:00', null);
insert into base_category3
values (293, '一体机', 33, '2021-12-14 00:00:00', null);
insert into base_category3
values (294, 'CPU', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (295, '主板', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (296, '显卡', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (297, '硬盘', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (298, 'SSD固态硬盘', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (299, '内存', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (300, '机箱', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (301, '电源', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (302, '显示器', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (303, '刻录机/光驱', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (304, '散热器', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (305, '声卡/扩展卡', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (306, '装机配件', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (307, '组装电脑', 34, '2021-12-14 00:00:00', null);
insert into base_category3
values (308, '移动硬盘', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (309, 'U盘', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (310, '鼠标', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (311, '键盘', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (312, '鼠标垫', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (313, '摄像头', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (314, '手写板', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (315, '硬盘盒', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (316, '插座', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (317, '线缆', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (318, 'UPS电源', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (319, '电脑工具', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (320, '游戏设备', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (321, '电玩', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (322, '电脑清洁', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (323, '网络仪表仪器', 35, '2021-12-14 00:00:00', null);
insert into base_category3
values (324, '游戏机', 36, '2021-12-14 00:00:00', null);
insert into base_category3
values (325, '游戏耳机', 36, '2021-12-14 00:00:00', null);
insert into base_category3
values (326, '手柄/方向盘', 36, '2021-12-14 00:00:00', null);
insert into base_category3
values (327, '游戏软件', 36, '2021-12-14 00:00:00', null);
insert into base_category3
values (328, '游戏周边', 36, '2021-12-14 00:00:00', null);
insert into base_category3
values (329, '路由器', 37, '2021-12-14 00:00:00', null);
insert into base_category3
values (330, '网卡', 37, '2021-12-14 00:00:00', null);
insert into base_category3
values (331, '交换机', 37, '2021-12-14 00:00:00', null);
insert into base_category3
values (332, '网络存储', 37, '2021-12-14 00:00:00', null);
insert into base_category3
values (333, '4G/3G上网', 37, '2021-12-14 00:00:00', null);
insert into base_category3
values (334, '网络盒子', 37, '2021-12-14 00:00:00', null);
insert into base_category3
values (335, '网络配件', 37, '2021-12-14 00:00:00', null);
insert into base_category3
values (336, '投影机', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (337, '投影配件', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (338, '多功能一体机', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (339, '打印机', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (340, '传真设备', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (341, '验钞/点钞机', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (342, '扫描设备', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (343, '复合机', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (344, '碎纸机', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (345, '考勤机', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (346, '收款/POS机', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (347, '会议音频视频', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (348, '保险柜', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (349, '装订/封装机', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (350, '安防监控', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (351, '办公家具', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (352, '白板', 38, '2021-12-14 00:00:00', null);
insert into base_category3
values (353, '硒鼓/墨粉', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (354, '墨盒', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (355, '色带', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (356, '纸类', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (357, '办公文具', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (358, '学生文具', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (359, '财会用品', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (360, '文件管理', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (361, '本册/便签', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (362, '计算器', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (363, '笔类', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (364, '画具画材', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (365, '刻录碟片/附件', 39, '2021-12-14 00:00:00', null);
insert into base_category3
values (366, '上门安装', 40, '2021-12-14 00:00:00', null);
insert into base_category3
values (367, '延保服务', 40, '2021-12-14 00:00:00', null);
insert into base_category3
values (368, '维修保养', 40, '2021-12-14 00:00:00', null);
insert into base_category3
values (369, '电脑软件', 40, '2021-12-14 00:00:00', null);
insert into base_category3
values (370, '京东服务', 40, '2021-12-14 00:00:00', null);
insert into base_category3
values (371, '炒锅', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (372, '煎锅', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (373, '压力锅', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (374, '蒸锅', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (375, '汤锅', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (376, '奶锅', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (377, '锅具套装', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (378, '煲类', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (379, '水壶', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (380, '火锅', 41, '2021-12-14 00:00:00', null);
insert into base_category3
values (381, '菜刀', 42, '2021-12-14 00:00:00', null);
insert into base_category3
values (382, '剪刀', 42, '2021-12-14 00:00:00', null);
insert into base_category3
values (383, '刀具套装', 42, '2021-12-14 00:00:00', null);
insert into base_category3
values (384, '砧板', 42, '2021-12-14 00:00:00', null);
insert into base_category3
values (385, '瓜果刀/刨', 42, '2021-12-14 00:00:00', null);
insert into base_category3
values (386, '多功能刀', 42, '2021-12-14 00:00:00', null);
insert into base_category3
values (387, '保鲜盒', 43, '2021-12-14 00:00:00', null);
insert into base_category3
values (388, '烘焙/烧烤', 43, '2021-12-14 00:00:00', null);
insert into base_category3
values (389, '饭盒/提锅', 43, '2021-12-14 00:00:00', null);
insert into base_category3
values (390, '储物/置物架', 43, '2021-12-14 00:00:00', null);
insert into base_category3
values (391, '厨房DIY/小工具', 43, '2021-12-14 00:00:00', null);
insert into base_category3
values (392, '塑料杯', 44, '2021-12-14 00:00:00', null);
insert into base_category3
values (393, '运动水壶', 44, '2021-12-14 00:00:00', null);
insert into base_category3
values (394, '玻璃杯', 44, '2021-12-14 00:00:00', null);
insert into base_category3
values (395, '陶瓷/马克杯', 44, '2021-12-14 00:00:00', null);
insert into base_category3
values (396, '保温杯', 44, '2021-12-14 00:00:00', null);
insert into base_category3
values (397, '保温壶', 44, '2021-12-14 00:00:00', null);
insert into base_category3
values (398, '酒杯/酒具', 44, '2021-12-14 00:00:00', null);
insert into base_category3
values (399, '杯具套装', 44, '2021-12-14 00:00:00', null);
insert into base_category3
values (400, '餐具套装', 45, '2021-12-14 00:00:00', null);
insert into base_category3
values (401, '碗/碟/盘', 45, '2021-12-14 00:00:00', null);
insert into base_category3
values (402, '筷勺/刀叉', 45, '2021-12-14 00:00:00', null);
insert into base_category3
values (403, '一次性用品', 45, '2021-12-14 00:00:00', null);
insert into base_category3
values (404, '果盘/果篮', 45, '2021-12-14 00:00:00', null);
insert into base_category3
values (405, '自助餐炉', 46, '2021-12-14 00:00:00', null);
insert into base_category3
values (406, '酒店餐具', 46, '2021-12-14 00:00:00', null);
insert into base_category3
values (407, '酒店水具', 46, '2021-12-14 00:00:00', null);
insert into base_category3
values (408, '整套茶具', 47, '2021-12-14 00:00:00', null);
insert into base_category3
values (409, '茶杯', 47, '2021-12-14 00:00:00', null);
insert into base_category3
values (410, '茶壶', 47, '2021-12-14 00:00:00', null);
insert into base_category3
values (411, '茶盘茶托', 47, '2021-12-14 00:00:00', null);
insert into base_category3
values (412, '茶叶罐', 47, '2021-12-14 00:00:00', null);
insert into base_category3
values (413, '茶具配件', 47, '2021-12-14 00:00:00', null);
insert into base_category3
values (414, '茶宠摆件', 47, '2021-12-14 00:00:00', null);
insert into base_category3
values (415, '咖啡具', 47, '2021-12-14 00:00:00', null);
insert into base_category3
values (416, '其他', 47, '2021-12-14 00:00:00', null);
insert into base_category3
values (417, '纸品湿巾', 48, '2021-12-14 00:00:00', null);
insert into base_category3
values (418, '衣物清洁', 48, '2021-12-14 00:00:00', null);
insert into base_category3
values (419, '清洁工具', 48, '2021-12-14 00:00:00', null);
insert into base_category3
values (420, '驱虫用品', 48, '2021-12-14 00:00:00', null);
insert into base_category3
values (421, '家庭清洁', 48, '2021-12-14 00:00:00', null);
insert into base_category3
values (422, '皮具护理', 48, '2021-12-14 00:00:00', null);
insert into base_category3
values (423, '一次性用品', 48, '2021-12-14 00:00:00', null);
insert into base_category3
values (424, '洁面', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (425, '乳液面霜', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (426, '面膜', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (427, '剃须', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (428, '套装', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (429, '精华', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (430, '眼霜', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (431, '卸妆', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (432, '防晒', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (433, '防晒隔离', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (434, 'T区护理', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (435, '眼部护理', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (436, '精华露', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (437, '爽肤水', 49, '2021-12-14 00:00:00', null);
insert into base_category3
values (438, '沐浴', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (439, '润肤', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (440, '颈部', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (441, '手足', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (442, '纤体塑形', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (443, '美胸', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (444, '套装', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (445, '精油', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (446, '洗发护发', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (447, '染发/造型', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (448, '香薰精油', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (449, '磨砂/浴盐', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (450, '手工/香皂', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (451, '洗发', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (452, '护发', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (453, '染发', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (454, '磨砂膏', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (455, '香皂', 50, '2021-12-14 00:00:00', null);
insert into base_category3
values (456, '牙膏/牙粉', 51, '2021-12-14 00:00:00', null);
insert into base_category3
values (457, '牙刷/牙线', 51, '2021-12-14 00:00:00', null);
insert into base_category3
values (458, '漱口水', 51, '2021-12-14 00:00:00', null);
insert into base_category3
values (459, '套装', 51, '2021-12-14 00:00:00', null);
insert into base_category3
values (460, '卫生巾', 52, '2021-12-14 00:00:00', null);
insert into base_category3
values (461, '卫生护垫', 52, '2021-12-14 00:00:00', null);
insert into base_category3
values (462, '私密护理', 52, '2021-12-14 00:00:00', null);
insert into base_category3
values (463, '脱毛膏', 52, '2021-12-14 00:00:00', null);
insert into base_category3
values (464, '其他', 52, '2021-12-14 00:00:00', null);
insert into base_category3
values (465, '洗发', 53, '2021-12-14 00:00:00', null);
insert into base_category3
values (466, '护发', 53, '2021-12-14 00:00:00', null);
insert into base_category3
values (467, '染发', 53, '2021-12-14 00:00:00', null);
insert into base_category3
values (468, '造型', 53, '2021-12-14 00:00:00', null);
insert into base_category3
values (469, '假发', 53, '2021-12-14 00:00:00', null);
insert into base_category3
values (470, '套装', 53, '2021-12-14 00:00:00', null);
insert into base_category3
values (471, '美发工具', 53, '2021-12-14 00:00:00', null);
insert into base_category3
values (472, '脸部护理', 53, '2021-12-14 00:00:00', null);
insert into base_category3
values (473, '香水', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (474, '底妆', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (475, '腮红', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (476, '眼影', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (477, '唇部', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (478, '美甲', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (479, '眼线', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (480, '美妆工具', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (481, '套装', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (482, '防晒隔离', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (483, '卸妆', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (484, '眉笔', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (485, '睫毛膏', 54, '2021-12-14 00:00:00', null);
insert into base_category3
values (486, 'T恤', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (487, '衬衫', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (488, '针织衫', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (489, '雪纺衫', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (490, '卫衣', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (491, '马甲', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (492, '连衣裙', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (493, '半身裙', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (494, '牛仔裤', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (495, '休闲裤', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (496, '打底裤', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (497, '正装裤', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (498, '小西装', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (499, '短外套', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (500, '风衣', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (501, '毛呢大衣', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (502, '真皮皮衣', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (503, '棉服', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (504, '羽绒服', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (505, '大码女装', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (506, '中老年女装', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (507, '婚纱', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (508, '打底衫', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (509, '旗袍/唐装', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (510, '加绒裤', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (511, '吊带/背心', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (512, '羊绒衫', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (513, '短裤', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (514, '皮草', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (515, '礼服', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (516, '仿皮皮衣', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (517, '羊毛衫', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (518, '设计师/潮牌', 55, '2021-12-14 00:00:00', null);
insert into base_category3
values (519, '衬衫', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (520, 'T恤', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (521, 'POLO衫', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (522, '针织衫', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (523, '羊绒衫', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (524, '卫衣', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (525, '马甲/背心', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (526, '夹克', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (527, '风衣', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (528, '毛呢大衣', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (529, '仿皮皮衣', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (530, '西服', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (531, '棉服', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (532, '羽绒服', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (533, '牛仔裤', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (534, '休闲裤', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (535, '西裤', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (536, '西服套装', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (537, '大码男装', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (538, '中老年男装', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (539, '唐装/中山装', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (540, '工装', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (541, '真皮皮衣', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (542, '加绒裤', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (543, '卫裤/运动裤', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (544, '短裤', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (545, '设计师/潮牌', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (546, '羊毛衫', 56, '2021-12-14 00:00:00', null);
insert into base_category3
values (547, '文胸', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (548, '女式内裤', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (549, '男式内裤', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (550, '睡衣/家居服', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (551, '塑身美体', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (552, '泳衣', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (553, '吊带/背心', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (554, '抹胸', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (555, '连裤袜/丝袜', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (556, '美腿袜', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (557, '商务男袜', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (558, '保暖内衣', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (559, '情侣睡衣', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (560, '文胸套装', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (561, '少女文胸', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (562, '休闲棉袜', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (563, '大码内衣', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (564, '内衣配件', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (565, '打底裤袜', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (566, '打底衫', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (567, '秋衣秋裤', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (568, '情趣内衣', 57, '2021-12-14 00:00:00', null);
insert into base_category3
values (569, '服装洗护', 58, '2021-12-14 00:00:00', null);
insert into base_category3
values (570, '太阳镜', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (571, '光学镜架/镜片', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (572, '围巾/手套/帽子套装', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (573, '袖扣', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (574, '棒球帽', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (575, '毛线帽', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (576, '遮阳帽', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (577, '老花镜', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (578, '装饰眼镜', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (579, '防辐射眼镜', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (580, '游泳镜', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (581, '女士丝巾/围巾/披肩', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (582, '男士丝巾/围巾', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (583, '鸭舌帽', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (584, '贝雷帽', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (585, '礼帽', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (586, '真皮手套', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (587, '毛线手套', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (588, '防晒手套', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (589, '男士腰带/礼盒', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (590, '女士腰带/礼盒', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (591, '钥匙扣', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (592, '遮阳伞/雨伞', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (593, '口罩', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (594, '耳罩/耳包', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (595, '假领', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (596, '毛线/布面料', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (597, '领带/领结/领带夹', 59, '2021-12-14 00:00:00', null);
insert into base_category3
values (598, '男表', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (599, '瑞表', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (600, '女表', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (601, '国表', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (602, '日韩表', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (603, '欧美表', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (604, '德表', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (605, '儿童手表', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (606, '智能手表', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (607, '闹钟', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (608, '座钟挂钟', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (609, '钟表配件', 60, '2021-12-14 00:00:00', null);
insert into base_category3
values (610, '商务休闲鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (611, '正装鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (612, '休闲鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (613, '凉鞋/沙滩鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (614, '男靴', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (615, '功能鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (616, '拖鞋/人字拖', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (617, '雨鞋/雨靴', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (618, '传统布鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (619, '鞋配件', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (620, '帆布鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (621, '增高鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (622, '工装鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (623, '定制鞋', 61, '2021-12-14 00:00:00', null);
insert into base_category3
values (624, '高跟鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (625, '单鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (626, '休闲鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (627, '凉鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (628, '女靴', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (629, '雪地靴', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (630, '拖鞋/人字拖', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (631, '踝靴', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (632, '筒靴', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (633, '帆布鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (634, '雨鞋/雨靴', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (635, '妈妈鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (636, '鞋配件', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (637, '特色鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (638, '鱼嘴鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (639, '布鞋/绣花鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (640, '马丁靴', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (641, '坡跟鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (642, '松糕鞋', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (643, '内增高', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (644, '防水台', 62, '2021-12-14 00:00:00', null);
insert into base_category3
values (645, '婴幼奶粉', 63, '2021-12-14 00:00:00', null);
insert into base_category3
values (646, '孕妈奶粉', 63, '2021-12-14 00:00:00', null);
insert into base_category3
values (647, '益生菌/初乳', 64, '2021-12-14 00:00:00', null);
insert into base_category3
values (648, '米粉/菜粉', 64, '2021-12-14 00:00:00', null);
insert into base_category3
values (649, '果泥/果汁', 64, '2021-12-14 00:00:00', null);
insert into base_category3
values (650, 'DHA', 64, '2021-12-14 00:00:00', null);
insert into base_category3
values (651, '宝宝零食', 64, '2021-12-14 00:00:00', null);
insert into base_category3
values (652, '钙铁锌/维生素', 64, '2021-12-14 00:00:00', null);
insert into base_category3
values (653, '清火/开胃', 64, '2021-12-14 00:00:00', null);
insert into base_category3
values (654, '面条/粥', 64, '2021-12-14 00:00:00', null);
insert into base_category3
values (655, '婴儿尿裤', 65, '2021-12-14 00:00:00', null);
insert into base_category3
values (656, '拉拉裤', 65, '2021-12-14 00:00:00', null);
insert into base_category3
values (657, '婴儿湿巾', 65, '2021-12-14 00:00:00', null);
insert into base_category3
values (658, '成人尿裤', 65, '2021-12-14 00:00:00', null);
insert into base_category3
values (659, '奶瓶奶嘴', 66, '2021-12-14 00:00:00', null);
insert into base_category3
values (660, '吸奶器', 66, '2021-12-14 00:00:00', null);
insert into base_category3
values (661, '暖奶消毒', 66, '2021-12-14 00:00:00', null);
insert into base_category3
values (662, '儿童餐具', 66, '2021-12-14 00:00:00', null);
insert into base_category3
values (663, '水壶/水杯', 66, '2021-12-14 00:00:00', null);
insert into base_category3
values (664, '牙胶安抚', 66, '2021-12-14 00:00:00', null);
insert into base_category3
values (665, '围兜/防溅衣', 66, '2021-12-14 00:00:00', null);
insert into base_category3
values (666, '辅食料理机', 66, '2021-12-14 00:00:00', null);
insert into base_category3
values (667, '食物存储', 66, '2021-12-14 00:00:00', null);
insert into base_category3
values (668, '宝宝护肤', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (669, '洗发沐浴', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (670, '奶瓶清洗', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (671, '驱蚊防晒', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (672, '理发器', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (673, '洗澡用具', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (674, '婴儿口腔清洁', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (675, '洗衣液/皂', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (676, '日常护理', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (677, '座便器', 67, '2021-12-14 00:00:00', null);
insert into base_category3
values (678, '婴儿推车', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (679, '餐椅摇椅', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (680, '婴儿床', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (681, '学步车', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (682, '三轮车', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (683, '自行车', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (684, '电动车', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (685, '扭扭车', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (686, '滑板车', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (687, '婴儿床垫', 68, '2021-12-14 00:00:00', null);
insert into base_category3
values (688, '婴儿外出服', 69, '2021-12-14 00:00:00', null);
insert into base_category3
values (689, '婴儿内衣', 69, '2021-12-14 00:00:00', null);
insert into base_category3
values (690, '婴儿礼盒', 69, '2021-12-14 00:00:00', null);
insert into base_category3
values (691, '婴儿鞋帽袜', 69, '2021-12-14 00:00:00', null);
insert into base_category3
values (692, '安全防护', 69, '2021-12-14 00:00:00', null);
insert into base_category3
values (693, '家居床品', 69, '2021-12-14 00:00:00', null);
insert into base_category3
values (694, '睡袋/抱被', 69, '2021-12-14 00:00:00', null);
insert into base_category3
values (695, '爬行垫', 69, '2021-12-14 00:00:00', null);
insert into base_category3
values (696, '妈咪包/背婴带', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (697, '产后塑身', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (698, '文胸/内裤', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (699, '防辐射服', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (700, '孕妈装', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (701, '孕期营养', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (702, '孕妇护肤', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (703, '待产护理', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (704, '月子装', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (705, '防溢乳垫', 70, '2021-12-14 00:00:00', null);
insert into base_category3
values (706, '套装', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (707, '上衣', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (708, '裤子', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (709, '裙子', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (710, '内衣/家居服', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (711, '羽绒服/棉服', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (712, '亲子装', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (713, '儿童配饰', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (714, '礼服/演出服', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (715, '运动鞋', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (716, '皮鞋/帆布鞋', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (717, '靴子', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (718, '凉鞋', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (719, '功能鞋', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (720, '户外/运动服', 71, '2021-12-14 00:00:00', null);
insert into base_category3
values (721, '提篮式', 72, '2021-12-14 00:00:00', null);
insert into base_category3
values (722, '安全座椅', 72, '2021-12-14 00:00:00', null);
insert into base_category3
values (723, '增高垫', 72, '2021-12-14 00:00:00', null);
insert into base_category3
values (724, '钱包', 73, '2021-12-14 00:00:00', null);
insert into base_category3
values (725, '手拿包', 73, '2021-12-14 00:00:00', null);
insert into base_category3
values (726, '单肩包', 73, '2021-12-14 00:00:00', null);
insert into base_category3
values (727, '双肩包', 73, '2021-12-14 00:00:00', null);
insert into base_category3
values (728, '手提包', 73, '2021-12-14 00:00:00', null);
insert into base_category3
values (729, '斜挎包', 73, '2021-12-14 00:00:00', null);
insert into base_category3
values (730, '钥匙包', 73, '2021-12-14 00:00:00', null);
insert into base_category3
values (731, '卡包/零钱包', 73, '2021-12-14 00:00:00', null);
insert into base_category3
values (732, '男士钱包', 74, '2021-12-14 00:00:00', null);
insert into base_category3
values (733, '男士手包', 74, '2021-12-14 00:00:00', null);
insert into base_category3
values (734, '卡包名片夹', 74, '2021-12-14 00:00:00', null);
insert into base_category3
values (735, '商务公文包', 74, '2021-12-14 00:00:00', null);
insert into base_category3
values (736, '双肩包', 74, '2021-12-14 00:00:00', null);
insert into base_category3
values (737, '单肩/斜挎包', 74, '2021-12-14 00:00:00', null);
insert into base_category3
values (738, '钥匙包', 74, '2021-12-14 00:00:00', null);
insert into base_category3
values (739, '电脑包', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (740, '拉杆箱', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (741, '旅行包', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (742, '旅行配件', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (743, '休闲运动包', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (744, '拉杆包', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (745, '登山包', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (746, '妈咪包', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (747, '书包', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (748, '相机包', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (749, '腰包/胸包', 75, '2021-12-14 00:00:00', null);
insert into base_category3
values (750, '火机烟具', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (751, '礼品文具', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (752, '军刀军具', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (753, '收藏品', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (754, '工艺礼品', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (755, '创意礼品', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (756, '礼盒礼券', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (757, '鲜花绿植', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (758, '婚庆节庆', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (759, '京东卡', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (760, '美妆礼品', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (761, '礼品定制', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (762, '京东福卡', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (763, '古董文玩', 76, '2021-12-14 00:00:00', null);
insert into base_category3
values (764, '箱包', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (765, '钱包', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (766, '服饰', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (767, '腰带', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (768, '太阳镜/眼镜框', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (769, '配件', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (770, '鞋靴', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (771, '饰品', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (772, '名品腕表', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (773, '高档化妆品', 77, '2021-12-14 00:00:00', null);
insert into base_category3
values (774, '婚嫁首饰', 78, '2021-12-14 00:00:00', null);
insert into base_category3
values (775, '婚纱摄影', 78, '2021-12-14 00:00:00', null);
insert into base_category3
values (776, '婚纱礼服', 78, '2021-12-14 00:00:00', null);
insert into base_category3
values (777, '婚庆服务', 78, '2021-12-14 00:00:00', null);
insert into base_category3
values (778, '婚庆礼品/用品', 78, '2021-12-14 00:00:00', null);
insert into base_category3
values (779, '婚宴', 78, '2021-12-14 00:00:00', null);
insert into base_category3
values (780, '饼干蛋糕', 79, '2021-12-14 00:00:00', null);
insert into base_category3
values (781, '糖果/巧克力', 79, '2021-12-14 00:00:00', null);
insert into base_category3
values (782, '休闲零食', 79, '2021-12-14 00:00:00', null);
insert into base_category3
values (783, '冲调饮品', 79, '2021-12-14 00:00:00', null);
insert into base_category3
values (784, '粮油调味', 79, '2021-12-14 00:00:00', null);
insert into base_category3
values (785, '牛奶', 79, '2021-12-14 00:00:00', null);
insert into base_category3
values (786, '其他特产', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (787, '新疆', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (788, '北京', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (789, '山西', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (790, '内蒙古', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (791, '福建', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (792, '湖南', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (793, '四川', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (794, '云南', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (795, '东北', 80, '2021-12-14 00:00:00', null);
insert into base_category3
values (796, '休闲零食', 81, '2021-12-14 00:00:00', null);
insert into base_category3
values (797, '坚果炒货', 81, '2021-12-14 00:00:00', null);
insert into base_category3
values (798, '肉干肉脯', 81, '2021-12-14 00:00:00', null);
insert into base_category3
values (799, '蜜饯果干', 81, '2021-12-14 00:00:00', null);
insert into base_category3
values (800, '糖果/巧克力', 81, '2021-12-14 00:00:00', null);
insert into base_category3
values (801, '饼干蛋糕', 81, '2021-12-14 00:00:00', null);
insert into base_category3
values (802, '无糖食品', 81, '2021-12-14 00:00:00', null);
insert into base_category3
values (803, '米面杂粮', 82, '2021-12-14 00:00:00', null);
insert into base_category3
values (804, '食用油', 82, '2021-12-14 00:00:00', null);
insert into base_category3
values (805, '调味品', 82, '2021-12-14 00:00:00', null);
insert into base_category3
values (806, '南北干货', 82, '2021-12-14 00:00:00', null);
insert into base_category3
values (807, '方便食品', 82, '2021-12-14 00:00:00', null);
insert into base_category3
values (808, '有机食品', 82, '2021-12-14 00:00:00', null);
insert into base_category3
values (809, '饮用水', 83, '2021-12-14 00:00:00', null);
insert into base_category3
values (810, '饮料', 83, '2021-12-14 00:00:00', null);
insert into base_category3
values (811, '牛奶乳品', 83, '2021-12-14 00:00:00', null);
insert into base_category3
values (812, '咖啡/奶茶', 83, '2021-12-14 00:00:00', null);
insert into base_category3
values (813, '冲饮谷物', 83, '2021-12-14 00:00:00', null);
insert into base_category3
values (814, '蜂蜜/柚子茶', 83, '2021-12-14 00:00:00', null);
insert into base_category3
values (815, '成人奶粉', 83, '2021-12-14 00:00:00', null);
insert into base_category3
values (816, '月饼', 84, '2021-12-14 00:00:00', null);
insert into base_category3
values (817, '大闸蟹', 84, '2021-12-14 00:00:00', null);
insert into base_category3
values (818, '粽子', 84, '2021-12-14 00:00:00', null);
insert into base_category3
values (819, '卡券', 84, '2021-12-14 00:00:00', null);
insert into base_category3
values (820, '铁观音', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (821, '普洱', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (822, '龙井', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (823, '绿茶', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (824, '红茶', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (825, '乌龙茶', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (826, '花草茶', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (827, '花果茶', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (828, '养生茶', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (829, '黑茶', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (830, '白茶', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (831, '其它茶', 85, '2021-12-14 00:00:00', null);
insert into base_category3
values (832, '项链', 86, '2021-12-14 00:00:00', null);
insert into base_category3
values (833, '手链/脚链', 86, '2021-12-14 00:00:00', null);
insert into base_category3
values (834, '戒指', 86, '2021-12-14 00:00:00', null);
insert into base_category3
values (835, '耳饰', 86, '2021-12-14 00:00:00', null);
insert into base_category3
values (836, '毛衣链', 86, '2021-12-14 00:00:00', null);
insert into base_category3
values (837, '发饰/发卡', 86, '2021-12-14 00:00:00', null);
insert into base_category3
values (838, '胸针', 86, '2021-12-14 00:00:00', null);
insert into base_category3
values (839, '饰品配件', 86, '2021-12-14 00:00:00', null);
insert into base_category3
values (840, '婚庆饰品', 86, '2021-12-14 00:00:00', null);
insert into base_category3
values (841, '黄金吊坠', 87, '2021-12-14 00:00:00', null);
insert into base_category3
values (842, '黄金项链', 87, '2021-12-14 00:00:00', null);
insert into base_category3
values (843, '黄金转运珠', 87, '2021-12-14 00:00:00', null);
insert into base_category3
values (844, '黄金手镯/手链/脚链', 87, '2021-12-14 00:00:00', null);
insert into base_category3
values (845, '黄金耳饰', 87, '2021-12-14 00:00:00', null);
insert into base_category3
values (846, '黄金戒指', 87, '2021-12-14 00:00:00', null);
insert into base_category3
values (847, 'K金吊坠', 88, '2021-12-14 00:00:00', null);
insert into base_category3
values (848, 'K金项链', 88, '2021-12-14 00:00:00', null);
insert into base_category3
values (849, 'K金手镯/手链/脚链', 88, '2021-12-14 00:00:00', null);
insert into base_category3
values (850, 'K金戒指', 88, '2021-12-14 00:00:00', null);
insert into base_category3
values (851, 'K金耳饰', 88, '2021-12-14 00:00:00', null);
insert into base_category3
values (852, '投资金', 89, '2021-12-14 00:00:00', null);
insert into base_category3
values (853, '投资银', 89, '2021-12-14 00:00:00', null);
insert into base_category3
values (854, '投资收藏', 89, '2021-12-14 00:00:00', null);
insert into base_category3
values (855, '银吊坠/项链', 90, '2021-12-14 00:00:00', null);
insert into base_category3
values (856, '银手镯/手链/脚链', 90, '2021-12-14 00:00:00', null);
insert into base_category3
values (857, '银戒指', 90, '2021-12-14 00:00:00', null);
insert into base_category3
values (858, '银耳饰', 90, '2021-12-14 00:00:00', null);
insert into base_category3
values (859, '足银手镯', 90, '2021-12-14 00:00:00', null);
insert into base_category3
values (860, '宝宝银饰', 90, '2021-12-14 00:00:00', null);
insert into base_category3
values (861, '裸钻', 91, '2021-12-14 00:00:00', null);
insert into base_category3
values (862, '钻戒', 91, '2021-12-14 00:00:00', null);
insert into base_category3
values (863, '钻石项链/吊坠', 91, '2021-12-14 00:00:00', null);
insert into base_category3
values (864, '钻石耳饰', 91, '2021-12-14 00:00:00', null);
insert into base_category3
values (865, '钻石手镯/手链', 91, '2021-12-14 00:00:00', null);
insert into base_category3
values (866, '项链/吊坠', 92, '2021-12-14 00:00:00', null);
insert into base_category3
values (867, '手镯/手串', 92, '2021-12-14 00:00:00', null);
insert into base_category3
values (868, '戒指', 92, '2021-12-14 00:00:00', null);
insert into base_category3
values (869, '耳饰', 92, '2021-12-14 00:00:00', null);
insert into base_category3
values (870, '挂件/摆件/把件', 92, '2021-12-14 00:00:00', null);
insert into base_category3
values (871, '玉石孤品', 92, '2021-12-14 00:00:00', null);
insert into base_category3
values (872, '项链/吊坠', 93, '2021-12-14 00:00:00', null);
insert into base_category3
values (873, '耳饰', 93, '2021-12-14 00:00:00', null);
insert into base_category3
values (874, '手镯/手链/脚链', 93, '2021-12-14 00:00:00', null);
insert into base_category3
values (875, '戒指', 93, '2021-12-14 00:00:00', null);
insert into base_category3
values (876, '头饰/胸针', 93, '2021-12-14 00:00:00', null);
insert into base_category3
values (877, '摆件/挂件', 93, '2021-12-14 00:00:00', null);
insert into base_category3
values (878, '琥珀/蜜蜡', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (879, '碧玺', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (880, '红宝石/蓝宝石', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (881, '坦桑石', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (882, '珊瑚', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (883, '祖母绿', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (884, '葡萄石', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (885, '其他天然宝石', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (886, '项链/吊坠', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (887, '耳饰', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (888, '手镯/手链', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (889, '戒指', 94, '2021-12-14 00:00:00', null);
insert into base_category3
values (890, '铂金项链/吊坠', 95, '2021-12-14 00:00:00', null);
insert into base_category3
values (891, '铂金手镯/手链/脚链', 95, '2021-12-14 00:00:00', null);
insert into base_category3
values (892, '铂金戒指', 95, '2021-12-14 00:00:00', null);
insert into base_category3
values (893, '铂金耳饰', 95, '2021-12-14 00:00:00', null);
insert into base_category3
values (894, '小叶紫檀', 96, '2021-12-14 00:00:00', null);
insert into base_category3
values (895, '黄花梨', 96, '2021-12-14 00:00:00', null);
insert into base_category3
values (896, '沉香木', 96, '2021-12-14 00:00:00', null);
insert into base_category3
values (897, '金丝楠', 96, '2021-12-14 00:00:00', null);
insert into base_category3
values (898, '菩提', 96, '2021-12-14 00:00:00', null);
insert into base_category3
values (899, '其他', 96, '2021-12-14 00:00:00', null);
insert into base_category3
values (900, '橄榄核/核桃', 96, '2021-12-14 00:00:00', null);
insert into base_category3
values (901, '檀香', 96, '2021-12-14 00:00:00', null);
insert into base_category3
values (902, '珍珠项链', 97, '2021-12-14 00:00:00', null);
insert into base_category3
values (903, '珍珠吊坠', 97, '2021-12-14 00:00:00', null);
insert into base_category3
values (904, '珍珠耳饰', 97, '2021-12-14 00:00:00', null);
insert into base_category3
values (905, '珍珠手链', 97, '2021-12-14 00:00:00', null);
insert into base_category3
values (906, '珍珠戒指', 97, '2021-12-14 00:00:00', null);
insert into base_category3
values (907, '珍珠胸针', 97, '2021-12-14 00:00:00', null);
insert into base_category3
values (908, '机油', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (909, '正时皮带', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (910, '添加剂', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (911, '汽车喇叭', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (912, '防冻液', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (913, '汽车玻璃', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (914, '滤清器', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (915, '火花塞', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (916, '减震器', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (917, '柴机油/辅助油', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (918, '雨刷', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (919, '车灯', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (920, '后视镜', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (921, '轮胎', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (922, '轮毂', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (923, '刹车片/盘', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (924, '维修配件', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (925, '蓄电池', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (926, '底盘装甲/护板', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (927, '贴膜', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (928, '汽修工具', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (929, '改装配件', 98, '2021-12-14 00:00:00', null);
insert into base_category3
values (930, '导航仪', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (931, '安全预警仪', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (932, '行车记录仪', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (933, '倒车雷达', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (934, '蓝牙设备', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (935, '车载影音', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (936, '净化器', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (937, '电源', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (938, '智能驾驶', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (939, '车载电台', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (940, '车载电器配件', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (941, '吸尘器', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (942, '智能车机', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (943, '冰箱', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (944, '汽车音响', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (945, '车载生活电器', 99, '2021-12-14 00:00:00', null);
insert into base_category3
values (946, '车蜡', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (947, '补漆笔', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (948, '玻璃水', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (949, '清洁剂', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (950, '洗车工具', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (951, '镀晶镀膜', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (952, '打蜡机', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (953, '洗车配件', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (954, '洗车机', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (955, '洗车水枪', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (956, '毛巾掸子', 100, '2021-12-14 00:00:00', null);
insert into base_category3
values (957, '脚垫', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (958, '座垫', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (959, '座套', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (960, '后备箱垫', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (961, '头枕腰靠', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (962, '方向盘套', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (963, '香水', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (964, '空气净化', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (965, '挂件摆件', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (966, '功能小件', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (967, '车身装饰件', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (968, '车衣', 101, '2021-12-14 00:00:00', null);
insert into base_category3
values (969, '安全座椅', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (970, '胎压监测', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (971, '防盗设备', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (972, '应急救援', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (973, '保温箱', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (974, '地锁', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (975, '摩托车', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (976, '充气泵', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (977, '储物箱', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (978, '自驾野营', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (979, '摩托车装备', 102, '2021-12-14 00:00:00', null);
insert into base_category3
values (980, '清洗美容', 103, '2021-12-14 00:00:00', null);
insert into base_category3
values (981, '功能升级', 103, '2021-12-14 00:00:00', null);
insert into base_category3
values (982, '保养维修', 103, '2021-12-14 00:00:00', null);
insert into base_category3
values (983, '油卡充值', 103, '2021-12-14 00:00:00', null);
insert into base_category3
values (984, '车险', 103, '2021-12-14 00:00:00', null);
insert into base_category3
values (985, '加油卡', 103, '2021-12-14 00:00:00', null);
insert into base_category3
values (986, 'ETC', 103, '2021-12-14 00:00:00', null);
insert into base_category3
values (987, '驾驶培训', 103, '2021-12-14 00:00:00', null);
insert into base_category3
values (988, '赛事服装', 104, '2021-12-14 00:00:00', null);
insert into base_category3
values (989, '赛事用品', 104, '2021-12-14 00:00:00', null);
insert into base_category3
values (990, '制动系统', 104, '2021-12-14 00:00:00', null);
insert into base_category3
values (991, '悬挂系统', 104, '2021-12-14 00:00:00', null);
insert into base_category3
values (992, '进气系统', 104, '2021-12-14 00:00:00', null);
insert into base_category3
values (993, '排气系统', 104, '2021-12-14 00:00:00', null);
insert into base_category3
values (994, '电子管理', 104, '2021-12-14 00:00:00', null);
insert into base_category3
values (995, '车身强化', 104, '2021-12-14 00:00:00', null);
insert into base_category3
values (996, '赛事座椅', 104, '2021-12-14 00:00:00', null);
insert into base_category3
values (997, '跑步鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (998, '休闲鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (999, '篮球鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (1000, '板鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (1001, '帆布鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (1002, '足球鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (1003, '乒羽网鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (1004, '专项运动鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (1005, '训练鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (1006, '拖鞋', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (1007, '运动包', 105, '2021-12-14 00:00:00', null);
insert into base_category3
values (1008, '羽绒服', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1009, '棉服', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1010, '运动裤', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1011, '夹克/风衣', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1012, '卫衣/套头衫', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1013, 'T恤', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1014, '套装', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1015, '乒羽网服', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1016, '健身服', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1017, '运动背心', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1018, '毛衫/线衫', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1019, '运动配饰', 106, '2021-12-14 00:00:00', null);
insert into base_category3
values (1020, '折叠车', 107, '2021-12-14 00:00:00', null);
insert into base_category3
values (1021, '山地车/公路车', 107, '2021-12-14 00:00:00', null);
insert into base_category3
values (1022, '电动车', 107, '2021-12-14 00:00:00', null);
insert into base_category3
values (1023, '其他整车', 107, '2021-12-14 00:00:00', null);
insert into base_category3
values (1024, '骑行服', 107, '2021-12-14 00:00:00', null);
insert into base_category3
values (1025, '骑行装备', 107, '2021-12-14 00:00:00', null);
insert into base_category3
values (1026, '平衡车', 107, '2021-12-14 00:00:00', null);
insert into base_category3
values (1027, '鱼竿鱼线', 108, '2021-12-14 00:00:00', null);
insert into base_category3
values (1028, '浮漂鱼饵', 108, '2021-12-14 00:00:00', null);
insert into base_category3
values (1029, '钓鱼桌椅', 108, '2021-12-14 00:00:00', null);
insert into base_category3
values (1030, '钓鱼配件', 108, '2021-12-14 00:00:00', null);
insert into base_category3
values (1031, '钓箱鱼包', 108, '2021-12-14 00:00:00', null);
insert into base_category3
values (1032, '其它', 108, '2021-12-14 00:00:00', null);
insert into base_category3
values (1033, '泳镜', 109, '2021-12-14 00:00:00', null);
insert into base_category3
values (1034, '泳帽', 109, '2021-12-14 00:00:00', null);
insert into base_category3
values (1035, '游泳包防水包', 109, '2021-12-14 00:00:00', null);
insert into base_category3
values (1036, '女士泳衣', 109, '2021-12-14 00:00:00', null);
insert into base_category3
values (1037, '男士泳衣', 109, '2021-12-14 00:00:00', null);
insert into base_category3
values (1038, '比基尼', 109, '2021-12-14 00:00:00', null);
insert into base_category3
values (1039, '其它', 109, '2021-12-14 00:00:00', null);
insert into base_category3
values (1040, '冲锋衣裤', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1041, '速干衣裤', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1042, '滑雪服', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1043, '羽绒服/棉服', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1044, '休闲衣裤', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1045, '抓绒衣裤', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1046, '软壳衣裤', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1047, 'T恤', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1048, '户外风衣', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1049, '功能内衣', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1050, '军迷服饰', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1051, '登山鞋', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1052, '雪地靴', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1053, '徒步鞋', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1054, '越野跑鞋', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1055, '休闲鞋', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1056, '工装鞋', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1057, '溯溪鞋', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1058, '沙滩/凉拖', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1059, '户外袜', 110, '2021-12-14 00:00:00', null);
insert into base_category3
values (1060, '帐篷/垫子', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1061, '睡袋/吊床', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1062, '登山攀岩', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1063, '户外配饰', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1064, '背包', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1065, '户外照明', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1066, '户外仪表', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1067, '户外工具', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1068, '望远镜', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1069, '旅游用品', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1070, '便携桌椅床', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1071, '野餐烧烤', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1072, '军迷用品', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1073, '救援装备', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1074, '滑雪装备', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1075, '极限户外', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1076, '冲浪潜水', 111, '2021-12-14 00:00:00', null);
insert into base_category3
values (1077, '综合训练器', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1078, '其他大型器械', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1079, '哑铃', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1080, '仰卧板/收腹机', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1081, '其他中小型器材', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1082, '瑜伽舞蹈', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1083, '甩脂机', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1084, '踏步机', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1085, '武术搏击', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1086, '健身车/动感单车', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1087, '跑步机', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1088, '运动护具', 112, '2021-12-14 00:00:00', null);
insert into base_category3
values (1089, '羽毛球', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1090, '乒乓球', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1091, '篮球', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1092, '足球', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1093, '网球', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1094, '排球', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1095, '高尔夫', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1096, '台球', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1097, '棋牌麻将', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1098, '轮滑滑板', 113, '2021-12-14 00:00:00', null);
insert into base_category3
values (1099, '其他', 113, '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for base_dic
-- ----------------------------
drop table if exists base_dic;
create table if not exists base_dic
(
    dic_code     varchar(10) not null comment '编号',
    dic_name     varchar(100) comment '编码名称',
    parent_code  varchar(10) comment '父编号',
    create_time  datetime comment '创建日期',
    operate_time datetime comment '修改日期',
    primary key (dic_code) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci
  row_format = dynamic;

-- ----------------------------
-- Records of base_dic
-- ----------------------------
insert into base_dic
values ('07', '退单状态', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('0701', '商家审核中', '07', '2021-12-14 00:00:00', null);
insert into base_dic
values ('0702', '商家审核通过', '07', '2021-12-14 00:00:00', null);
insert into base_dic
values ('0703', '商家审核未通过', '07', '2021-12-14 00:00:00', null);
insert into base_dic
values ('0704', '买家已发货', '07', '2021-12-14 00:00:00', null);
insert into base_dic
values ('0705', '退单完成', '07', '2021-12-14 00:00:00', null);
insert into base_dic
values ('0706', '退单失败', '07', '2021-12-14 00:00:00', null);
insert into base_dic
values ('10', '单据状态', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('1001', '未支付', '10', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1002', '已支付', '10', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1003', '已取消', '10', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1004', '已完成', '10', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1005', '退款中', '10', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1006', '退款完成', '10', '2021-12-14 00:00:00', null);
insert into base_dic
values ('11', '支付状态', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('1101', '支付宝', '11', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1102', '微信', '11', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1103', '银联', '11', '2021-12-14 00:00:00', null);
insert into base_dic
values ('12', '评价', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('1201', '好评', '12', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1202', '中评', '12', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1203', '差评', '12', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1204', '自动', '12', '2021-12-14 00:00:00', null);
insert into base_dic
values ('13', '退货原因', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('1301', '质量问题', '13', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1302', '商品描述与实际描述不一致', '13', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1303', '缺货', '13', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1304', '号码不合适', '13', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1305', '拍错', '13', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1306', '不想买了', '13', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1307', '其他', '13', '2021-12-14 00:00:00', null);
insert into base_dic
values ('14', '购物券状态', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('1401', '未使用', '14', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1402', '使用中', '14', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1403', '已使用', '14', '2021-12-14 00:00:00', null);
insert into base_dic
values ('15', '退款类型', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('1501', '仅退款', '15', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1502', '退货退款', '15', '2021-12-14 00:00:00', null);
insert into base_dic
values ('16', '支付状态', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('1601', '未支付', '16', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1602', '已支付', '16', '2021-12-14 00:00:00', null);
insert into base_dic
values ('1603', '取消支付', '16', '2021-12-14 00:00:00', null);
insert into base_dic
values ('24', '来源类型', '', '2021-12-14 00:00:00', null);
insert into base_dic
values ('2401', '用户查询', '24', '2021-12-14 00:00:00', null);
insert into base_dic
values ('2402', '商品推广', '24', '2021-12-14 00:00:00', null);
insert into base_dic
values ('2403', '智能推荐', '24', '2021-12-14 00:00:00', null);
insert into base_dic
values ('2404', '促销活动', '24', '2021-12-14 00:00:00', null);
insert into base_dic
values ('31', '活动类型', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('3101', '满额减价', '31', '2021-12-14 00:00:00', null);
insert into base_dic
values ('3102', '满量打折', '31', '2021-12-14 00:00:00', null);
insert into base_dic
values ('3103', '直接折扣', '31', '2021-12-14 00:00:00', null);
insert into base_dic
values ('32', '购物券类型', '', '2021-12-14 00:00:00', null);
insert into base_dic
values ('3201', '满额减价', '32', '2021-12-14 00:00:00', null);
insert into base_dic
values ('3202', '满量打折', '32', '2021-12-14 00:00:00', null);
insert into base_dic
values ('3203', '代金券', '32', '2021-12-14 00:00:00', null);
insert into base_dic
values ('33', '优惠券范围', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('3301', '品类券', '33', '2021-12-14 00:00:00', null);
insert into base_dic
values ('3302', '品牌券', '33', '2021-12-14 00:00:00', null);
insert into base_dic
values ('3303', '单品(spu)', '33', '2021-12-14 00:00:00', null);
insert into base_dic
values ('35', '付款方式', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('3501', '在线支付', '35', '2021-12-14 00:00:00', null);
insert into base_dic
values ('3502', '货到付款', '35', '2021-12-14 00:00:00', null);
insert into base_dic
values ('41', '营销类型', null, '2021-12-14 00:00:00', null);
insert into base_dic
values ('4101', '固定', '41', '2021-12-14 00:00:00', null);
insert into base_dic
values ('4102', '算法', '41', '2021-12-14 00:00:00', null);
insert into base_dic
values ('42', '坑位类型', '', '2021-12-14 00:00:00', null);
insert into base_dic
values ('4201', 'banner', '', '2021-12-14 00:00:00', null);
insert into base_dic
values ('4202', '宫格', '42', '2021-12-14 00:00:00', null);
insert into base_dic
values ('4203', '列表', '42', '2021-12-14 00:00:00', null);
insert into base_dic
values ('4204', '瀑布', '42', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for base_frontend_param
-- ----------------------------
drop table if exists base_frontend_param;
create table if not exists base_frontend_param
(
    id           bigint       not null auto_increment comment '编号',
    code         varchar(100) not null comment '属性名称',
    delete_id    bigint comment '分类id',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '前端数据保护表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_frontend_param
-- ----------------------------

-- ----------------------------
-- Table structure for base_province
-- ----------------------------
drop table if exists base_province;
create table if not exists base_province
(
    id           bigint not null comment 'id',
    name         varchar(20) comment '省份名称',
    region_id    varchar(20) comment '地区id',
    area_code    varchar(20) comment '地区编码',
    iso_code     varchar(20) comment '旧版国际标准地区编码，供可视化使用',
    iso_3166_2   varchar(20) comment '新版国际标准地区编码，供可视化使用',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '省份表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_province
-- ----------------------------
insert into base_province
values (1, '北京', '1', '110000', 'CN-11', 'CN-BJ', '2021-12-14 00:00:00', null);
insert into base_province
values (2, '天津', '1', '120000', 'CN-12', 'CN-TJ', '2021-12-14 00:00:00', null);
insert into base_province
values (3, '山西', '1', '140000', 'CN-14', 'CN-SX', '2021-12-14 00:00:00', null);
insert into base_province
values (4, '内蒙古', '1', '150000', 'CN-15', 'CN-NM', '2021-12-14 00:00:00', null);
insert into base_province
values (5, '河北', '1', '130000', 'CN-13', 'CN-HE', '2021-12-14 00:00:00', null);
insert into base_province
values (6, '上海', '2', '310000', 'CN-31', 'CN-SH', '2021-12-14 00:00:00', null);
insert into base_province
values (7, '江苏', '2', '320000', 'CN-32', 'CN-JS', '2021-12-14 00:00:00', null);
insert into base_province
values (8, '浙江', '2', '330000', 'CN-33', 'CN-ZJ', '2021-12-14 00:00:00', null);
insert into base_province
values (9, '安徽', '2', '340000', 'CN-34', 'CN-AH', '2021-12-14 00:00:00', null);
insert into base_province
values (10, '福建', '2', '350000', 'CN-35', 'CN-FJ', '2021-12-14 00:00:00', null);
insert into base_province
values (11, '江西', '2', '360000', 'CN-36', 'CN-JX', '2021-12-14 00:00:00', null);
insert into base_province
values (12, '山东', '2', '370000', 'CN-37', 'CN-SD', '2021-12-14 00:00:00', null);
insert into base_province
values (13, '重庆', '6', '500000', 'CN-50', 'CN-CQ', '2021-12-14 00:00:00', null);
insert into base_province
values (14, '台湾', '2', '710000', 'CN-71', 'CN-TW', '2021-12-14 00:00:00', null);
insert into base_province
values (15, '黑龙江', '3', '230000', 'CN-23', 'CN-HL', '2021-12-14 00:00:00', null);
insert into base_province
values (16, '吉林', '3', '220000', 'CN-22', 'CN-JL', '2021-12-14 00:00:00', null);
insert into base_province
values (17, '辽宁', '3', '210000', 'CN-21', 'CN-LN', '2021-12-14 00:00:00', null);
insert into base_province
values (18, '陕西', '7', '610000', 'CN-61', 'CN-SN', '2021-12-14 00:00:00', null);
insert into base_province
values (19, '甘肃', '7', '620000', 'CN-62', 'CN-GS', '2021-12-14 00:00:00', null);
insert into base_province
values (20, '青海', '7', '630000', 'CN-63', 'CN-QH', '2021-12-14 00:00:00', null);
insert into base_province
values (21, '宁夏', '7', '640000', 'CN-64', 'CN-NX', '2021-12-14 00:00:00', null);
insert into base_province
values (22, '新疆', '7', '650000', 'CN-65', 'CN-XJ', '2021-12-14 00:00:00', null);
insert into base_province
values (23, '河南', '4', '410000', 'CN-41', 'CN-HA', '2021-12-14 00:00:00', null);
insert into base_province
values (24, '湖北', '4', '420000', 'CN-42', 'CN-HB', '2021-12-14 00:00:00', null);
insert into base_province
values (25, '湖南', '4', '430000', 'CN-43', 'CN-HN', '2021-12-14 00:00:00', null);
insert into base_province
values (26, '广东', '5', '440000', 'CN-44', 'CN-GD', '2021-12-14 00:00:00', null);
insert into base_province
values (27, '广西', '5', '450000', 'CN-45', 'CN-GX', '2021-12-14 00:00:00', null);
insert into base_province
values (28, '海南', '5', '460000', 'CN-46', 'CN-HI', '2021-12-14 00:00:00', null);
insert into base_province
values (29, '香港', '5', '810000', 'CN-91', 'CN-HK', '2021-12-14 00:00:00', null);
insert into base_province
values (30, '澳门', '5', '820000', 'CN-92', 'CN-MO', '2021-12-14 00:00:00', null);
insert into base_province
values (31, '四川', '6', '510000', 'CN-51', 'CN-SC', '2021-12-14 00:00:00', null);
insert into base_province
values (32, '贵州', '6', '520000', 'CN-52', 'CN-GZ', '2021-12-14 00:00:00', null);
insert into base_province
values (33, '云南', '6', '530000', 'CN-53', 'CN-YN', '2021-12-14 00:00:00', null);
insert into base_province
values (34, '西藏', '6', '540000', 'CN-54', 'CN-XZ', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for base_region
-- ----------------------------
drop table if exists base_region;
create table if not exists base_region
(
    id           varchar(20) comment '地区id',
    region_name  varchar(20) comment '地区名称',
    create_time  datetime comment '创建时间',
    operate_time datetime
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '地区表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_region
-- ----------------------------
insert into base_region
values ('1', '华北', '2020-05-01 11:20:40', null);
insert into base_region
values ('2', '华东', '2020-05-01 11:20:40', null);
insert into base_region
values ('3', '东北', '2020-05-01 11:20:40', null);
insert into base_region
values ('4', '华中', '2020-05-01 11:20:40', null);
insert into base_region
values ('5', '华南', '2020-05-01 11:20:40', null);
insert into base_region
values ('6', '西南', '2020-05-01 11:20:40', null);
insert into base_region
values ('7', '西北', '2020-05-01 11:20:40', null);

-- ----------------------------
-- Table structure for base_sale_attr
-- ----------------------------
drop table if exists base_sale_attr;
create table if not exists base_sale_attr
(
    id           bigint      not null auto_increment comment '编号',
    name         varchar(20) not null comment '销售属性名称',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 5
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '基本销售属性表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_sale_attr
-- ----------------------------
insert into base_sale_attr
values (1, '颜色', '2021-12-14 00:00:00', null);
insert into base_sale_attr
values (2, '版本', '2021-12-14 00:00:00', null);
insert into base_sale_attr
values (3, '尺码', '2021-12-14 00:00:00', null);
insert into base_sale_attr
values (4, '类别', '2021-12-14 00:00:00', null);
insert into base_sale_attr
values (5, '处理器或内存', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for base_trademark
-- ----------------------------
drop table if exists base_trademark;
create table if not exists base_trademark
(
    id           bigint       not null auto_increment comment '编号',
    tm_name      varchar(100) not null comment '品牌名称',
    logo_url     varchar(200) comment '品牌logo的图片路径',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 16
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '品牌表'
  row_format = dynamic;

-- ----------------------------
-- Records of base_trademark
-- ----------------------------
insert into base_trademark
values (1, '红米', null, '2021-12-14 00:00:00', null);
insert into base_trademark
values (2, '苹果', '/static/default.jpg2323', '2021-12-14 00:00:00', null);
insert into base_trademark
values (3, '联想', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (4, 'TCL', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (5, '小米', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (6, '长粒香', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (7, '金沙河', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (8, '索芙特', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (9, 'CAREMiLLE', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (10, '欧莱雅', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (11, '香奈儿', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (12, '华为', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (13, 'H&U&W', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (14, 'VIVO', '/static/default.jpg', '2021-12-14 00:00:00', null);
insert into base_trademark
values (15, 'OPPO', '/static/default.jpg', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for cart_info
-- ----------------------------
drop table if exists cart_info;
create table if not exists cart_info
(
    id           bigint not null auto_increment comment '编号',
    user_id      varchar(200) comment '用户id',
    sku_id       bigint comment 'skuid',
    cart_price   decimal(10, 2) comment '放入购物车时价格',
    sku_num      int comment '数量',
    img_url      varchar(200) comment '商品图片地址',
    sku_name     varchar(200) comment 'sku名称 (冗余)',
    is_checked   int comment '是否被选中',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    is_ordered   bigint comment '是否已经下单',
    order_time   datetime comment '下单时间',
    primary key (id) using btree,
    index idx_uid (user_id asc) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '购物车表'
  row_format = dynamic;

-- ----------------------------
-- Records of cart_info
-- ----------------------------

-- ----------------------------
-- Table structure for cms_banner
-- ----------------------------
drop table if exists cms_banner;
create table if not exists cms_banner
(
    id           bigint                                                        not null auto_increment comment 'ID',
    title        varchar(20) character set utf8mb4 collate utf8mb4_0900_ai_ci  null     default '' comment '标题',
    image_url    varchar(500) character set utf8mb4 collate utf8mb4_0900_ai_ci not null default '' comment '图片地址',
    link_url     varchar(500) character set utf8mb4 collate utf8mb4_0900_ai_ci null     default '' comment '链接地址',
    sort         int unsigned                                                  not null default 0 comment '排序',
    create_time  datetime                                                      null     default null comment '创建时间',
    operate_time datetime                                                      null     default null comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_0900_ai_ci comment = '首页banner表'
  row_format = dynamic;

-- ----------------------------
-- Records of cms_banner
-- ----------------------------

-- ----------------------------
-- Table structure for comment_info
-- ----------------------------
drop table if exists comment_info;
create table if not exists comment_info
(
    id           bigint not null auto_increment comment '编号',
    user_id      bigint comment '用户id',
    nick_name    varchar(20) comment '用户昵称',
    head_img     varchar(200),
    sku_id       bigint comment 'skuid',
    spu_id       bigint comment 'spuid',
    order_id     bigint comment '订单编号',
    appraise     varchar(10) comment '评价 1 好评 2 中评 3 差评',
    comment_txt  varchar(2000) comment '评价内容',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '商品评论表'
  row_format = dynamic;

-- ----------------------------
-- Records of comment_info
-- ----------------------------

-- ----------------------------
-- Table structure for coupon_info
-- ----------------------------
drop table if exists coupon_info;
create table if not exists coupon_info
(
    id               bigint         not null auto_increment comment '购物券编号',
    coupon_name      varchar(100)   null     default null comment '购物券名称',
    coupon_type      varchar(10)    null     default null comment '购物券类型 1 现金券 2 折扣券 3 满减券 4 满件打折券',
    condition_amount decimal(10, 2) null     default null comment '满额数',
    condition_num    bigint         null     default null comment '满件数',
    activity_id      bigint         null     default null comment '活动编号',
    benefit_amount   decimal(16, 2) null     default null comment '减免金额',
    benefit_discount decimal(10, 2) null     default null comment '折扣',
    create_time      datetime       null     default null comment '创建时间',
    range_type       varchar(10)    null     default null comment '范围类型 1、商品(spuid) 2、品类(三级分类id) 3、品牌',
    limit_num        int            not null default 0 comment '最多领用次数',
    taken_count      int            not null default 0 comment '已领用次数',
    start_time       datetime       null     default null comment '可以领取的开始时间',
    end_time         datetime       null     default null comment '可以领取的结束时间',
    operate_time     datetime       null     default null comment '修改时间',
    expire_time      datetime       null     default null comment '过期时间',
    range_desc       varchar(500)   null     default null comment '范围描述',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 5
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '优惠券信息表'
  row_format = dynamic;

-- ----------------------------
-- Records of coupon_info
-- ----------------------------
insert into coupon_info
values (1, '口红品类券满99减30', '3201', 99.00, null, null, 30.00, null, '2022-06-06 00:00:00', '3301', 100, 0,
        '2022-02-13 01:15:41', '2023-12-13 01:15:58', null, '2023-12-13 01:15:58', null);
insert into coupon_info
values (2, '口红品类券满199减70', '3201', 199.00, null, null, 70.00, null, '2022-05-20 00:00:00', '3301', 100, 0,
        '2022-02-13 01:15:41', '2023-12-13 01:15:58', null, '2023-12-13 01:15:58', null);
insert into coupon_info
values (3, '口红品类券满499减100', '3201', 499.00, null, null, 100.00, null, '2022-06-02 00:00:00', '3301', 100, 0,
        '2022-02-13 01:15:41', '2023-12-13 01:15:58', null, '2023-12-13 01:15:58', null);
insert into coupon_info
values (4, '金沙河面条买二送一', '3202', null, 2, null, 0.00, 5.00, '2022-06-02 00:00:00', '3302', 100, 0,
        '2022-02-13 01:15:41', '2023-12-13 01:15:58', null, '2023-12-13 01:15:58', null);
insert into coupon_info
values (5, 'iPhone 代金券', '3203', null, null, null, 300.00, null, '2022-06-02 00:00:00', '3303', 100, 0,
        '2022-02-13 01:15:41', '2023-12-13 01:15:58', null, null, null);

-- ----------------------------
-- Table structure for coupon_range
-- ----------------------------
drop table if exists coupon_range;
create table if not exists coupon_range
(
    id           bigint      not null auto_increment comment '购物券编号',
    coupon_id    bigint      not null default 0 comment '优惠券id',
    range_type   varchar(10) not null default '' comment '范围类型 1、商品(spuid) 2、品类(三级分类id) 3、品牌',
    range_id     bigint      not null default 0,
    create_time  datetime    null     default null comment '创建时间',
    operate_time datetime    null     default null comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 5
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '优惠券范围表'
  row_format = dynamic;

-- ----------------------------
-- Records of coupon_range
-- ----------------------------
insert into coupon_range
values (1, 1, '3301', 477, '2021-12-14 00:00:00', null);
insert into coupon_range
values (2, 2, '3301', 477, '2021-12-14 00:00:00', null);
insert into coupon_range
values (3, 3, '3301', 477, '2021-12-14 00:00:00', null);
insert into coupon_range
values (4, 4, '3302', 6, '2021-12-14 00:00:00', null);
insert into coupon_range
values (5, 5, '3303', 0, '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for coupon_use
-- ----------------------------
drop table if exists coupon_use;
create table if not exists coupon_use
(
    id            bigint not null auto_increment comment '编号',
    coupon_id     bigint comment '购物券ID',
    user_id       bigint comment '用户ID',
    order_id      bigint comment '订单ID',
    coupon_status varchar(10) comment '购物券状态（1：未使用 2：已使用）',
    get_time      datetime comment '获取时间',
    using_time    datetime comment '使用时间',
    used_time     datetime comment '支付时间',
    expire_time   datetime comment '过期时间',
    create_time   datetime comment '创建时间',
    operate_time  datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '优惠券领用表'
  row_format = dynamic;

-- ----------------------------
-- Records of coupon_use
-- ----------------------------

-- ----------------------------
-- Table structure for entity_mapping
-- ----------------------------
drop table if exists entity_mapping;
create table if not exists entity_mapping
(
    id          int not null auto_increment comment '主键',
    entity_type varchar(255) comment '实体类型（spu_name,attr_name,attr_value）',
    std_name    varchar(255) comment '标准词',
    synonym     varchar(255) comment '同义词',
    distance    double comment '距离',
    is_reviewed int comment '是否通过审核（1：审核通过，0：审核未通过）',
    primary key (id) using btree,
    unique index unique_idx (std_name asc, synonym asc) using btree
) engine = InnoDB
  auto_increment = 23
  character set = utf8mb4
  collate = utf8mb4_general_ci
  row_format = dynamic;

-- ----------------------------
-- Records of entity_mapping
-- ----------------------------
insert into entity_mapping
values (1, 'spu_name', '小米12S Ultra', '小米12S Ultra', 0, 1);
insert into entity_mapping
values (2, 'spu_name', 'Redmi 10X', 'Redmi 10X', 0, 1);
insert into entity_mapping
values (3, 'spu_name', 'Apple iPhone 12', 'Apple iPhone 12', 0, 1);
insert into entity_mapping
values (4, 'spu_name', '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑',
        '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑', 0, 1);
insert into entity_mapping
values (5, 'spu_name', 'TCL巨幕私人影院电视 4K超高清 AI智慧屏  液晶平板电视机',
        'TCL巨幕私人影院电视 4K超高清 AI智慧屏  液晶平板电视机', 0, 1);
insert into entity_mapping
values (6, 'spu_name', '小米电视 内置小爱 智能网络液晶平板教育电视', '小米电视 内置小爱 智能网络液晶平板教育电视', 0,
        1);
insert into entity_mapping
values (7, 'spu_name', '十月稻田 长粒香大米 东北大米 东北香米 5kg', '十月稻田 长粒香大米 东北大米 东北香米 5kg', 0, 1);
insert into entity_mapping
values (8, 'spu_name', '金沙河面条 原味银丝挂面 龙须面 方便速食拉面 清汤面 900g',
        '金沙河面条 原味银丝挂面 龙须面 方便速食拉面 清汤面 900g', 0, 1);
insert into entity_mapping
values (9, 'spu_name', '索芙特i-Softto 口红不掉色唇膏保湿滋润 璀璨金钻哑光唇膏 ',
        '索芙特i-Softto 口红不掉色唇膏保湿滋润 璀璨金钻哑光唇膏 ', 0, 1);
insert into entity_mapping
values (10, 'spu_name', 'CAREMiLLE珂曼奶油小方口红 雾面滋润保湿持久丝缎唇膏',
        'CAREMiLLE珂曼奶油小方口红 雾面滋润保湿持久丝缎唇膏', 0, 1);
insert into entity_mapping
values (11, 'spu_name', '香奈儿（Chanel）女士香水5号香水 粉邂逅柔情淡香水EDT ',
        '香奈儿（Chanel）女士香水5号香水 粉邂逅柔情淡香水EDT ', 0, 1);
insert into entity_mapping
values (12, 'spu_name', '华为智慧屏 4K全面屏智能电视机', '华为智慧屏 4K全面屏智能电视机', 0, 1);
insert into entity_mapping
values (13, 'spu_name', 'HAWEIAI Book 2025英特尔14 Pro满血独显笔记本', 'HAWEIAI Book 2025英特尔14 Pro满血独显笔记本', 0,
        1);
insert into entity_mapping
values (14, 'spu_name', '华为HUAWEI二手笔记本MateBook13触屏2K全面屏', '华为HUAWEI二手笔记本MateBook13触屏2K全面屏', 0,
        1);
insert into entity_mapping
values (15, 'spu_name', 'H&U&W国行笔记本电脑轻薄本', 'H&U&W国行笔记本电脑轻薄本', 0, 1);
insert into entity_mapping
values (16, 'spu_name', 'vivo S20', 'vivo S20', 0, 1);
insert into entity_mapping
values (17, 'spu_name', 'REDMI Turbo4 Pro', 'REDMI Turbo4 Pro', 0, 1);
insert into entity_mapping
values (18, 'spu_name', '华为Mate 40 pro', '华为Mate 40 pro', 0, 1);
insert into entity_mapping
values (19, 'spu_name', 'Apple/苹果 iPhone 16 Pro', 'Apple/苹果 iPhone 16 Pro', 0, 1);
insert into entity_mapping
values (20, 'spu_name', 'OPPO Find X8', 'OPPO Find X8', 0, 1);
insert into entity_mapping
values (21, 'spu_name', '小米12S Ultra', '小米12s ultr', 0.33665862679481506, 1);
insert into entity_mapping
values (22, 'spu_name', '小米12S Ultra', 'xiaomi 12s ultra', 0.4070693254470825, 1);
insert into entity_mapping
values (23, 'spu_name', '小米12S Ultra', 'MI 12s ultr', 0.6911226511001587, 1);

-- ----------------------------
-- Table structure for favor_info
-- ----------------------------
drop table if exists favor_info;
create table if not exists favor_info
(
    id           bigint not null auto_increment comment '编号',
    user_id      bigint comment '用户id',
    sku_id       bigint comment 'skuid',
    spu_id       bigint comment 'spuid',
    is_cancel    varchar(1) comment '是否已取消 0 正常 1 已取消',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '商品收藏表'
  row_format = dynamic;

-- ----------------------------
-- Records of favor_info
-- ----------------------------

-- ----------------------------
-- Table structure for financial_sku_cost
-- ----------------------------
drop table if exists financial_sku_cost;
create table if not exists financial_sku_cost
(
    id          varchar(20) not null,
    sku_id      bigint comment 'sku_id',
    sku_name    varchar(20) comment 'sku名称',
    busi_date   varchar(20) comment '业务日期',
    is_lastest  varchar(2) comment '是否最近',
    sku_cost    decimal(16, 2) comment '商品结算成本',
    create_time datetime comment '创建时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci
  row_format = dynamic;

-- ----------------------------
-- Records of financial_sku_cost
-- ----------------------------

-- ----------------------------
-- Table structure for order_detail
-- ----------------------------
drop table if exists order_detail;
create table if not exists order_detail
(
    id                    bigint not null auto_increment comment '编号',
    order_id              bigint comment '订单id',
    sku_id                bigint comment 'sku_id',
    sku_name              varchar(200) comment 'sku名称（冗余)',
    img_url               varchar(200) comment '图片链接（冗余)',
    order_price           decimal(10, 2) comment '购买价格(下单时sku价格）',
    sku_num               bigint comment '购买个数',
    create_time           datetime comment '创建时间',
    split_total_amount    decimal(16, 2),
    split_activity_amount decimal(16, 2),
    split_coupon_amount   decimal(16, 2),
    operate_time          datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '订单明细表'
  row_format = dynamic;

-- ----------------------------
-- Records of order_detail
-- ----------------------------

-- ----------------------------
-- Table structure for order_detail_activity
-- ----------------------------
drop table if exists order_detail_activity;
create table if not exists order_detail_activity
(
    id               bigint not null auto_increment comment '编号',
    order_id         bigint comment '订单id',
    order_detail_id  bigint comment '订单明细id',
    activity_id      bigint comment '活动id',
    activity_rule_id bigint comment '活动规则id',
    sku_id           bigint comment 'skuid',
    create_time      datetime comment '创建时间',
    operate_time     datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '订单明细活动关联表'
  row_format = dynamic;

-- ----------------------------
-- Records of order_detail_activity
-- ----------------------------

-- ----------------------------
-- Table structure for order_detail_coupon
-- ----------------------------
drop table if exists order_detail_coupon;
create table if not exists order_detail_coupon
(
    id              bigint not null auto_increment comment '编号',
    order_id        bigint comment '订单id',
    order_detail_id bigint comment '订单明细id',
    coupon_id       bigint comment '购物券id',
    coupon_use_id   bigint comment '购物券领用id',
    sku_id          bigint comment 'skuid',
    create_time     datetime comment '创建时间',
    operate_time    datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '订单明细优惠券关联表'
  row_format = dynamic;

-- ----------------------------
-- Records of order_detail_coupon
-- ----------------------------

-- ----------------------------
-- Table structure for order_info
-- ----------------------------
drop table if exists order_info;
create table if not exists order_info
(
    id                     bigint not null auto_increment comment '编号',
    consignee              varchar(100) comment '收货人',
    consignee_tel          varchar(20) comment '收件人电话',
    total_amount           decimal(10, 2) comment '总金额',
    order_status           varchar(20) comment '订单状态',
    user_id                bigint comment '用户id',
    payment_way            varchar(20) comment '付款方式',
    delivery_address       varchar(1000) comment '送货地址',
    order_comment          varchar(200) comment '订单备注',
    out_trade_no           varchar(50) comment '订单交易编号（第三方支付用)',
    trade_body             varchar(200) comment '订单描述(第三方支付用)',
    create_time            datetime comment '创建时间',
    operate_time           datetime comment '操作时间',
    expire_time            datetime comment '失效时间',
    process_status         varchar(20) comment '进度状态',
    tracking_no            varchar(100) comment '物流单编号',
    parent_order_id        bigint comment '父订单编号',
    img_url                varchar(200) comment '图片链接',
    province_id            int comment '省份id',
    activity_reduce_amount decimal(16, 2) comment '活动减免金额',
    coupon_reduce_amount   decimal(16, 2) comment '优惠券减免金额',
    original_total_amount  decimal(16, 2) comment '原始总金额',
    feight_fee             decimal(16, 2) comment '运费金额',
    feight_fee_reduce      decimal(16, 2) comment '运费减免金额',
    refundable_time        datetime comment '可退款时间（签收后30天）',
    primary key (id) using btree,
    index idx_uid_status (order_status asc, user_id asc) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '订单表'
  row_format = dynamic;

-- ----------------------------
-- Records of order_info
-- ----------------------------

-- ----------------------------
-- Table structure for order_refund_info
-- ----------------------------
drop table if exists order_refund_info;
create table if not exists order_refund_info
(
    id                 bigint not null auto_increment comment '编号',
    user_id            bigint comment '用户id',
    order_id           bigint comment '订单id',
    sku_id             bigint comment 'skuid',
    refund_type        varchar(20) comment '退款类型',
    refund_num         bigint comment '退货件数',
    refund_amount      decimal(16, 2) comment '退款金额',
    refund_reason_type varchar(200) comment '原因类型',
    refund_reason_txt  varchar(20) comment '原因内容',
    refund_status      varchar(10) comment '退款状态（0：待审批 1：已退款）',
    create_time        datetime comment '创建时间',
    operate_time       datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '退单表'
  row_format = dynamic;

-- ----------------------------
-- Records of order_refund_info
-- ----------------------------

-- ----------------------------
-- Table structure for order_status_log
-- ----------------------------
drop table if exists order_status_log;
create table if not exists order_status_log
(
    id           bigint not null auto_increment comment '编号',
    order_id     bigint comment '订单id',
    order_status varchar(11) comment '订单状态',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '订单状态流水表'
  row_format = dynamic;

-- ----------------------------
-- Records of order_status_log
-- ----------------------------

-- ----------------------------
-- Table structure for payment_info
-- ----------------------------
drop table if exists payment_info;
create table if not exists payment_info
(
    id               int  not null auto_increment comment '编号',
    out_trade_no     varchar(50) comment '对外业务编号',
    order_id         bigint comment '订单id',
    user_id          bigint comment '用户id',
    payment_type     varchar(20) comment '支付类型（微信 支付宝）',
    trade_no         varchar(50) comment '交易编号',
    total_amount     decimal(10, 2) comment '支付金额',
    subject          varchar(200) comment '交易内容',
    payment_status   varchar(20) comment '支付状态',
    create_time      datetime comment '创建时间',
    callback_time    datetime comment '回调时间',
    callback_content text null comment '回调信息',
    operate_time     datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '支付信息表'
  row_format = dynamic;

-- ----------------------------
-- Records of payment_info
-- ----------------------------

-- ----------------------------
-- Table structure for promotion_pos
-- ----------------------------
drop table if exists promotion_pos;
create table if not exists promotion_pos
(
    id             bigint not null comment '营销坑位id',
    pos_location   varchar(200) comment '营销坑位位置',
    pos_type       varchar(20) comment '营销坑位类型：banner,宫格,列表, 瀑布',
    promotion_type varchar(20) comment '营销类型：算法、固定、搜索',
    create_time    datetime comment '创建时间',
    operate_time   datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '营销坑位表'
  row_format = dynamic;

-- ----------------------------
-- Records of promotion_pos
-- ----------------------------
insert into promotion_pos
values (1, '首页banner', '4201', '4101', '2021-12-14 00:00:00', null);
insert into promotion_pos
values (2, '首页下方瀑布推荐', '4204', '4102', '2021-12-14 00:00:00', null);
insert into promotion_pos
values (3, '搜索页排行列表', '4203', '4102', '2021-12-14 00:00:00', null);
insert into promotion_pos
values (4, '详情页下方9宫格', '4202', '4102', '2021-12-14 00:00:00', null);
insert into promotion_pos
values (5, '购物车底部瀑布', '4104', '4102', '2021-12-14 00:00:00', null);
insert into promotion_pos
values (6, '我的页底部瀑布', '4104', '4102', '2021-12-14 00:00:00', null);
insert into promotion_pos
values (7, '新品精选-新发现瀑布', '4204', '4101', '2021-12-14 00:00:00', null);
insert into promotion_pos
values (8, '双十一活动页瀑布', '4204', '4101', '2021-12-14 00:00:00', null);
insert into promotion_pos
values (9, '双十一活动banner', '4201', '4101', '2021-12-14 00:00:00', null);
insert into promotion_pos
values (10, '商品搜索结果列表瀑布', '4204', '4103', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for promotion_refer
-- ----------------------------
drop table if exists promotion_refer;
create table if not exists promotion_refer
(
    id           bigint not null comment '外部营销渠道id',
    refer_name   varchar(200) comment '外部营销渠道名称',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '营销渠道表'
  row_format = dynamic;

-- ----------------------------
-- Records of promotion_refer
-- ----------------------------
insert into promotion_refer
values (1, '百度推广', '2021-12-14 00:00:00', null);
insert into promotion_refer
values (2, '小红书软文', '2021-12-14 00:00:00', null);
insert into promotion_refer
values (3, '手机推送消息', '2021-12-14 00:00:00', null);
insert into promotion_refer
values (4, '微信公众号', '2021-12-14 00:00:00', null);
insert into promotion_refer
values (5, '微博推广', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for refund_payment
-- ----------------------------
drop table if exists refund_payment;
create table if not exists refund_payment
(
    id               int  not null auto_increment comment '编号',
    out_trade_no     varchar(50) comment '对外业务编号',
    order_id         bigint comment '订单id',
    sku_id           bigint comment 'skuid',
    payment_type     varchar(20) comment '支付类型（微信 支付宝）',
    trade_no         varchar(50) comment '交易编号',
    total_amount     decimal(10, 2) comment '退款金额',
    subject          varchar(200) comment '交易内容',
    refund_status    varchar(30) comment '退款状态',
    create_time      datetime comment '创建时间',
    callback_time    datetime comment '回调时间',
    callback_content text null comment '回调信息',
    operate_time     datetime comment '修改时间',
    primary key (id) using btree,
    index idx_out_trade_no (out_trade_no asc) using btree,
    index idx_order_id (order_id asc) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '退款支付表'
  row_format = dynamic;

-- ----------------------------
-- Records of refund_payment
-- ----------------------------

-- ----------------------------
-- Table structure for seckill_goods
-- ----------------------------
drop table if exists seckill_goods;
create table if not exists seckill_goods
(
    id              bigint not null auto_increment,
    spu_id          bigint comment 'spu_id',
    sku_id          bigint comment 'sku_id',
    sku_name        varchar(100) comment '标题',
    sku_default_img varchar(150) comment '商品图片',
    price           decimal(10, 2) comment '原价格',
    cost_price      decimal(10, 2) comment '秒杀价格',
    create_time     datetime comment '添加日期',
    check_time      datetime comment '审核日期',
    status          varchar(1) comment '审核状态',
    start_time      datetime comment '开始时间',
    end_time        datetime comment '结束时间',
    num             int comment '秒杀商品数',
    stock_count     int comment '剩余库存数',
    sku_desc        varchar(2000) comment '描述',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci
  row_format = dynamic;

-- ----------------------------
-- Records of seckill_goods
-- ----------------------------

-- ----------------------------
-- Table structure for sku_attr_value
-- ----------------------------
drop table if exists sku_attr_value;
create table if not exists sku_attr_value
(
    id           bigint not null auto_increment comment '编号',
    attr_id      bigint comment '平台属性id（冗余)',
    value_id     bigint comment '平台属性值id',
    sku_id       bigint comment 'skuid',
    attr_name    varchar(30) comment '平台属性名称',
    value_name   varchar(30) comment '平台属性值名称',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 129
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = 'sku平台属性值关联表'
  row_format = dynamic;

-- ----------------------------
-- Records of sku_attr_value
-- ----------------------------
insert into sku_attr_value
values (1, 106, 176, 1, '手机一级1', '安卓手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (2, 107, 177, 1, '二级手机2', '小米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (3, 23, 83, 1, '运行内存', '8G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (4, 24, 82, 1, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (5, 106, 176, 2, '手机一级', '安卓手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (6, 107, 177, 2, '二级手机', '小米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (7, 23, 83, 2, '运行内存', '8G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (8, 24, 166, 2, '机身内存', '256G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (9, 106, 176, 3, '手机一级', '安卓手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (10, 107, 177, 3, '二级手机', '小米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (11, 23, 83, 3, '运行内存', '8G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (12, 24, 82, 3, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (13, 106, 176, 4, '手机一级', '安卓手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (14, 107, 177, 4, '二级手机', '小米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (15, 23, 14, 4, '运行内存', '4G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (16, 24, 82, 4, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (17, 106, 176, 5, '手机一级', '安卓手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (18, 107, 177, 5, '二级手机', '小米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (19, 23, 14, 5, '运行内存', '4G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (20, 24, 82, 5, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (21, 106, 176, 6, '手机一级', '安卓手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (22, 107, 177, 6, '二级手机', '小米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (23, 23, 83, 6, '运行内存', '8G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (24, 24, 82, 6, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (25, 106, 176, 7, '手机一级', '安卓手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (26, 107, 177, 7, '二级手机', '小米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (27, 23, 83, 7, '运行内存', '8G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (28, 24, 82, 7, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (29, 106, 175, 8, '手机一级', '苹果手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (30, 107, 179, 8, '二级手机', '苹果', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (31, 23, 14, 8, '运行内存', '4G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (32, 24, 82, 8, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (33, 106, 175, 9, '手机一级', '苹果手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (34, 107, 179, 9, '二级手机', '苹果', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (35, 23, 14, 9, '运行内存', '4G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (36, 24, 82, 9, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (37, 106, 175, 10, '手机一级', '苹果手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (38, 107, 179, 10, '二级手机', '苹果', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (39, 23, 14, 10, '运行内存', '4G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (40, 24, 82, 10, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (41, 106, 175, 11, '手机一级', '苹果手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (42, 107, 179, 11, '二级手机', '苹果', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (43, 23, 14, 11, '运行内存', '4G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (44, 24, 82, 11, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (45, 106, 175, 12, '手机一级', '苹果手机', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (46, 107, 179, 12, '二级手机', '苹果', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (47, 23, 14, 12, '运行内存', '4G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (48, 24, 82, 12, '机身内存', '128G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (49, 25, 20, 13, '处理器', 'i9', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (50, 26, 22, 13, '显卡', 'RTX3060', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (51, 66, 84, 13, '硬盘', '512GB', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (52, 67, 86, 13, '内存', '16G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (53, 25, 20, 14, '处理器', 'i9', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (54, 26, 21, 14, '显卡', 'RTX3070Ti', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (55, 66, 84, 14, '硬盘', '512GB', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (56, 67, 86, 14, '内存', '16G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (57, 25, 19, 15, '处理器', 'i7', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (58, 26, 22, 15, '显卡', 'RTX3060', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (59, 66, 84, 15, '硬盘', '512GB', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (60, 67, 82, 15, '内存', '16G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (61, 25, 19, 16, '处理器', 'i7', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (62, 26, 22, 16, '显卡', 'RTX3060', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (63, 66, 85, 16, '硬盘', '512GB+2T', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (64, 67, 82, 16, '内存', '16G', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (65, 89, 136, 17, '电视类型', '4K超清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (66, 96, 195, 17, '屏幕尺寸', '60-70', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (67, 97, 147, 17, '分辨率', '4K超高清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (68, 98, 149, 17, '观看距离', '3.5m', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (69, 89, 136, 17, '电视类型', '4K超清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (70, 89, 136, 18, '电视类型', '4K超清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (71, 96, 144, 18, '屏幕尺寸', '70-75', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (72, 97, 146, 18, '分辨率', '8K超高清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (73, 98, 149, 18, '观看距离', '3.5m', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (74, 89, 136, 18, '电视类型', '4K超清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (75, 89, 193, 19, '电视类型', '人工智能', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (76, 96, 145, 19, '屏幕尺寸', '75以上', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (77, 97, 148, 19, '分辨率', '12K超高清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (78, 98, 149, 19, '观看距离', '3.5m', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (79, 89, 136, 19, '电视类型', '4K超清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (80, 89, 192, 20, '电视类型', '超薄', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (81, 96, 195, 20, '屏幕尺寸', '60-70', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (82, 97, 147, 20, '分辨率', '4K超高清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (83, 98, 150, 20, '观看距离', '3m', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (84, 89, 136, 20, '电视类型', '4K超清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (85, 89, 191, 21, '电视类型', '曲面', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (86, 96, 144, 21, '屏幕尺寸', '70-75', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (87, 97, 147, 21, '分辨率', '4K超高清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (88, 98, 150, 21, '观看距离', '3m', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (89, 89, 136, 21, '电视类型', '4K超清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (90, 108, 197, 22, '粮食调味', '大米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (91, 109, 201, 22, '是否有机', '非有机食品', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (92, 110, 203, 22, '分类', '米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (93, 108, 197, 23, '粮食调味', '大米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (94, 109, 201, 23, '是否有机', '非有机食品', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (95, 110, 203, 23, '分类', '米', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (96, 108, 198, 24, '粮食调味', '面食', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (97, 109, 200, 24, '是否有机', '有机食品', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (98, 110, 204, 24, '分类', '面', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (99, 108, 198, 25, '粮食调味', '面食', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (100, 109, 200, 25, '是否有机', '有机食品', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (101, 110, 204, 25, '分类', '面', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (102, 111, 206, 26, '功效', '滋润', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (103, 112, 210, 26, '香水彩妆', '口红', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (104, 113, 212, 26, '面部护肤', '润唇膏', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (105, 111, 207, 27, '功效', '保湿', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (106, 112, 210, 27, '香水彩妆', '口红', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (107, 113, 212, 27, '面部护肤', '润唇膏', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (108, 111, 208, 28, '功效', '防水', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (109, 112, 210, 28, '香水彩妆', '口红', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (110, 113, 212, 28, '面部护肤', '润唇膏', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (111, 111, 209, 29, '功效', '防晒', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (112, 112, 210, 29, '香水彩妆', '口红', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (113, 113, 212, 29, '面部护肤', '润唇膏', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (114, 111, 207, 30, '功效', '保湿', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (115, 112, 210, 30, '香水彩妆', '口红', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (116, 113, 212, 30, '面部护肤', '润唇膏', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (117, 111, 209, 31, '功效', '防晒', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (118, 112, 210, 31, '香水彩妆', '口红', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (119, 113, 212, 31, '面部护肤', '润唇膏', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (120, 114, 216, 32, '香调', '海洋香调', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (121, 114, 215, 33, '香调', '花果香调', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (122, 89, 136, 34, '电视类型', '4K超清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (123, 96, 194, 34, '屏幕尺寸', '60以下', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (124, 97, 147, 34, '分辨率', '4K超高清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (125, 98, 150, 34, '观看距离', '3m', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (126, 89, 193, 35, '电视类型', '人工智能', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (127, 96, 195, 35, '屏幕尺寸', '60-70', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (128, 97, 147, 35, '分辨率', '4K超高清', '2021-12-14 00:00:00', null);
insert into sku_attr_value
values (129, 98, 150, 35, '观看距离', '3m', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for sku_image
-- ----------------------------
drop table if exists sku_image;
create table if not exists sku_image
(
    id           bigint not null auto_increment comment '编号',
    sku_id       bigint comment 'skuid',
    img_name     varchar(200) comment '图片名称（冗余）',
    img_url      varchar(300) comment '图片路径(冗余)',
    spu_img_id   bigint comment 'spu图片id',
    is_default   varchar(4000) comment '是否默认',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 245
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '库存单元图片表'
  row_format = dynamic;

-- ----------------------------
-- Records of sku_image
-- ----------------------------
insert into sku_image
values (1, 1, 'ead186426badb626.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAHpFuAACTenfIJWo734.jpg',
        2, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (2, 1, 'b58ab2d79b859f39.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAcbl2AAFopp2WGBQ404.jpg',
        3, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (3, 1, '0d93a071c839d890.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmATs5EAABriLbF9vE207.jpg',
        4, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (4, 1, 'a7b1125239354d0d.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAeWopAAEtpBjP1VQ788.jpg',
        5, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (5, 1, '6029cb2c2b2c7668.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAZJX2AAGmVo8Tz9s683.jpg',
        6, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (6, 1, '2ff0882c9607e57c.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAIpgZAAIvrX6L9fo612.jpg',
        1, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (7, 2, 'ead186426badb626.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAHpFuAACTenfIJWo734.jpg',
        2, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (8, 2, 'b58ab2d79b859f39.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAcbl2AAFopp2WGBQ404.jpg',
        3, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (9, 2, '0d93a071c839d890.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmATs5EAABriLbF9vE207.jpg',
        4, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (10, 2, 'a7b1125239354d0d.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAeWopAAEtpBjP1VQ788.jpg',
        5, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (11, 2, '6029cb2c2b2c7668.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAZJX2AAGmVo8Tz9s683.jpg',
        6, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (12, 3, '2ff0882c9607e57c.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAIpgZAAIvrX6L9fo612.jpg',
        1, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (13, 3, 'ead186426badb626.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAHpFuAACTenfIJWo734.jpg',
        2, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (14, 3, 'b58ab2d79b859f39.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAcbl2AAFopp2WGBQ404.jpg',
        3, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (15, 3, '0d93a071c839d890.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmATs5EAABriLbF9vE207.jpg',
        4, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (16, 3, 'a7b1125239354d0d.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAeWopAAEtpBjP1VQ788.jpg',
        5, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (17, 3, '6029cb2c2b2c7668.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAZJX2AAGmVo8Tz9s683.jpg',
        6, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (18, 4, '2b78b6fdabfd2fbe.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rgJqAHPnoAAF9hoDNfsc505.jpg',
        7, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (19, 4, '5d5c57ab443f5fbb.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAbNFZAADi9nT5SuM524.jpg',
        8, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (20, 4, 'cef3c55b8caad783.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAMq2nAAGtjwY17fA932.jpg',
        9, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (21, 4, '6eaaecc91b9ad059.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAXjRKAAFpxKwrSvY886.jpg',
        10, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (22, 4, 'b7bea7af48e935fd.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqARA19AAFuZ18W_ks439.jpg',
        11, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (23, 5, '2b78b6fdabfd2fbe.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rgJqAHPnoAAF9hoDNfsc505.jpg',
        7, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (24, 5, '5d5c57ab443f5fbb.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAbNFZAADi9nT5SuM524.jpg',
        8, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (25, 5, 'cef3c55b8caad783.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAMq2nAAGtjwY17fA932.jpg',
        9, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (26, 5, '6eaaecc91b9ad059.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAXjRKAAFpxKwrSvY886.jpg',
        10, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (27, 5, 'b7bea7af48e935fd.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqARA19AAFuZ18W_ks439.jpg',
        11, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (28, 6, '2b78b6fdabfd2fbe.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rgJqAHPnoAAF9hoDNfsc505.jpg',
        7, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (29, 6, '5d5c57ab443f5fbb.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAbNFZAADi9nT5SuM524.jpg',
        8, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (30, 6, 'cef3c55b8caad783.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAMq2nAAGtjwY17fA932.jpg',
        9, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (31, 6, '6eaaecc91b9ad059.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAXjRKAAFpxKwrSvY886.jpg',
        10, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (32, 6, 'b7bea7af48e935fd.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqARA19AAFuZ18W_ks439.jpg',
        11, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (33, 7, '2b78b6fdabfd2fbe.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rgJqAHPnoAAF9hoDNfsc505.jpg',
        7, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (34, 7, '5d5c57ab443f5fbb.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAbNFZAADi9nT5SuM524.jpg',
        8, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (35, 7, 'cef3c55b8caad783.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAMq2nAAGtjwY17fA932.jpg',
        9, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (36, 7, '6eaaecc91b9ad059.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAXjRKAAFpxKwrSvY886.jpg',
        10, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (37, 7, 'b7bea7af48e935fd.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqARA19AAFuZ18W_ks439.jpg',
        11, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (38, 8, '7155bba4c363065f.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAVRWzAABUiOmA0ic932.jpg',
        12, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (39, 8, '2689bc534d570eaf.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAO2oYAAEw9kY2VKk982.jpg',
        13, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (40, 8, '7ae59d1d962f0965.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAFeQLAAEt9MLZnho584.jpg',
        16, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (41, 8, 'f73bfe30f5ec641a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWABhwlAAEjBwwVkrI735.jpg',
        18, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (42, 9, '2689bc534d570eaf.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAO2oYAAEw9kY2VKk982.jpg',
        13, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (43, 9, '6ef342197c8095b6.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAJllcAAEY0AkXL8M782.jpg',
        14, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (44, 9, '7ae59d1d962f0965.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAFeQLAAEt9MLZnho584.jpg',
        16, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (45, 9, 'f73bfe30f5ec641a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWABhwlAAEjBwwVkrI735.jpg',
        18, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (46, 10, '2689bc534d570eaf.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAO2oYAAEw9kY2VKk982.jpg',
        13, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (47, 10, '34c390fe3ab2bab5.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAbqkuAAENKBtJukQ551.jpg',
        15, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (48, 10, '7ae59d1d962f0965.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAFeQLAAEt9MLZnho584.jpg',
        16, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (49, 10, 'f73bfe30f5ec641a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWABhwlAAEjBwwVkrI735.jpg',
        18, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (50, 11, '2689bc534d570eaf.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAO2oYAAEw9kY2VKk982.jpg',
        13, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (51, 11, '7ae59d1d962f0965.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAFeQLAAEt9MLZnho584.jpg',
        16, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (52, 11, 'de33680f921e5838.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWASR1YAADsOUYB-2g312.jpg',
        17, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (53, 11, 'f73bfe30f5ec641a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWABhwlAAEjBwwVkrI735.jpg',
        18, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (54, 12, '2689bc534d570eaf.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAO2oYAAEw9kY2VKk982.jpg',
        13, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (55, 12, '7ae59d1d962f0965.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAFeQLAAEt9MLZnho584.jpg',
        16, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (56, 12, 'f73bfe30f5ec641a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWABhwlAAEjBwwVkrI735.jpg',
        18, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (57, 12, '7155bba4c363065f.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAVRWzAABUiOmA0ic932.jpg',
        12, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (58, 13, '19b35dc3ebe1579e.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAQwdLAACW7swImE4752.jpg',
        19, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (59, 13, '1009958cd1bc4e70.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAUJH9AACHXa0HPC8315.jpg',
        20, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (60, 13, '76c7922bb9d226d0.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAPVqkAAEoiSa9WoM463.jpg',
        21, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (61, 13, '9316593be50948f8.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaALrngAAHGDqdpFtU741.jpg',
        22, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (62, 13, 'ee11befc0d6dfa18.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleASDLsAAFcVo0uNCs962.jpg',
        24, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (63, 13, 'fa4ffba88e29ee03.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAJ6zNAADSblcDDEM109.jpg',
        25, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (64, 13, 'a01d74c9878967fa.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAa3edAAKUHkq4s24909.jpg',
        26, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (65, 14, '19b35dc3ebe1579e.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAQwdLAACW7swImE4752.jpg',
        19, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (66, 14, '1009958cd1bc4e70.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAUJH9AACHXa0HPC8315.jpg',
        20, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (67, 14, '76c7922bb9d226d0.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAPVqkAAEoiSa9WoM463.jpg',
        21, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (68, 14, '89e57f95b32e5385.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAbYPbAAHJf20K7J4980.jpg',
        23, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (69, 14, 'ee11befc0d6dfa18.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleASDLsAAFcVo0uNCs962.jpg',
        24, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (70, 14, 'fa4ffba88e29ee03.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAJ6zNAADSblcDDEM109.jpg',
        25, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (71, 14, 'a01d74c9878967fa.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAa3edAAKUHkq4s24909.jpg',
        26, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (72, 15, '19b35dc3ebe1579e.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAQwdLAACW7swImE4752.jpg',
        19, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (73, 15, '1009958cd1bc4e70.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAUJH9AACHXa0HPC8315.jpg',
        20, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (74, 15, '76c7922bb9d226d0.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAPVqkAAEoiSa9WoM463.jpg',
        21, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (75, 15, '89e57f95b32e5385.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAbYPbAAHJf20K7J4980.jpg',
        23, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (76, 15, 'ee11befc0d6dfa18.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleASDLsAAFcVo0uNCs962.jpg',
        24, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (77, 15, 'fa4ffba88e29ee03.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAJ6zNAADSblcDDEM109.jpg',
        25, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (78, 15, 'a01d74c9878967fa.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAa3edAAKUHkq4s24909.jpg',
        26, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (79, 16, '19b35dc3ebe1579e.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAQwdLAACW7swImE4752.jpg',
        19, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (80, 16, '1009958cd1bc4e70.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAUJH9AACHXa0HPC8315.jpg',
        20, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (81, 16, '76c7922bb9d226d0.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAPVqkAAEoiSa9WoM463.jpg',
        21, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (82, 16, '9316593be50948f8.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaALrngAAHGDqdpFtU741.jpg',
        22, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (83, 16, 'ee11befc0d6dfa18.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleASDLsAAFcVo0uNCs962.jpg',
        24, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (84, 16, 'fa4ffba88e29ee03.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAJ6zNAADSblcDDEM109.jpg',
        25, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (85, 16, 'a01d74c9878967fa.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAa3edAAKUHkq4s24909.jpg',
        26, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (86, 17, '23e94e5f9fa168d7.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAaz7cAACS1bFmjlE652.jpg',
        27, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (87, 17, '8ea8ac1e43eb09bc.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAe9mBAAHubDHNM_s207.jpg',
        29, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (88, 17, '44b81ee60ba37250.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-ARs7SAAK2xlc5Kew601.jpg',
        31, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (89, 17, 'ed289ba23e865e31.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-AN7-lAAJRUqAcXEI304.jpg',
        32, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (90, 17, 'bae6e6a540c68c48.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAWr6DAAOBwhDxkRg939.jpg',
        33, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (91, 17, 'd37bc807dd3080d6.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAcfXYAAOtpRUCgAc311.jpg',
        34, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (92, 17, 'b978ec45035aa218.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAFTPcAAM3hhhj828508.jpg',
        35, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (93, 17, 'f496d9ae34b76554.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3GAUIstAAMFiaVe0I4100.jpg',
        36, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (94, 18, '23e94e5f9fa168d7.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAaz7cAACS1bFmjlE652.jpg',
        27, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (95, 18, '5f679f4a7990fffb.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAAHK_AAHxOsbi0Gc462.jpg',
        28, '1', '2021-12-14 00:00:00', null);
insert into sku_image
values (96, 18, '44b81ee60ba37250.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-ARs7SAAK2xlc5Kew601.jpg',
        31, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (97, 18, 'ed289ba23e865e31.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-AN7-lAAJRUqAcXEI304.jpg',
        32, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (98, 18, 'bae6e6a540c68c48.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAWr6DAAOBwhDxkRg939.jpg',
        33, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (99, 18, 'd37bc807dd3080d6.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAcfXYAAOtpRUCgAc311.jpg',
        34, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (100, 18, 'b978ec45035aa218.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAFTPcAAM3hhhj828508.jpg', 35, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (101, 18, 'f496d9ae34b76554.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3GAUIstAAMFiaVe0I4100.jpg', 36, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (102, 19, '23e94e5f9fa168d7.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAaz7cAACS1bFmjlE652.jpg', 27, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (103, 19, 'ccaad675b92601b8.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-AU8esAAIV74ZBdhU344.jpg', 30, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (104, 19, '44b81ee60ba37250.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-ARs7SAAK2xlc5Kew601.jpg', 31, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (105, 19, 'ed289ba23e865e31.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-AN7-lAAJRUqAcXEI304.jpg', 32, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (106, 19, 'bae6e6a540c68c48.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAWr6DAAOBwhDxkRg939.jpg', 33, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (107, 19, 'd37bc807dd3080d6.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAcfXYAAOtpRUCgAc311.jpg', 34, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (108, 19, 'b978ec45035aa218.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAFTPcAAM3hhhj828508.jpg', 35, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (109, 19, 'f496d9ae34b76554.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3GAUIstAAMFiaVe0I4100.jpg', 36, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (110, 20, '1d06cce763319de9.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kH6AGdWUAADGjZ-bAuc105.jpg', 37, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (111, 20, '6057c618c32233d3.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kH6AIR2DAAB34EDXR8I868.jpg', 38, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (112, 20, 'b701596e43b3433b.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kH-AOqGjAABTm8Yp74U305.jpg', 40, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (113, 20, 'cc2d09a3feba8058.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIGAY1IuAADTekb4Aks567.jpg', 42, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (114, 20, 'a4eaf7bf9528fe4d.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIGAWtMyAAGxs6Q350k510.jpg', 43, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (115, 20, '9306232083ca53d6.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIGAY4cIAAHCbpsLG8Y072.jpg', 44, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (116, 20, 'a55bc2b7a3b0ecfb.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIKAC8WUAAGuYv8KYsE398.jpg', 47, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (117, 21, '6057c618c32233d3.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kH6AIR2DAAB34EDXR8I868.jpg', 38, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (118, 21, '1eabe76b0f15b0d8.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kH6AQb87AAJYDnKvZoU838.jpg', 39, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (119, 21, '1fffb98409fa32c0.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kICAaGuxAAKnO3DNDcY020.jpg', 41, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (120, 21, 'a55bc2b7a3b0ecfb.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIKAC8WUAAGuYv8KYsE398.jpg', 47, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (121, 21, '21401b8a2c2b38f1.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIKAa4cXAAJ021_HJN8583.jpg', 45, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (122, 21, '42ed4e6655d2acca.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIKAMJkPAAJdKCVoSR0812.jpg', 46, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (123, 22, '4a5fc6ff3ea986e9 (1).jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0lieAGQHUAAIiC_lx9cU417.jpg', 48, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (124, 22, '6e82f1a4475f871e.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liqALXl6AAOvXBZbBYs429.jpg', 49, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (125, 22, 'cc2d09a3feba8058.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liqAARz7AAHeAIWIl4I126.jpg', 51, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (126, 22, '8d83227b75119532.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liqAE9CSAAIUaEugX8E823.jpg', 52, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (127, 22, '31bd117f36197b9d.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liuAZ1P_AALOZHDbvCM585.jpg', 54, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (128, 22, 'e26709c6dbd6a1fe.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0li2AZLT5AAMhohWBIMs183.jpg', 57, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (129, 23, '4a5fc6ff3ea986e9 (1).jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0lieAGQHUAAIiC_lx9cU417.jpg', 48, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (130, 23, '8d83227b75119532.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liqAE9CSAAIUaEugX8E823.jpg', 52, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (131, 23, '31bd117f36197b9d.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liuAZ1P_AALOZHDbvCM585.jpg', 54, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (132, 23, 'ed854afc5bb54697.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liyAJ34AAAJLREFgZVM767.jpg', 55, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (133, 23, '0490b051476c112e.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liuAJTluAAVP1d_tXYs725.jpg', 53, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (134, 24, '5b73a35dN94a5e30a.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l7aADmXLAAI5tpjy5CI066.jpg', 58, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (135, 24, '5b73a36dNd0a67203.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l7yAfFv9AAM5ZEY69Uo453.jpg', 59, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (136, 24, '5b73a35aN92891309.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l72AKuQVAALmOIO3U5M856.jpg', 62, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (137, 24, '5b73a362Nc6b5f3fb.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l76AKjn2AAlz4fZOF_8339.jpg', 63, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (138, 25, '5b73a36dNd0a67203.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l7yAfFv9AAM5ZEY69Uo453.jpg', 59, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (139, 25, 'c035c2acf72e5ff1.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l7yALvPlAAO4xZsGHFI059.jpg', 60, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (140, 25, '5cdf66beN8aa239ab.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l72AaH20AATmWw3ydsA295.jpg', 61, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (141, 25, '5b73a362Nc6b5f3fb (1).jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l7-AVJfOAAlz4fZOF_8230.jpg', 64, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (142, 26, '7ffd8d2a4be62085.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAZ6jBAAGu7qTDWVA490.jpg', 65, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (143, 26, 'c406559b05bcf6d4.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAc7geAAFOkBl0eCU984.jpg', 66, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (144, 26, '7496d660c45c45ac.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAbtKiAAFs7t6eSJ0508.jpg', 67, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (145, 26, 'f8051c8538cb011e.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAC5dfAAH_Rtwwzq8880.jpg', 68, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (146, 26, 'b28620aae9d31c52.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yciAPvJGAARhSl8kZA8647.png', 69, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (147, 27, '7ffd8d2a4be62085.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAZ6jBAAGu7qTDWVA490.jpg', 65, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (148, 27, 'c406559b05bcf6d4.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAc7geAAFOkBl0eCU984.jpg', 66, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (149, 27, '7496d660c45c45ac.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAbtKiAAFs7t6eSJ0508.jpg', 67, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (150, 27, 'f8051c8538cb011e.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAC5dfAAH_Rtwwzq8880.jpg', 68, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (151, 27, 'b28620aae9d31c52.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yciAPvJGAARhSl8kZA8647.png', 69, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (152, 28, '7ffd8d2a4be62085.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAZ6jBAAGu7qTDWVA490.jpg', 65, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (153, 28, 'c406559b05bcf6d4.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAc7geAAFOkBl0eCU984.jpg', 66, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (154, 28, '7496d660c45c45ac.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAbtKiAAFs7t6eSJ0508.jpg', 67, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (155, 28, 'f8051c8538cb011e.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAC5dfAAH_Rtwwzq8880.jpg', 68, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (156, 28, 'b28620aae9d31c52.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yciAPvJGAARhSl8kZA8647.png', 69, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (157, 29, '72cec68481f86aff.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1WATxItAAEcZnKxvfI617.jpg', 70, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (158, 29, '1b462be0fb148e88.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1WAKv_cAAHKVw8AZqk151.jpg', 71, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (159, 29, 'dcc198936a4601de.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1eAS25WAAEYg9IP_7o495.jpg', 73, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (160, 29, '1057db3d2a4deea2.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iAAXYvAAGZqARg5F4191.jpg', 74, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (161, 29, 'bb4a19c813f7e61e.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iAaMWAAANMuaHHijI678.png', 75, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (162, 29, '8c35313dfcbccf2a.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iADJZ_AAIz437wUUc659.jpg', 76, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (163, 29, '0ed0cf1bb387059b.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1mAcqDEAAVe-gtfew4145.png', 77, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (164, 30, '1b462be0fb148e88.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1WAKv_cAAHKVw8AZqk151.jpg', 71, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (165, 30, '507a23898221cd6a.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1eASPU7AAEiYRrkMww103.jpg', 72, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (166, 30, '1057db3d2a4deea2.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iAAXYvAAGZqARg5F4191.jpg', 74, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (167, 30, 'bb4a19c813f7e61e.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iAaMWAAANMuaHHijI678.png', 75, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (168, 30, '8c35313dfcbccf2a.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iADJZ_AAIz437wUUc659.jpg', 76, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (169, 30, '0ed0cf1bb387059b.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1mAcqDEAAVe-gtfew4145.png', 77, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (170, 31, '72cec68481f86aff.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1WATxItAAEcZnKxvfI617.jpg', 70, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (171, 31, '1b462be0fb148e88.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1WAKv_cAAHKVw8AZqk151.jpg', 71, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (172, 31, '1057db3d2a4deea2.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iAAXYvAAGZqARg5F4191.jpg', 74, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (173, 31, 'bb4a19c813f7e61e.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iAaMWAAANMuaHHijI678.png', 75, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (174, 31, '8c35313dfcbccf2a.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iADJZ_AAIz437wUUc659.jpg', 76, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (175, 31, '0ed0cf1bb387059b.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1mAcqDEAAVe-gtfew4145.png', 77, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (176, 32, '53f744c57c9bed0d.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MKAbhV8AACzhzshAss449.jpg', 79, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (177, 32, '09ee8484ac136e01.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MKAXnZ9AAExlZ_f0b0308.jpg', 80, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (178, 32, 'a4a448f9df8c715a.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAEXECAAFZJnPg5O0915.jpg', 84, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (179, 32, 'a4a448f9df8c715a (1).jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAe1vIAAFZJnPg5O0004.jpg', 86, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (180, 32, 'd6fb7d2f6cb06195.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MWAfxwgAAD8jFUkfao175.jpg', 87, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (181, 33, '5ad5104b7cff69f6.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MKAcQ0_AAGxbDKQSm0286.jpg', 78, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (182, 33, '196d96f59897cf39.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSABFB2AAHD3bWoRhw015.jpg', 82, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (183, 33, '6cc3723538c7f7b3.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAPFONAAGchseVkoM398.jpg', 83, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (184, 33, 'a4a448f9df8c715a.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAEXECAAFZJnPg5O0915.jpg', 84, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (185, 33, '374b25b22e90ed74.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAe9k4AAINKcLONPQ919.jpg', 85, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (186, 34, '4cd12718fd5e1bd7.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AeAd45VAAF1GK3U-NE661.jpg', 88, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (187, 34, 'a61a13eb7e3489f1.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AeASZitAAFcbBnUWrw650.jpg', 89, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (188, 34, 'c7b173293ee66929.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AuAIVVAAAFjH-WR0oA236.jpg', 92, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (189, 34, '4e9461a5b6e0136f.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AyARcFFAAKGCeWL410100.jpg', 94, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (190, 34, 'b33f63b0a7fab02d.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02A2Ae-VYAAbQwOM632g076.png', 95, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (191, 34, 'b526433a4d9e51ca.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02A2AXG14AAY1E5sugTg523.jpg', 96, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (192, 35, '0be857e07965a67e.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 90, '1', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (193, 35, 'b104fa8eec6f6de6.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AuAfizUAAKkARuK5vg313.jpg', 91, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (194, 35, '64332079e66a291c.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AyAGFZzAAMnSgOWLUo218.jpg', 93, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (195, 35, 'b33f63b0a7fab02d.png',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02A2Ae-VYAAbQwOM632g076.png', 95, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (196, 35, 'a61a13eb7e3489f1.jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AeASZitAAFcbBnUWrw650.jpg', 89, '0', '2021-12-14 00:00:00',
        null);
insert into sku_image
values (197, 36, '1.jpg', '/data/images/36/1.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (198, 36, '2.jpg', '/data/images/36/2.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (199, 36, '3.jpg', '/data/images/36/3.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (200, 36, '4.jpg', '/data/images/36/4.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (201, 36, '5.jpg', '/data/images/36/5.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (202, 36, '6.jpg', '/data/images/36/6.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (203, 36, '7.jpg', '/data/images/36/7.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (204, 36, '8.jpg', '/data/images/36/8.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (205, 36, '9.jpg', '/data/images/36/9.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (206, 36, '10.jpg', '/data/images/36/10.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (207, 36, '11.jpg', '/data/images/36/11.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (208, 36, '12.jpg', '/data/images/36/12.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (209, 36, '13.jpg', '/data/images/36/13.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (210, 36, '14.jpg', '/data/images/36/14.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (211, 36, '15.jpg', '/data/images/36/15.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (212, 36, '16.jpg', '/data/images/36/16.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (213, 36, '17.jpg', '/data/images/36/17.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (214, 37, '1.jpg', '/data/images/37/1.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (215, 37, '2.jpg', '/data/images/37/2.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (216, 37, '3.jpg', '/data/images/37/3.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (217, 37, '4.jpg', '/data/images/37/4.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (218, 38, '1.jpg', '/data/images/38/1.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (219, 38, '2.jpg', '/data/images/38/2.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (220, 38, '3.jpg', '/data/images/38/3.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (221, 39, '1.jpg', '/data/images/39/1.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (222, 39, '2.jpg', '/data/images/39/2.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (223, 39, '3.jpg', '/data/images/39/3.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (224, 39, '4.jpg', '/data/images/39/4.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (225, 39, '5.jpg', '/data/images/39/5.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (226, 39, '6.jpg', '/data/images/39/6.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (227, 40, '1.jpg', '/data/images/40/1.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (228, 40, '2.jpg', '/data/images/40/2.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (229, 40, '3.jpg', '/data/images/40/3.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (230, 40, '4.jpg', '/data/images/40/4.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (231, 40, '5.jpg', '/data/images/40/5.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (232, 40, '6.jpg', '/data/images/40/6.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (233, 41, '1.jpg', '/data/images/41/1.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (234, 41, '2.jpg', '/data/images/41/2.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (235, 41, '3.jpg', '/data/images/41/3.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (236, 41, '4.jpg', '/data/images/41/4.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (237, 42, '1.jpg', '/data/images/42/1.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (238, 42, '2.jpg', '/data/images/42/2.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (239, 42, '3.jpg', '/data/images/42/3.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (240, 42, '4.jpg', '/data/images/42/4.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (241, 43, '1.jpg', '/data/images/43/1.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (242, 43, '2.jpg', '/data/images/43/2.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (243, 43, '3.jpg', '/data/images/43/3.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (244, 43, '4.jpg', '/data/images/43/4.jpg', 89, '0', '2021-12-14 00:00:00', null);
insert into sku_image
values (245, 43, '5.jpg', '/data/images/43/5.jpg', 89, '0', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for sku_info
-- ----------------------------
drop table if exists sku_info;
create table if not exists sku_info
(
    id              bigint         not null auto_increment comment 'skuid',
    spu_id          bigint         null     default null comment 'spuid',
    price           decimal(10, 0) null     default null comment '价格',
    sku_name        varchar(200)   null     default null comment 'sku名称',
    sku_desc        varchar(2000)  null     default null comment '商品规格描述',
    weight          decimal(10, 2) null     default null comment '重量',
    tm_id           bigint         null     default null comment '品牌id(冗余)',
    category3_id    bigint         null     default null comment '三级品类id（冗余)',
    sku_default_img varchar(300)   null     default null comment '默认显示图片地址(冗余)',
    is_sale         tinyint        not null default 0 comment '是否在售（1：是 0：否）',
    create_time     datetime       null     default null comment '创建时间',
    operate_time    datetime       null     default null comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 44
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = 'sku表'
  row_format = dynamic;

-- ----------------------------
-- Records of sku_info
-- ----------------------------
insert into sku_info
values (1, 1, 6999, '小米12S Ultra 骁龙8+旗舰处理器 徕卡光学镜头 2K超视感屏 120Hz高刷 67W快充 8GB+128GB 冷杉绿 5G手机',
        '小米12S Ultra 骁龙8+旗舰处理器 徕卡光学镜头 2K超视感屏 120Hz高刷 67W快充 8GB+128GB 冷杉绿 5G手机', 1.00, 5, 61,
        'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAIpgZAAIvrX6L9fo612.jpg', 1, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (2, 1, 6999, '小米12S Ultra 骁龙8+旗舰处理器 徕卡光学镜头 2K超视感屏 120Hz高刷 67W快充 8GB+256GB 经典黑 5G手机',
        '小米12S Ultra 骁龙8+旗舰处理器 徕卡光学镜头 2K超视感屏 120Hz高刷 67W快充 8GB+256GB 经典黑 5G手机', 1.00, 5, 61,
        'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAcbl2AAFopp2WGBQ404.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (3, 1, 6499, '小米12S Ultra 骁龙8+旗舰处理器 徕卡光学镜头 2K超视感屏 120Hz高刷 67W快充 8GB+128GB 经典黑 5G手机',
        '小米12S Ultra 骁龙8+旗舰处理器 徕卡光学镜头 2K超视感屏 120Hz高刷 67W快充 8GB+128GB 经典黑 5G手机', 1.00, 5, 61,
        'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAIpgZAAIvrX6L9fo612.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (4, 2, 999,
        'Redmi 10X 4G Helio G85游戏芯 4800万超清四摄 5020mAh大电量 小孔全面屏 128GB大存储 4GB+128GB 冰雾白 游戏智能手机 小米 红米',
        'Redmi 10X 4G Helio G85游戏芯 4800万超清四摄 5020mAh大电量 小孔全面屏 128GB大存储 4GB+128GB 冰雾白 游戏智能手机 小米 红米',
        1.00, 1, 61, 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rgJqAHPnoAAF9hoDNfsc505.jpg', 0,
        '2021-12-14 00:00:00', null);
insert into sku_info
values (5, 2, 999,
        'Redmi 10X 4G Helio G85游戏芯 4800万超清四摄 5020mAh大电量 小孔全面屏 128GB大存储 4GB+128GB 明月灰 游戏智能手机 小米 红米',
        'Redmi 10X 4G Helio G85游戏芯 4800万超清四摄 5020mAh大电量 小孔全面屏 128GB大存储 4GB+128GB 明月灰 游戏智能手机 小米 红米',
        1.00, 1, 61, 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rgJqAHPnoAAF9hoDNfsc505.jpg', 0,
        '2021-12-14 00:00:00', null);
insert into sku_info
values (6, 2, 1299,
        'Redmi 10X 4G Helio G85游戏芯 4800万超清四摄 5020mAh大电量 小孔全面屏 128GB大存储 8GB+128GB 冰雾白 游戏智能手机 小米 红米',
        'Redmi 10X 4G Helio G85游戏芯 4800万超清四摄 5020mAh大电量 小孔全面屏 128GB大存储 8GB+128GB 冰雾白 游戏智能手机 小米 红米',
        1.00, 1, 61, 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rgJqAHPnoAAF9hoDNfsc505.jpg', 0,
        '2021-12-14 00:00:00', null);
insert into sku_info
values (7, 2, 1299,
        'Redmi 10X 4G Helio G85游戏芯 4800万超清四摄 5020mAh大电量 小孔全面屏 128GB大存储 8GB+128GB 明月灰 游戏智能手机 小米 红米',
        'Redmi 10X 4G Helio G85游戏芯 4800万超清四摄 5020mAh大电量 小孔全面屏 128GB大存储 8GB+128GB 明月灰 游戏智能手机 小米 红米',
        1.00, 1, 61, 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rgJqAHPnoAAF9hoDNfsc505.jpg', 1,
        '2021-12-14 00:00:00', null);
insert into sku_info
values (8, 3, 8197, 'Apple iPhone 12 (A2404) 64GB 黑色 支持移动联通电信5G 双卡双待手机',
        'Apple iPhone 12 (A2404) 64GB 黑色 支持移动联通电信5G 双卡双待手机', 1.00, 2, 61,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAVRWzAABUiOmA0ic932.jpg', 1, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (9, 3, 8197, 'Apple iPhone 12 (A2404) 64GB 红色 支持移动联通电信5G 双卡双待手机',
        'Apple iPhone 12 (A2404) 64GB 红色 支持移动联通电信5G 双卡双待手机', 1.00, 2, 61,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAJllcAAEY0AkXL8M782.jpg', 1, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (10, 3, 8197, 'Apple iPhone 12 (A2404) 64GB 蓝色 支持移动联通电信5G 双卡双待手机',
        'Apple iPhone 12 (A2404) 64GB 蓝色 支持移动联通电信5G 双卡双待手机', 1.00, 2, 61,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAbqkuAAENKBtJukQ551.jpg', 1, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (11, 3, 8197, 'Apple iPhone 12 (A2404) 64GB 白色 支持移动联通电信5G 双卡双待手机',
        'Apple iPhone 12 (A2404) 64GB 白色 支持移动联通电信5G 双卡双待手机', 1.00, 2, 61,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWASR1YAADsOUYB-2g312.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (12, 3, 9197, 'Apple iPhone 12 (A2404) 128GB 黑色 支持移动联通电信5G 双卡双待手机',
        'Apple iPhone 12 (A2404) 128GB 黑色 支持移动联通电信5G 双卡双待手机', 1.00, 2, 61,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAVRWzAABUiOmA0ic932.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (13, 4, 9899, '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑 i9-12900H RTX3060 钛晶灰',
        '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑 i9-12900H RTX3060 钛晶灰', 4.00, 3, 287,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaALrngAAHGDqdpFtU741.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (14, 4, 11999, '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑 i9-12900H RTX3070Ti 钛晶灰',
        '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑 i9-12900H RTX3070Ti 钛晶灰', 1.00, 3, 287,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAbYPbAAHJf20K7J4980.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (15, 4, 9799, '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑 i7-12700H 512G RTX3060 钛晶灰',
        '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑 i7-12700H 512G RTX3060 钛晶灰', 1.00, 3, 287,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAbYPbAAHJf20K7J4980.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (16, 4, 10599, '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑 i7-12700H RTX3060 冰魄白',
        '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑 i7-12700H RTX3060 冰魄白', 1.00, 3, 287,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaALrngAAHGDqdpFtU741.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (17, 5, 6699, 'TCL 65Q10 65英寸 QLED原色量子点电视 安桥音响 AI声控智慧屏 超薄全面屏 MEMC防抖 3+32GB 平板电视',
        'TCL 65Q10 65英寸 QLED原色量子点电视 安桥音响 AI声控智慧屏 超薄全面屏 MEMC防抖 3+32GB 平板电视', 23.00, 4, 86,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAe9mBAAHubDHNM_s207.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (18, 5, 9199, 'TCL 75Q10 75英寸 QLED原色量子点电视 安桥音响 AI声控智慧屏 超薄全面屏 MEMC防抖 3+32GB 平板电视',
        'TCL 75Q10 75英寸 QLED原色量子点电视 安桥音响 AI声控智慧屏 超薄全面屏 MEMC防抖 3+32GB 平板电视', 25.00, 4, 86,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAAHK_AAHxOsbi0Gc462.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (19, 5, 11999,
        'TCL 85Q6 85英寸 巨幕私人影院电视 4K超高清 AI智慧屏 全景全面屏 MEMC运动防抖 2+16GB 液晶平板电视机',
        'TCL 85Q6 85英寸 巨幕私人影院电视 4K超高清 AI智慧屏 全景全面屏 MEMC运动防抖 2+16GB 液晶平板电视机', 30.00, 4,
        86, 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-AU8esAAIV74ZBdhU344.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (20, 6, 2899,
        '小米电视E65X 65英寸 全面屏 4K超高清HDR 蓝牙遥控内置小爱 2+8GB AI人工智能液晶网络平板电视 L65M5-EA',
        '小米电视E65X 65英寸 全面屏 4K超高清HDR 蓝牙遥控内置小爱 2+8GB AI人工智能液晶网络平板电视 L65M5-EA', 23.00, 5,
        86, 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIGAWtMyAAGxs6Q350k510.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (21, 6, 3299, '小米电视4A 70英寸 4K超高清 HDR 二级能效 2GB+16GB L70M5-4A 内置小爱 智能网络液晶平板教育电视',
        '小米电视4A 70英寸 4K超高清 HDR 二级能效 2GB+16GB L70M5-4A 内置小爱 智能网络液晶平板教育电视', 28.00, 5, 86,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kICAaGuxAAKnO3DNDcY020.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (22, 7, 39, '十月稻田 长粒香大米 东北大米 东北香米 5kg', '十月稻田 长粒香大米 东北大米 东北香米 5kg', 5.00, 6,
        803, 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liqAARz7AAHeAIWIl4I126.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (23, 7, 40, '十月稻田 辽河长粒香 东北大米 5kg', '十月稻田 辽河长粒香 东北大米 5kg', 5.00, 6, 803,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liuAJTluAAVP1d_tXYs725.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (24, 8, 11, '金沙河面条 原味银丝挂面 龙须面 方便速食拉面 清汤面 900g',
        '金沙河面条 原味银丝挂面 龙须面 方便速食拉面 清汤面 900g', 0.90, 7, 803,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l72AKuQVAALmOIO3U5M856.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (25, 8, 23, '金沙河面条 银丝挂面900g*3包 爽滑 细面条 龙须面 速食面',
        '金沙河面条 银丝挂面900g*3包 爽滑 细面条 龙须面 速食面', 2.70, 7, 803,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l72AaH20AATmWw3ydsA295.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (26, 9, 129, '索芙特i-Softto 口红不掉色唇膏保湿滋润 璀璨金钻哑光唇膏 Y01复古红 百搭气质 璀璨金钻哑光唇膏 ',
        '索芙特i-Softto 口红不掉色唇膏保湿滋润 璀璨金钻哑光唇膏 Y01复古红 百搭气质 璀璨金钻哑光唇膏 ', 1.00, 8, 477,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAC5dfAAH_Rtwwzq8880.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (27, 9, 129, '索芙特i-Softto 口红不掉色唇膏保湿滋润 璀璨金钻哑光唇膏 Z02少女红 活力青春 璀璨金钻哑光唇膏 ',
        '索芙特i-Softto 口红不掉色唇膏保湿滋润 璀璨金钻哑光唇膏 Z02少女红 活力青春 璀璨金钻哑光唇膏 ', 1.00, 8, 477,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAC5dfAAH_Rtwwzq8880.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (28, 9, 129, '索芙特i-Softto 口红不掉色唇膏保湿滋润 璀璨金钻哑光唇膏 Z03女王红 性感冷艳 璀璨金钻哑光唇膏 ',
        '索芙特i-Softto 口红不掉色唇膏保湿滋润 璀璨金钻哑光唇膏 Z03女王红 性感冷艳 璀璨金钻哑光唇膏 ', 1.00, 8, 477,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAC5dfAAH_Rtwwzq8880.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (29, 10, 69, 'CAREMiLLE珂曼奶油小方口红 雾面滋润保湿持久丝缎唇膏 M01醉蔷薇',
        'CAREMiLLE珂曼奶油小方口红 雾面滋润保湿持久丝缎唇膏 M01醉蔷薇', 1.00, 9, 477,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1eAS25WAAEYg9IP_7o495.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (30, 10, 69, 'CAREMiLLE珂曼奶油小方口红 雾面滋润保湿持久丝缎唇膏 M02干玫瑰',
        'CAREMiLLE珂曼奶油小方口红 雾面滋润保湿持久丝缎唇膏 M02干玫瑰', 1.00, 9, 477,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1eASPU7AAEiYRrkMww103.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (31, 10, 69, 'CAREMiLLE珂曼奶油小方口红 雾面滋润保湿持久丝缎唇膏 M03赤茶',
        'CAREMiLLE珂曼奶油小方口红 雾面滋润保湿持久丝缎唇膏 M03赤茶', 1.00, 9, 477,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1WATxItAAEcZnKxvfI617.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (32, 11, 300, '香奈儿（Chanel）女士香水5号香水 粉邂逅柔情淡香水EDT 5号淡香水35ml',
        '香奈儿（Chanel）女士香水5号香水 粉邂逅柔情淡香水EDT 5号淡香水35ml', 1.00, 11, 473,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MKAbhV8AACzhzshAss449.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (33, 11, 488, '香奈儿（Chanel）女士香水5号香水 粉邂逅柔情淡香水EDT 粉邂逅淡香水35ml',
        '香奈儿（Chanel）女士香水5号香水 粉邂逅柔情淡香水EDT 粉邂逅淡香水35ml', 1.00, 11, 473,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSABFB2AAHD3bWoRhw015.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (34, 12, 3927, '华为智慧屏V55i-J 55英寸 HEGE-550B 4K全面屏智能电视机 多方视频通话 AI升降摄像头 银钻灰 京品家电',
        '华为智慧屏V55i-J 55英寸 HEGE-550B 4K全面屏智能电视机 多方视频通话 AI升降摄像头 银钻灰 京品家电', 30.00, 12, 86,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AyARcFFAAKGCeWL410100.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (35, 12, 5499, '华为智慧屏V65i 65英寸 HEGE-560B 4K全面屏智能电视机 多方视频通话 AI升降摄像头 4GB+32GB 星际黑',
        '华为智慧屏V65i 65英寸 HEGE-560B 4K全面屏智能电视机 多方视频通话 AI升降摄像头 4GB+32GB 星际黑', 35.00, 12, 86,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (36, 13, 3488,
        'HAWEIAI Book【补贴30%】2025英特尔14 Pro满血独显笔记本电脑轻薄本高端高性能金属游戏设计大学生【2.5K全面屏+抗蓝光+指纹】 32G内存+2TB超速硬盘',
        'HAWEIAI Book【补贴30%】2025英特尔14 Pro满血独显笔记本电脑轻薄本高端高性能金属游戏设计大学生【2.5K全面屏+抗蓝光+指纹】 32G内存+2TB超速硬盘',
        35.00, 12, 285, 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 0,
        '2021-12-14 00:00:00', null);
insert into sku_info
values (37, 14, 1229,
        '华为HUAWEI二手笔记本MateBook13触屏2K全面屏 便携二手笔记本电脑 Magic R5-2500-8G-256G-高分屏 95成新',
        '华为HUAWEI二手笔记本MateBook13触屏2K全面屏 便携二手笔记本电脑 Magic R5-2500-8G-256G-高分屏 95成新', 35.00, 12,
        285, 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (38, 15, 955,
        'H&U&W国行【2025新英特尔+酷睿i7】笔记本电脑轻薄本大学生办公便携高性能游戏本商务设计AI标压手提本 【15代14英寸】英特尔IPS护眼+9D蓝光全面屏 8G内存/128G超速硬盘',
        'H&U&W国行【2025新英特尔+酷睿i7】笔记本电脑轻薄本大学生办公便携高性能游戏本商务设计AI标压手提本 【15代14英寸】英特尔IPS护眼+9D蓝光全面屏 8G内存/128G超速硬盘',
        35.00, 13, 285, 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 0,
        '2021-12-14 00:00:00', null);
insert into sku_info
values (39, 16, 1437, 'vivo S20 8GB+256GB 凤羽金 国家补贴 6500mAh超薄长续航 5000万防畸变柔光自拍 拍照 AI 手机 送礼',
        'vivo S20 8GB+256GB 凤羽金 国家补贴 6500mAh超薄长续航 5000万防畸变柔光自拍 拍照 AI 手机 送礼', 35.00, 14, 61,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (40, 17, 1436,
        '小米【国家补贴】REDMI Turbo4 Pro 新品上市 小米手机 小米5G手机红米turbo 7550mAh长续航电池 白色 12GB+256GB',
        '小米【国家补贴】REDMI Turbo4 Pro 新品上市 小米手机 小米5G手机红米turbo 7550mAh长续航电池 白色 12GB+256GB', 35.00,
        1, 61, 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 0,
        '2021-12-14 00:00:00', null);
insert into sku_info
values (41, 18, 1999, '华为Mate 40 pro 5G全网通麒麟9000芯片鸿蒙国货NFC双卡游戏学生 黑色 8+128 送适用100w充电器',
        '华为Mate 40 pro 5G全网通麒麟9000芯片鸿蒙国货NFC双卡游戏学生 黑色 8+128 送适用100w充电器', 35.00, 12, 61,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (42, 19, 6961, 'Apple/苹果 iPhone 16 Pro（A3294）256GB 黑色钛金属 支持移动联通电信5G 双卡双待手机',
        'Apple/苹果 iPhone 16 Pro（A3294）256GB 黑色钛金属 支持移动联通电信5G 双卡双待手机', 35.00, 2, 61,
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 0, '2021-12-14 00:00:00',
        null);
insert into sku_info
values (43, 20, 2739,
        'OPPO【分期免息】Find X8手机 全网通5G双卡双待 AI拍照新机 Find X8浮光白 12GB+256GB 简配+全国联保+版本咨询客服',
        'OPPO【分期免息】Find X8手机 全网通5G双卡双待 AI拍照新机 Find X8浮光白 12GB+256GB 简配+全国联保+版本咨询客服',
        35.00, 15, 61, 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg', 0,
        '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for sku_sale_attr_value
-- ----------------------------
drop table if exists sku_sale_attr_value;
create table if not exists sku_sale_attr_value
(
    id                   bigint not null auto_increment comment '编号',
    sku_id               bigint comment 'sku_id',
    spu_id               int comment 'spu_id(冗余)',
    sale_attr_value_id   bigint comment '销售属性值id',
    sale_attr_id         bigint comment '销售属性id',
    sale_attr_name       varchar(30) comment '销售属性名称',
    sale_attr_value_name varchar(30) comment '销售属性值名称',
    create_time          datetime comment '创建时间',
    operate_time         datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 51
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = 'sku销售属性值表'
  row_format = dynamic;

-- ----------------------------
-- Records of sku_sale_attr_value
-- ----------------------------
insert into sku_sale_attr_value
values (1, 1, 1, 1, 1, '颜色', '冷杉绿', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (2, 1, 1, 4, 2, '版本', '8G+128G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (3, 2, 1, 2, 1, '颜色', '经典黑', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (4, 2, 1, 4, 2, '版本', '8G+256G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (5, 3, 1, 2, 1, '颜色', '经典黑', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (6, 3, 1, 3, 2, '版本', '8G+128G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (7, 4, 2, 5, 1, '颜色', '冰雾白', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (8, 4, 2, 7, 2, '版本', '4G+128G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (9, 5, 2, 6, 1, '颜色', '明月灰', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (10, 5, 2, 7, 2, '版本', '4G+128G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (11, 6, 2, 5, 1, '颜色', '冰雾白', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (12, 6, 2, 8, 2, '版本', '8G+128G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (13, 7, 2, 6, 1, '颜色', '明月灰', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (14, 7, 2, 8, 2, '版本', '8G+128G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (15, 8, 3, 9, 1, '颜色', '黑色', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (16, 8, 3, 13, 2, '版本', '64G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (17, 9, 3, 10, 1, '颜色', '红色', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (18, 9, 3, 13, 2, '版本', '64G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (19, 10, 3, 11, 1, '颜色', '蓝色', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (20, 10, 3, 13, 2, '版本', '64G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (21, 11, 3, 12, 1, '颜色', '白色', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (22, 11, 3, 13, 2, '版本', '64G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (23, 12, 3, 9, 1, '颜色', '黑色', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (24, 12, 3, 14, 2, '版本', '128G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (25, 13, 4, 15, 5, '处理器或内存', 'i9-12700H 512G RTX3060 灰', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (27, 14, 4, 16, 5, '处理器或内存', 'i9-12700H 512G RTX3070Ti 灰', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (29, 15, 4, 17, 5, '处理器或内存', 'i7-12700H 512G RTX3060 灰', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (31, 16, 4, 18, 5, '处理器或内存', 'i7-12700H 512G+2T RTX3060 白', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (33, 17, 5, 19, 3, '尺码', '65英寸', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (34, 18, 5, 20, 3, '尺码', '75英寸', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (35, 19, 5, 21, 3, '尺码', '85英寸', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (36, 20, 6, 22, 3, '尺码', '65英寸', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (37, 21, 6, 23, 3, '尺码', '70英寸', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (38, 22, 7, 24, 4, '类别', '长粒香大米5KG', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (39, 23, 7, 25, 4, '类别', '辽河长粒香5KG', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (40, 24, 8, 26, 4, '类别', '900G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (41, 25, 8, 27, 4, '类别', '3*900G', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (42, 26, 9, 28, 4, '类别', 'Y01复古红 百搭气质', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (43, 27, 9, 29, 4, '类别', 'Z02少女红 活力青春', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (44, 28, 9, 30, 4, '类别', 'Z03女王红 性感冷艳', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (45, 29, 10, 31, 4, '类别', 'M01醉蔷薇', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (46, 30, 10, 32, 4, '类别', 'M02干玫瑰', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (47, 31, 10, 33, 4, '类别', 'M03赤茶', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (48, 32, 11, 34, 4, '类别', '5号淡香水35ml', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (49, 33, 11, 35, 4, '类别', '5号粉邂逅淡香水35ml', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (50, 34, 12, 36, 3, '尺码', '55英寸', '2021-12-14 00:00:00', null);
insert into sku_sale_attr_value
values (51, 35, 12, 37, 3, '尺码', '65英寸', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for spu_image
-- ----------------------------
drop table if exists spu_image;
create table if not exists spu_image
(
    id           bigint not null auto_increment comment '编号',
    spu_id       bigint comment '商品id',
    img_name     varchar(200) comment '图片名称',
    img_url      varchar(300) comment '图片路径',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 97
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = 'spu图片表'
  row_format = dynamic;

-- ----------------------------
-- Records of spu_image
-- ----------------------------
insert into spu_image
values (1, 1, '2ff0882c9607e57c.jpg2', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAIpgZAAIvrX6L9fo612.jpg',
        null, null);
insert into spu_image
values (2, 1, 'ead186426badb626.jpg3', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAHpFuAACTenfIJWo734.jpg',
        null, null);
insert into spu_image
values (3, 1, 'b58ab2d79b859f39.jpg3', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAcbl2AAFopp2WGBQ404.jpg',
        null, null);
insert into spu_image
values (4, 1, '0d93a071c839d890.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmATs5EAABriLbF9vE207.jpg',
        null, null);
insert into spu_image
values (5, 1, 'a7b1125239354d0d.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAeWopAAEtpBjP1VQ788.jpg',
        null, null);
insert into spu_image
values (6, 1, '6029cb2c2b2c7668.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rfvmAZJX2AAGmVo8Tz9s683.jpg',
        null, null);
insert into spu_image
values (7, 2, '2b78b6fdabfd2fbe.jpg', 'http://47.93.148.192:8080/group1/M00/00/01/rBHu8l-rgJqAHPnoAAF9hoDNfsc505.jpg',
        null, null);
insert into spu_image
values (8, 2, '5d5c57ab443f5fbb.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAbNFZAADi9nT5SuM524.jpg',
        null, null);
insert into spu_image
values (9, 2, 'cef3c55b8caad783.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAMq2nAAGtjwY17fA932.jpg',
        null, null);
insert into spu_image
values (10, 2, '6eaaecc91b9ad059.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqAXjRKAAFpxKwrSvY886.jpg',
        null, null);
insert into spu_image
values (11, 2, 'b7bea7af48e935fd.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgJqARA19AAFuZ18W_ks439.jpg',
        null, null);
insert into spu_image
values (12, 3, '7155bba4c363065f.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAVRWzAABUiOmA0ic932.jpg',
        null, null);
insert into spu_image
values (13, 3, '2689bc534d570eaf.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAO2oYAAEw9kY2VKk982.jpg',
        null, null);
insert into spu_image
values (14, 3, '6ef342197c8095b6.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAJllcAAEY0AkXL8M782.jpg',
        null, null);
insert into spu_image
values (15, 3, '34c390fe3ab2bab5.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAbqkuAAENKBtJukQ551.jpg',
        null, null);
insert into spu_image
values (16, 3, '7ae59d1d962f0965.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWAFeQLAAEt9MLZnho584.jpg',
        null, null);
insert into spu_image
values (17, 3, 'de33680f921e5838.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWASR1YAADsOUYB-2g312.jpg',
        null, null);
insert into spu_image
values (18, 3, 'f73bfe30f5ec641a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-rgfWABhwlAAEjBwwVkrI735.jpg',
        null, null);
insert into spu_image
values (19, 4, '19b35dc3ebe1579e.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAQwdLAACW7swImE4752.jpg',
        null, null);
insert into spu_image
values (20, 4, '1009958cd1bc4e70.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklWAUJH9AACHXa0HPC8315.jpg',
        null, null);
insert into spu_image
values (21, 4, '76c7922bb9d226d0.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAPVqkAAEoiSa9WoM463.jpg',
        null, null);
insert into spu_image
values (22, 4, '9316593be50948f8.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaALrngAAHGDqdpFtU741.jpg',
        null, null);
insert into spu_image
values (23, 4, '89e57f95b32e5385.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-sklaAbYPbAAHJf20K7J4980.jpg',
        null, null);
insert into spu_image
values (24, 4, 'ee11befc0d6dfa18.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleASDLsAAFcVo0uNCs962.jpg',
        null, null);
insert into spu_image
values (25, 4, 'fa4ffba88e29ee03.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAJ6zNAADSblcDDEM109.jpg',
        null, null);
insert into spu_image
values (26, 4, 'a01d74c9878967fa.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-skleAa3edAAKUHkq4s24909.jpg',
        null, null);
insert into spu_image
values (27, 5, '23e94e5f9fa168d7.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAaz7cAACS1bFmjlE652.jpg',
        null, null);
insert into spu_image
values (28, 5, '5f679f4a7990fffb.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAAHK_AAHxOsbi0Gc462.jpg',
        null, null);
insert into spu_image
values (29, 5, '8ea8ac1e43eb09bc.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2uAe9mBAAHubDHNM_s207.jpg',
        null, null);
insert into spu_image
values (30, 5, 'ccaad675b92601b8.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-AU8esAAIV74ZBdhU344.jpg',
        null, null);
insert into spu_image
values (31, 5, '44b81ee60ba37250.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-ARs7SAAK2xlc5Kew601.jpg',
        null, null);
insert into spu_image
values (32, 5, 'ed289ba23e865e31.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i2-AN7-lAAJRUqAcXEI304.jpg',
        null, null);
insert into spu_image
values (33, 5, 'bae6e6a540c68c48.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAWr6DAAOBwhDxkRg939.jpg',
        null, null);
insert into spu_image
values (34, 5, 'd37bc807dd3080d6.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAcfXYAAOtpRUCgAc311.jpg',
        null, null);
insert into spu_image
values (35, 5, 'b978ec45035aa218.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3CAFTPcAAM3hhhj828508.jpg',
        null, null);
insert into spu_image
values (36, 5, 'f496d9ae34b76554.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0i3GAUIstAAMFiaVe0I4100.jpg',
        null, null);
insert into spu_image
values (37, 6, '1d06cce763319de9.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kH6AGdWUAADGjZ-bAuc105.jpg',
        null, null);
insert into spu_image
values (38, 6, '6057c618c32233d3.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kH6AIR2DAAB34EDXR8I868.jpg',
        null, null);
insert into spu_image
values (39, 6, '1eabe76b0f15b0d8.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kH6AQb87AAJYDnKvZoU838.jpg',
        null, null);
insert into spu_image
values (40, 6, 'b701596e43b3433b.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kH-AOqGjAABTm8Yp74U305.jpg',
        null, null);
insert into spu_image
values (41, 6, '1fffb98409fa32c0.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kICAaGuxAAKnO3DNDcY020.jpg',
        null, null);
insert into spu_image
values (42, 6, 'cc2d09a3feba8058.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIGAY1IuAADTekb4Aks567.jpg',
        null, null);
insert into spu_image
values (43, 6, 'a4eaf7bf9528fe4d.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIGAWtMyAAGxs6Q350k510.jpg',
        null, null);
insert into spu_image
values (44, 6, '9306232083ca53d6.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIGAY4cIAAHCbpsLG8Y072.jpg',
        null, null);
insert into spu_image
values (45, 6, '21401b8a2c2b38f1.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIKAa4cXAAJ021_HJN8583.jpg',
        null, null);
insert into spu_image
values (46, 6, '42ed4e6655d2acca.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIKAMJkPAAJdKCVoSR0812.jpg',
        null, null);
insert into spu_image
values (47, 6, 'a55bc2b7a3b0ecfb.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0kIKAC8WUAAGuYv8KYsE398.jpg',
        null, null);
insert into spu_image
values (48, 7, '4a5fc6ff3ea986e9 (1).jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0lieAGQHUAAIiC_lx9cU417.jpg', null, null);
insert into spu_image
values (49, 7, '6e82f1a4475f871e.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liqALXl6AAOvXBZbBYs429.jpg',
        null, null);
insert into spu_image
values (50, 7, '4a5fc6ff3ea986e9.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liqAR6hmAAIiC_lx9cU271.jpg',
        null, null);
insert into spu_image
values (51, 7, 'cc2d09a3feba8058.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liqAARz7AAHeAIWIl4I126.jpg',
        null, null);
insert into spu_image
values (52, 7, '8d83227b75119532.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liqAE9CSAAIUaEugX8E823.jpg',
        null, null);
insert into spu_image
values (53, 7, '0490b051476c112e.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liuAJTluAAVP1d_tXYs725.jpg',
        null, null);
insert into spu_image
values (54, 7, '31bd117f36197b9d.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liuAZ1P_AALOZHDbvCM585.jpg',
        null, null);
insert into spu_image
values (55, 7, 'ed854afc5bb54697.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0liyAJ34AAAJLREFgZVM767.jpg',
        null, null);
insert into spu_image
values (56, 7, 'dc8784f5f37700e7.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0li2ATv_qAAJbSlyzKD8549.jpg',
        null, null);
insert into spu_image
values (57, 7, 'e26709c6dbd6a1fe.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0li2AZLT5AAMhohWBIMs183.jpg',
        null, null);
insert into spu_image
values (58, 8, '5b73a35dN94a5e30a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l7aADmXLAAI5tpjy5CI066.jpg',
        null, null);
insert into spu_image
values (59, 8, '5b73a36dNd0a67203.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l7yAfFv9AAM5ZEY69Uo453.jpg',
        null, null);
insert into spu_image
values (60, 8, 'c035c2acf72e5ff1.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l7yALvPlAAO4xZsGHFI059.jpg',
        null, null);
insert into spu_image
values (61, 8, '5cdf66beN8aa239ab.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l72AaH20AATmWw3ydsA295.jpg',
        null, null);
insert into spu_image
values (62, 8, '5b73a35aN92891309.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l72AKuQVAALmOIO3U5M856.jpg',
        null, null);
insert into spu_image
values (63, 8, '5b73a362Nc6b5f3fb.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l76AKjn2AAlz4fZOF_8339.jpg',
        null, null);
insert into spu_image
values (64, 8, '5b73a362Nc6b5f3fb (1).jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0l7-AVJfOAAlz4fZOF_8230.jpg', null, null);
insert into spu_image
values (65, 9, '7ffd8d2a4be62085.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAZ6jBAAGu7qTDWVA490.jpg',
        null, null);
insert into spu_image
values (66, 9, 'c406559b05bcf6d4.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAc7geAAFOkBl0eCU984.jpg',
        null, null);
insert into spu_image
values (67, 9, '7496d660c45c45ac.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAbtKiAAFs7t6eSJ0508.jpg',
        null, null);
insert into spu_image
values (68, 9, 'f8051c8538cb011e.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yceAC5dfAAH_Rtwwzq8880.jpg',
        null, null);
insert into spu_image
values (69, 9, 'b28620aae9d31c52.png', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0yciAPvJGAARhSl8kZA8647.png',
        null, null);
insert into spu_image
values (70, 10, '72cec68481f86aff.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1WATxItAAEcZnKxvfI617.jpg',
        null, null);
insert into spu_image
values (71, 10, '1b462be0fb148e88.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1WAKv_cAAHKVw8AZqk151.jpg',
        null, null);
insert into spu_image
values (72, 10, '507a23898221cd6a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1eASPU7AAEiYRrkMww103.jpg',
        null, null);
insert into spu_image
values (73, 10, 'dcc198936a4601de.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1eAS25WAAEYg9IP_7o495.jpg',
        null, null);
insert into spu_image
values (74, 10, '1057db3d2a4deea2.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iAAXYvAAGZqARg5F4191.jpg',
        null, null);
insert into spu_image
values (75, 10, 'bb4a19c813f7e61e.png', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iAaMWAAANMuaHHijI678.png',
        null, null);
insert into spu_image
values (76, 10, '8c35313dfcbccf2a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1iADJZ_AAIz437wUUc659.jpg',
        null, null);
insert into spu_image
values (77, 10, '0ed0cf1bb387059b.png', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-0y1mAcqDEAAVe-gtfew4145.png',
        null, null);
insert into spu_image
values (78, 11, '5ad5104b7cff69f6.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MKAcQ0_AAGxbDKQSm0286.jpg',
        null, null);
insert into spu_image
values (79, 11, '53f744c57c9bed0d.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MKAbhV8AACzhzshAss449.jpg',
        null, null);
insert into spu_image
values (80, 11, '09ee8484ac136e01.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MKAXnZ9AAExlZ_f0b0308.jpg',
        null, null);
insert into spu_image
values (81, 11, '6b1ca0a6e796e5c9.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAIPzOAAHFKmckxVk619.jpg',
        null, null);
insert into spu_image
values (82, 11, '196d96f59897cf39.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSABFB2AAHD3bWoRhw015.jpg',
        null, null);
insert into spu_image
values (83, 11, '6cc3723538c7f7b3.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAPFONAAGchseVkoM398.jpg',
        null, null);
insert into spu_image
values (84, 11, 'a4a448f9df8c715a.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAEXECAAFZJnPg5O0915.jpg',
        null, null);
insert into spu_image
values (85, 11, '374b25b22e90ed74.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAe9k4AAINKcLONPQ919.jpg',
        null, null);
insert into spu_image
values (86, 11, 'a4a448f9df8c715a (1).jpg',
        'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MSAe1vIAAFZJnPg5O0004.jpg', null, null);
insert into spu_image
values (87, 11, 'd6fb7d2f6cb06195.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-00MWAfxwgAAD8jFUkfao175.jpg',
        null, null);
insert into spu_image
values (88, 12, '4cd12718fd5e1bd7.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AeAd45VAAF1GK3U-NE661.jpg',
        null, null);
insert into spu_image
values (89, 12, 'a61a13eb7e3489f1.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AeASZitAAFcbBnUWrw650.jpg',
        null, null);
insert into spu_image
values (90, 12, '0be857e07965a67e.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AiAbf9pAAJ-rvQXZj4029.jpg',
        null, null);
insert into spu_image
values (91, 12, 'b104fa8eec6f6de6.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AuAfizUAAKkARuK5vg313.jpg',
        null, null);
insert into spu_image
values (92, 12, 'c7b173293ee66929.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AuAIVVAAAFjH-WR0oA236.jpg',
        null, null);
insert into spu_image
values (93, 12, '64332079e66a291c.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AyAGFZzAAMnSgOWLUo218.jpg',
        null, null);
insert into spu_image
values (94, 12, '4e9461a5b6e0136f.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02AyARcFFAAKGCeWL410100.jpg',
        null, null);
insert into spu_image
values (95, 12, 'b33f63b0a7fab02d.png', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02A2Ae-VYAAbQwOM632g076.png',
        null, null);
insert into spu_image
values (96, 12, 'b526433a4d9e51ca.jpg', 'http://47.93.148.192:8080/group1/M00/00/02/rBHu8l-02A2AXG14AAY1E5sugTg523.jpg',
        null, null);

-- ----------------------------
-- Table structure for spu_info
-- ----------------------------
drop table if exists spu_info;
create table if not exists spu_info
(
    id           bigint not null auto_increment comment 'spu_id',
    spu_name     varchar(200) comment 'spu名称',
    description  varchar(1000) comment '描述信息',
    category3_id bigint comment '三级品类id',
    tm_id        bigint comment '品牌id',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 21
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = 'spu表'
  row_format = dynamic;

-- ----------------------------
-- Records of spu_info
-- ----------------------------
insert into spu_info
values (1, '小米12S Ultra', '顶级拍照旗舰，影像效果超乎想象。', 61, 5, '2021-12-14 00:00:00', null);
insert into spu_info
values (2, 'Redmi 10X', '高性价比全能手机，续航持久不卡顿。', 61, 1, '2021-12-14 00:00:00', null);
insert into spu_info
values (3, 'Apple iPhone 12', '经典苹果体验，流畅手感一触即发。', 61, 2, '2021-12-14 00:00:00', null);
insert into spu_info
values (4, '联想（Lenovo） 拯救者Y9000P 2022 16英寸游戏笔记本电脑', '强悍性能，畅玩大型3A游戏无压力。', 287, 3,
        '2021-12-14 00:00:00', null);
insert into spu_info
values (5, 'TCL巨幕私人影院电视 4K超高清 AI智慧屏  液晶平板电视机', '超大屏4K影院体验，家庭观影首选。', 86, 4,
        '2021-12-14 00:00:00', null);
insert into spu_info
values (6, '小米电视 内置小爱 智能网络液晶平板教育电视', '智能语音控制，孩子学习与娱乐兼顾。', 86, 5,
        '2021-12-14 00:00:00', null);
insert into spu_info
values (7, '十月稻田 长粒香大米 东北大米 东北香米 5kg', '东北香米，粒粒饱满米香浓郁。', 803, 6, '2021-12-14 00:00:00',
        null);
insert into spu_info
values (8, '金沙河面条 原味银丝挂面 龙须面 方便速食拉面 清汤面 900g', '劲道爽滑，方便速食好选择。', 803, 7,
        '2021-12-14 00:00:00', null);
insert into spu_info
values (9, '索芙特i-Softto 口红不掉色唇膏保湿滋润 璀璨金钻哑光唇膏 ', '持久不脱色，唇色饱满动人。', 477, 8,
        '2021-12-14 00:00:00', null);
insert into spu_info
values (10, 'CAREMiLLE珂曼奶油小方口红 雾面滋润保湿持久丝缎唇膏', '丝缎雾面质感，滋润双唇长久绽放。', 477, 9,
        '2021-12-14 00:00:00', null);
insert into spu_info
values (11, '香奈儿（Chanel）女士香水5号香水 粉邂逅柔情淡香水EDT ', '经典香氛，柔情淡雅一喷迷人。', 473, 11,
        '2021-12-14 00:00:00', null);
insert into spu_info
values (12, '华为智慧屏 4K全面屏智能电视机', '轻薄高性能，办公娱乐全能本。', 86, 12, '2021-12-14 00:00:00', null);
insert into spu_info
values (13, 'HAWEIAI Book 2025英特尔14 Pro满血独显笔记本', '清晰画质，智能家庭娱乐新体验。', 285, 12,
        '2021-12-14 00:00:00', null);
insert into spu_info
values (14, '华为HUAWEI二手笔记本MateBook13触屏2K全面屏', '性价比高，2K触控屏办公顺畅。', 285, 12, '2021-12-14 00:00:00',
        null);
insert into spu_info
values (15, 'H&U&W国行笔记本电脑轻薄本', '便携办公利器，日常使用轻松无压力。', 285, 13, '2021-12-14 00:00:00', null);
insert into spu_info
values (16, 'vivo S20', '自拍旗舰，拍照清晰自然，颜值与性能兼顾。', 61, 14, '2021-12-14 00:00:00', null);
insert into spu_info
values (17, 'REDMI Turbo4 Pro', '充电快，游戏体验顺滑顺畅。', 61, 1, '2021-12-14 00:00:00', null);
insert into spu_info
values (18, '华为Mate 40 pro', '影像旗舰，拍照、性能全面领先。', 61, 12, '2021-12-14 00:00:00', null);
insert into spu_info
values (19, 'Apple iPhone 16 Pro', '全新旗舰，极致流畅与高效体验。', 61, 2, '2021-12-14 00:00:00', null);
insert into spu_info
values (20, 'OPPO Find X8', '超清屏幕与高颜值设计，手感舒适出众。', 61, 15, '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for spu_poster
-- ----------------------------
drop table if exists spu_poster;
create table if not exists spu_poster
(
    id           bigint       not null auto_increment comment '编号',
    spu_id       bigint       null     default null comment '商品id',
    img_name     varchar(200) null     default null comment '文件名称',
    img_url      varchar(200) null     default null comment '文件路径',
    create_time  datetime     not null comment '创建时间',
    operate_time datetime     not null comment '更新时间',
    is_deleted   tinyint      not null default 0 comment '逻辑删除 1（true）已删除， 0（false）未删除',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 1
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '商品海报表'
  row_format = dynamic;

-- ----------------------------
-- Records of spu_poster
-- ----------------------------

-- ----------------------------
-- Table structure for spu_sale_attr
-- ----------------------------
drop table if exists spu_sale_attr;
create table if not exists spu_sale_attr
(
    id                bigint not null auto_increment comment '编号(业务中无关联)',
    spu_id            bigint comment '商品id',
    base_sale_attr_id bigint comment '销售属性id',
    sale_attr_name    varchar(20) comment '销售属性名称(冗余)',
    create_time       datetime comment '创建时间',
    operate_time      datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 17
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = 'spu销售属性表'
  row_format = dynamic;

-- ----------------------------
-- Records of spu_sale_attr
-- ----------------------------
insert into spu_sale_attr
values (1, 1, 1, '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (2, 1, 2, '版本', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (3, 2, 1, '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (4, 2, 2, '版本', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (5, 3, 1, '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (6, 3, 2, '版本', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (7, 4, 5, '处理器或显卡', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (9, 5, 3, '尺码', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (10, 6, 3, '尺码', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (11, 7, 4, '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (12, 8, 4, '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (13, 9, 4, '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (14, 10, 4, '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (15, 11, 4, '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr
values (16, 12, 3, '尺码', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for spu_sale_attr_value
-- ----------------------------
drop table if exists spu_sale_attr_value;
create table if not exists spu_sale_attr_value
(
    id                   bigint not null auto_increment comment '销售属性值编号',
    spu_id               bigint comment 'spuid',
    base_sale_attr_id    bigint comment '销售属性id',
    sale_attr_value_name varchar(200) comment '销售属性值名称',
    sale_attr_name       varchar(200) comment '销售属性名称(冗余)',
    create_time          datetime comment '创建时间',
    operate_time         datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 38
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = 'spu销售属性值表'
  row_format = dynamic;

-- ----------------------------
-- Records of spu_sale_attr_value
-- ----------------------------
insert into spu_sale_attr_value
values (1, 1, 1, '冷杉绿', '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (2, 1, 1, '经典黑', '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (3, 1, 2, '12G+256G', '版本', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (4, 1, 2, '12G+512G', '版本', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (5, 2, 1, '冰雾白', '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (6, 2, 1, '明月灰', '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (7, 2, 2, '4G+128G', '版本', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (8, 2, 2, '8G+128G', '版本', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (9, 3, 1, '黑色', '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (10, 3, 1, '红色', '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (11, 3, 1, '蓝色', '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (12, 3, 1, '白色', '颜色', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (13, 3, 2, '64G', '版本', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (14, 3, 2, '128G', '版本', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (15, 4, 5, 'i9-12700H 512G RTX3060 灰', '处理器或内存', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (16, 4, 5, 'i9-12700H 512G RTX3070Ti 灰', '处理器或内存', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (17, 4, 5, 'i7-12700H 512G RTX3060 灰', '处理器或内存', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (18, 4, 5, 'i7-12700H 512G+2T RTX3060 白', '处理器或内存', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (19, 5, 3, '65英寸', '尺码', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (20, 5, 3, '75英寸', '尺码', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (21, 5, 3, '85英寸', '尺码', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (22, 6, 3, '65英寸', '尺码', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (23, 6, 3, '70英寸', '尺码', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (24, 7, 4, '长粒香大米5KG', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (25, 7, 4, '辽河长粒香5KG', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (26, 8, 4, '900G', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (27, 8, 4, '3*900G', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (28, 9, 4, 'Y01复古红 百搭气质', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (29, 9, 4, 'Z02少女红 活力青春', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (30, 9, 4, 'Z03女王红 性感冷艳', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (31, 10, 4, 'M01醉蔷薇', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (32, 10, 4, 'M02干玫瑰', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (33, 10, 4, 'M03赤茶', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (34, 11, 4, '5号淡香水35ml', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (35, 11, 4, '5号粉邂逅淡香水35ml', '类别', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (36, 12, 3, '55英寸', '尺码', '2021-12-14 00:00:00', null);
insert into spu_sale_attr_value
values (37, 12, 3, '65英寸', '尺码', '2021-12-14 00:00:00', null);

-- ----------------------------
-- Table structure for user_address
-- ----------------------------
drop table if exists user_address;
create table if not exists user_address
(
    id           bigint not null auto_increment comment '编号',
    user_id      bigint comment '用户id',
    province_id  bigint comment '省份id',
    user_address varchar(500) comment '用户地址',
    consignee    varchar(40) comment '收件人',
    phone_num    varchar(40) comment '联系方式',
    is_default   varchar(1) comment '是否是默认',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '用户地址表'
  row_format = dynamic;

-- ----------------------------
-- Records of user_address
-- ----------------------------

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
drop table if exists user_info;
create table if not exists user_info
(
    id           bigint not null auto_increment comment '编号',
    login_name   varchar(200) comment '用户名称',
    nick_name    varchar(200) comment '用户昵称',
    passwd       varchar(200) comment '用户密码',
    name         varchar(200) comment '用户姓名',
    phone_num    varchar(200) comment '手机号',
    email        varchar(200) comment '邮箱',
    head_img     varchar(200) comment '头像',
    user_level   varchar(200) comment '用户级别',
    birthday     date comment '用户生日',
    gender       varchar(1) comment '性别 M男,F女',
    create_time  datetime comment '创建时间',
    operate_time datetime comment '修改时间',
    status       varchar(200) comment '状态',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 50
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '用户表'
  row_format = dynamic;

-- ----------------------------
-- Records of user_info
-- ----------------------------
insert into user_info
values (1, '5vifw38y83', '亮政', null, '马亮政', '13624443478', '5vifw38y83@163.com', null, '3', '1998-05-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (2, 'maoddwb', '珍贞', null, '韩珍贞', '13796741171', 'maoddwb@0355.net', null, '3', '1987-12-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (3, 'stgzyf0g', '功松', null, '范功松', '13256727988', 'stgzyf0g@263.net', null, '2', '1974-04-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (4, '7bgplo7da6h2', '勤勤', null, '南门勤', '13418647143', '7bgplo7da6h2@163.com', null, '1', '2001-03-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (5, 'k3mmqahyod', '功松', null, '苏功松', '13539579772', 'k3mmqahyod@126.com', null, '2', '1989-02-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (6, 't7dk2h', '冰冰', null, '淳于冰', '13178654378', 't7dk2h@263.net', null, '1', '1997-12-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (7, 'vihcj30p1', '豪心', null, '魏豪心', '13956932645', 'vihcj30p1@live.com', null, '1', '1991-06-07', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (8, '02r2ahx', '卿卿', null, '穆卿', '13412413361', '02r2ahx@sohu.com', null, '1', '2001-07-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (9, 'mjhrxnu', '武新', null, '罗武新', '13617856358', 'mjhrxnu@yahoo.com', null, '1', '2001-08-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (10, 'kwua2155', '纨纨', null, '姜纨', '13742843828', 'kwua2155@163.net', null, '3', '1997-11-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (11, 'cmgwb7ppkin', '阿雄', null, '姚雄', '13429591392', 'cmgwb7ppkin@qq.com', null, '3', '1996-06-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (12, '60y6nnx', '咏卿', null, '严咏卿', '13876615939', '60y6nnx@yahoo.com.cn', null, '1', '1994-04-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (13, '3m03hlymsg3t', '茂进', null, '欧阳茂进', '13298737833', '3m03hlymsg3t@3721.net', null, '1', '1996-05-08',
        'M', '2022-06-08 00:00:00', null, null);
insert into user_info
values (14, 'dn8h5z965', '玉玉', null, '钱玉', '13547441827', 'dn8h5z965@163.com', null, '1', '2001-02-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (15, '1rm3htq', '阿炎', null, '马炎', '13292258292', '1rm3htq@qq.com', null, '1', '1999-03-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (16, 'h6ejz7', '洁梅', null, '顾洁梅', '13148353964', 'h6ejz7@msn.com', null, '1', '1967-11-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (17, 'ggycwk2b5', '阿善', null, '钱善', '13425528535', 'ggycwk2b5@163.com', null, '1', '1968-08-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (18, 'x2egtg6p8', '婉娴', null, '伍婉娴', '13597716793', 'x2egtg6p8@3721.net', null, '2', '1982-03-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (19, 'dk7nd4iuggoo', '阿亮', null, '姚亮', '13232515756', 'dk7nd4iuggoo@yahoo.com.cn', null, '1', '1995-12-08',
        'M', '2022-06-08 00:00:00', null, null);
insert into user_info
values (20, 'p5ia3ks', '茜秋', null, '秦茜秋', '13823771879', 'p5ia3ks@yahoo.com.cn', null, '2', '1985-05-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (21, 'hjhqtwl2', '振壮', null, '黄振壮', '13889387431', 'hjhqtwl2@126.com', null, '1', '2002-11-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (22, 'g6jqg3vzq9', '亚宜', null, '熊亚宜', '13893783542', 'g6jqg3vzq9@googlemail.com', null, '2', '1980-07-08',
        'F', '2022-06-08 00:00:00', null, null);
insert into user_info
values (23, 'ahk0cbkkajv', '德行', null, '舒德行', '13584948943', 'ahk0cbkkajv@aol.com', null, '1', '1969-10-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (24, 'tx2jncfen0js', '悦悦', null, '柳悦', '13615362171', 'tx2jncfen0js@263.net', null, '1', '1978-09-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (25, '65swoxxt', '义兴', null, '唐义兴', '13976838475', '65swoxxt@263.net', null, '1', '1980-01-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (26, 'i023bfy23y', '素云', null, '穆素云', '13218631878', 'i023bfy23y@googlemail.com', null, '1', '1969-09-08',
        'F', '2022-06-08 00:00:00', null, null);
insert into user_info
values (27, '2r5r9nx5cm', '盛雄', null, '于盛雄', '13763784866', '2r5r9nx5cm@aol.com', null, '1', '1974-08-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (28, 'uz6ce9', '倩倩', null, '尉迟倩', '13146425993', 'uz6ce9@msn.com', null, '3', '1968-05-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (29, 'l7il2i4mr', '力明', null, '郝力明', '13525978189', 'l7il2i4mr@aol.com', null, '2', '1979-09-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (30, 'so0vah1oz', '宁宁', null, '冯宁', '13352624982', 'so0vah1oz@3721.net', null, '1', '1995-03-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (31, 'brgh2ub', '泽晨', null, '袁泽晨', '13511229488', 'brgh2ub@3721.net', null, '1', '1972-12-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (32, 'orpu36szbp', '颖颖', null, '范颖', '13634137917', 'orpu36szbp@126.com', null, '1', '1970-10-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (33, 'd2uw8al', '贵福', null, '茅贵福', '13577486681', 'd2uw8al@263.net', null, '1', '1972-06-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (34, 'bra8fz', '柔竹', null, '司空柔竹', '13317542416', 'bra8fz@yahoo.com', null, '1', '2006-05-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (35, 'amantuyy0', '阿行', null, '鲍行', '13527165486', 'amantuyy0@ask.com', null, '1', '1991-04-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (36, 'amkowmh', '婵雁', null, '葛婵雁', '13971977259', 'amkowmh@126.com', null, '1', '1984-06-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (37, '8q69ui', '鸣朋', null, '司徒鸣朋', '13141139783', '8q69ui@ask.com', null, '1', '1990-01-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (38, '745p7p2rrfe', '宜宜', null, '俞宜', '13987866129', '745p7p2rrfe@aol.com', null, '1', '1995-11-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (39, 'xejhlltccc', '林有', null, '许林有', '13379219833', 'xejhlltccc@sohu.com', null, '1', '1996-01-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (40, '5ruxdv4', '桂娣', null, '曹桂娣', '13536559486', '5ruxdv4@263.net', null, '2', '1977-07-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (41, 'wvok02on95e', '阿厚', null, '熊厚', '13464138191', 'wvok02on95e@ask.com', null, '2', '1987-02-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (42, '63k5cvx', '艺欣', null, '邹艺欣', '13512773463', '63k5cvx@sohu.com', null, '1', '1973-07-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (43, 'ic6l4q05h9', '阿新', null, '康新', '13149746973', 'ic6l4q05h9@qq.com', null, '2', '1986-08-07', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (44, 'q5j2qefws', '君琴', null, '柳君琴', '13357496986', 'q5j2qefws@aol.com', null, '3', '1977-03-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (45, '21aq6t', '致树', null, '韩致树', '13344779847', '21aq6t@googlemail.com', null, '1', '1988-12-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (46, 'bkny929i', '琴琴', null, '西门琴', '13376776493', 'bkny929i@qq.com', null, '1', '1977-04-08', 'F',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (47, '3tnorb2', '善厚', null, '濮阳善厚', '13669935997', '3tnorb2@aol.com', null, '1', '2003-05-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (48, 'w0q8cmus', '育滢', null, '施育滢', '13822764859', 'w0q8cmus@ask.com', null, '1', '1973-07-08', null,
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (49, 'a9gdq3q', '阿中', null, '岑中', '13154938926', 'a9gdq3q@googlemail.com', null, '3', '1969-01-08', 'M',
        '2022-06-08 00:00:00', null, null);
insert into user_info
values (50, 'ok3hqncd3wx', '晶妍', null, '方晶妍', '13199299967', 'ok3hqncd3wx@0355.net', null, '1', '1968-02-08', 'F',
        '2022-06-08 00:00:00', null, null);

-- ----------------------------
-- Table structure for user_view_log
-- ----------------------------
drop table if exists user_view_log;
create table if not exists user_view_log
(
    id        bigint    not null auto_increment comment '编号',
    user_id   bigint    not null comment '用户编号',
    sku_id    bigint    not null comment 'skuid',
    view_time timestamp null default current_timestamp comment '浏览时间',
    primary key (id) using btree
) engine = InnoDB
  auto_increment = 102
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '用户浏览日志表'
  row_format = dynamic;

-- ----------------------------
-- Records of user_view_log
-- ----------------------------
insert into user_view_log
values (1, 41, 8, '2011-02-08 20:28:06');
insert into user_view_log
values (2, 48, 18, '2012-01-16 10:13:48');
insert into user_view_log
values (3, 15, 9, '2011-06-09 05:17:49');
insert into user_view_log
values (4, 44, 35, '2011-05-16 01:18:52');
insert into user_view_log
values (5, 38, 28, '2011-02-19 08:56:39');
insert into user_view_log
values (6, 2, 6, '2011-12-06 15:24:52');
insert into user_view_log
values (7, 15, 33, '2013-07-24 04:53:06');
insert into user_view_log
values (8, 2, 36, '2011-11-05 21:12:17');
insert into user_view_log
values (9, 46, 42, '2013-12-25 11:17:24');
insert into user_view_log
values (10, 35, 27, '2011-12-09 10:37:19');
insert into user_view_log
values (11, 29, 38, '2012-03-08 03:42:04');
insert into user_view_log
values (12, 1, 11, '2013-12-20 12:31:23');
insert into user_view_log
values (13, 28, 22, '2012-03-07 15:47:40');
insert into user_view_log
values (14, 10, 14, '2012-06-06 21:09:15');
insert into user_view_log
values (15, 7, 6, '2012-08-13 04:42:59');
insert into user_view_log
values (16, 7, 23, '2012-06-18 07:35:55');
insert into user_view_log
values (17, 39, 17, '2011-03-09 11:56:59');
insert into user_view_log
values (18, 47, 30, '2013-04-13 00:01:56');
insert into user_view_log
values (19, 8, 25, '2011-05-03 09:53:03');
insert into user_view_log
values (20, 36, 19, '2013-09-03 13:23:25');
insert into user_view_log
values (21, 40, 24, '2013-06-15 21:14:53');
insert into user_view_log
values (22, 13, 5, '2011-03-13 04:27:24');
insert into user_view_log
values (23, 43, 15, '2012-03-25 13:09:54');
insert into user_view_log
values (24, 6, 15, '2011-06-06 21:36:22');
insert into user_view_log
values (25, 25, 18, '2012-12-05 08:21:40');
insert into user_view_log
values (26, 41, 24, '2011-09-10 16:11:03');
insert into user_view_log
values (27, 24, 23, '2011-11-22 10:59:17');
insert into user_view_log
values (28, 43, 18, '2013-12-26 05:45:27');
insert into user_view_log
values (29, 44, 42, '2011-04-22 02:12:15');
insert into user_view_log
values (30, 26, 32, '2012-04-23 12:59:49');
insert into user_view_log
values (31, 5, 20, '2013-01-20 18:11:56');
insert into user_view_log
values (32, 33, 11, '2013-07-29 22:44:32');
insert into user_view_log
values (33, 14, 7, '2013-08-10 14:53:19');
insert into user_view_log
values (34, 18, 5, '2011-06-12 00:34:16');
insert into user_view_log
values (35, 4, 33, '2013-12-05 10:40:14');
insert into user_view_log
values (36, 17, 21, '2012-11-22 06:23:10');
insert into user_view_log
values (37, 6, 25, '2013-06-03 08:59:12');
insert into user_view_log
values (38, 39, 2, '2013-07-02 01:09:24');
insert into user_view_log
values (39, 15, 14, '2011-03-12 02:34:20');
insert into user_view_log
values (40, 19, 5, '2012-12-10 04:22:32');
insert into user_view_log
values (41, 6, 11, '2011-03-30 11:35:10');
insert into user_view_log
values (42, 28, 10, '2013-04-11 23:00:15');
insert into user_view_log
values (43, 11, 3, '2013-05-02 19:12:39');
insert into user_view_log
values (44, 12, 41, '2011-10-13 07:03:24');
insert into user_view_log
values (45, 9, 27, '2012-05-22 18:47:29');
insert into user_view_log
values (46, 40, 16, '2011-02-21 21:00:32');
insert into user_view_log
values (47, 3, 1, '2011-09-01 04:55:42');
insert into user_view_log
values (48, 23, 22, '2013-09-17 20:21:19');
insert into user_view_log
values (49, 4, 19, '2011-10-26 17:23:41');
insert into user_view_log
values (50, 5, 13, '2012-01-14 11:42:10');
insert into user_view_log
values (51, 13, 9, '2012-08-01 23:45:23');
insert into user_view_log
values (52, 36, 26, '2013-11-15 22:29:50');
insert into user_view_log
values (53, 32, 17, '2012-02-17 09:03:35');
insert into user_view_log
values (54, 49, 40, '2012-12-18 16:09:42');
insert into user_view_log
values (55, 10, 29, '2011-03-21 19:57:18');
insert into user_view_log
values (56, 37, 37, '2012-06-03 20:12:14');
insert into user_view_log
values (57, 3, 38, '2011-07-23 06:47:55');
insert into user_view_log
values (58, 45, 43, '2013-06-30 05:56:44');
insert into user_view_log
values (59, 27, 12, '2011-04-08 11:44:32');
insert into user_view_log
values (60, 13, 16, '2011-05-30 00:34:50');
insert into user_view_log
values (61, 30, 28, '2012-09-02 08:24:06');
insert into user_view_log
values (62, 33, 3, '2012-10-12 17:49:18');
insert into user_view_log
values (63, 50, 8, '2012-05-05 21:39:12');
insert into user_view_log
values (64, 24, 1, '2013-10-17 03:13:19');
insert into user_view_log
values (65, 20, 6, '2011-08-19 06:45:28');
insert into user_view_log
values (66, 30, 27, '2011-12-29 20:25:57');
insert into user_view_log
values (67, 11, 5, '2013-03-30 12:01:06');
insert into user_view_log
values (68, 18, 34, '2012-07-12 09:19:38');
insert into user_view_log
values (69, 7, 18, '2012-08-23 06:15:01');
insert into user_view_log
values (70, 21, 9, '2012-02-11 11:47:43');
insert into user_view_log
values (71, 46, 10, '2011-07-08 15:58:07');
insert into user_view_log
values (72, 19, 30, '2013-11-01 02:48:13');
insert into user_view_log
values (73, 31, 6, '2011-06-03 08:01:44');
insert into user_view_log
values (74, 14, 4, '2012-05-15 03:35:29');
insert into user_view_log
values (75, 22, 20, '2011-08-03 14:16:25');
insert into user_view_log
values (76, 49, 7, '2012-11-20 07:41:48');
insert into user_view_log
values (77, 34, 14, '2013-04-30 06:38:02');
insert into user_view_log
values (78, 21, 4, '2011-01-23 22:17:58');
insert into user_view_log
values (79, 38, 12, '2011-07-16 01:25:56');
insert into user_view_log
values (80, 16, 39, '2012-10-26 18:34:07');
insert into user_view_log
values (81, 17, 22, '2012-09-19 20:06:37');
insert into user_view_log
values (82, 31, 36, '2012-01-30 07:40:12');
insert into user_view_log
values (83, 25, 9, '2013-02-06 05:28:31');
insert into user_view_log
values (84, 26, 10, '2012-03-15 03:27:49');
insert into user_view_log
values (85, 22, 31, '2011-09-28 23:38:41');
insert into user_view_log
values (86, 9, 14, '2013-12-14 10:11:13');
insert into user_view_log
values (87, 42, 19, '2012-04-07 02:11:06');
insert into user_view_log
values (88, 12, 23, '2012-06-10 08:02:15');
insert into user_view_log
values (89, 8, 7, '2013-08-03 10:42:12');
insert into user_view_log
values (90, 45, 29, '2011-03-08 01:27:33');
insert into user_view_log
values (91, 37, 39, '2012-07-09 12:03:09');
insert into user_view_log
values (92, 27, 41, '2013-01-25 13:53:44');
insert into user_view_log
values (93, 5, 12, '2012-09-23 05:38:50');
insert into user_view_log
values (94, 32, 11, '2012-07-21 04:25:55');
insert into user_view_log
values (95, 20, 21, '2012-10-02 06:58:26');
insert into user_view_log
values (96, 16, 2, '2013-11-08 08:59:03');
insert into user_view_log
values (97, 23, 16, '2011-01-10 11:45:16');
insert into user_view_log
values (98, 34, 8, '2013-05-13 01:24:32');
insert into user_view_log
values (99, 29, 40, '2011-08-30 03:42:20');
insert into user_view_log
values (100, 35, 43, '2011-06-26 20:41:12');
insert into user_view_log
values (101, 48, 33, '2012-11-28 09:00:49');
insert into user_view_log
values (102, 50, 13, '2012-03-29 15:03:50');

-- ----------------------------
-- Table structure for ware_info
-- ----------------------------
drop table if exists ware_info;
create table if not exists ware_info
(
    id       bigint not null,
    name     varchar(200),
    address  varchar(200),
    areacode varchar(20),
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci
  row_format = dynamic;

-- ----------------------------
-- Records of ware_info
-- ----------------------------

-- ----------------------------
-- Table structure for ware_order_task
-- ----------------------------
drop table if exists ware_order_task;
create table if not exists ware_order_task
(
    id               bigint not null auto_increment comment '编号',
    order_id         bigint comment '订单编号',
    consignee        varchar(100) comment '收货人',
    consignee_tel    varchar(20) comment '收货人电话',
    delivery_address varchar(1000) comment '送货地址',
    order_comment    varchar(200) comment '订单备注',
    payment_way      varchar(2) comment '付款方式 1:在线付款 2:货到付款',
    task_status      varchar(20) comment '工作单状态',
    order_body       varchar(200) comment '订单描述',
    tracking_no      varchar(200) comment '物流单号',
    create_time      datetime comment '创建时间',
    ware_id          bigint comment '仓库编号',
    task_comment     varchar(500) comment '工作单备注',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '库存工作单表 库存工作单表'
  row_format = dynamic;

-- ----------------------------
-- Records of ware_order_task
-- ----------------------------

-- ----------------------------
-- Table structure for ware_order_task_detail
-- ----------------------------
drop table if exists ware_order_task_detail;
create table if not exists ware_order_task_detail
(
    id            bigint not null auto_increment comment '编号',
    sku_id        bigint comment 'sku_id',
    sku_name      varchar(200) comment 'sku名称',
    sku_num       int comment '购买个数',
    task_id       bigint comment '工作单编号',
    refund_status varchar(20),
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = '库存工作单明细表 库存工作单明细表'
  row_format = dynamic;

-- ----------------------------
-- Records of ware_order_task_detail
-- ----------------------------

-- ----------------------------
-- Table structure for ware_sku
-- ----------------------------
drop table if exists ware_sku;
create table if not exists ware_sku
(
    id           bigint not null auto_increment comment '编号',
    sku_id       bigint comment 'skuid',
    warehouse_id bigint comment '仓库id',
    stock        int comment '库存数',
    stock_name   varchar(200) comment '存货名称',
    stock_locked int comment '锁定库存数',
    primary key (id) using btree
) engine = InnoDB
  character set = utf8mb4
  collate = utf8mb4_general_ci comment = 'sku与仓库关联表'
  row_format = dynamic;
