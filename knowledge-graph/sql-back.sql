-- we don't know how to generate root <with-no-name> (class Root) :(

grant alter, alter routine, create, create routine, create temporary tables, create view, delete, drop, event, execute, index, insert, lock tables, references, select, show view, trigger, update on education.* to issac;

grant alter, alter routine, create, create routine, create temporary tables, create view, delete, drop, event, execute, index, insert, lock tables, references, select, show view, trigger, update on gmail.* to issac;

grant alter, alter routine, create, create routine, create temporary tables, create view, delete, drop, event, execute, index, insert, lock tables, references, select, show view, trigger, update on issac.* to issac;

grant alter, alter routine, create, create routine, create temporary tables, create view, delete, drop, event, execute, index, insert, lock tables, references, select, show view, trigger, update on other.* to issac;

grant alter, alter routine, create, create routine, create temporary tables, create view, delete, drop, event, execute, index, insert, lock tables, references, select, show view, trigger, update on test.* to issac;

drop table if exists activity_info;
create table if not exists activity_info
(
    id            bigint auto_increment comment '活动id'
        primary key,
    activity_name varchar(200)  null comment '活动名称',
    activity_type varchar(10)   null comment '活动类型（1：满减，2：折扣）',
    activity_desc varchar(2000) null comment '活动描述',
    start_time    datetime      null comment '开始时间',
    end_time      datetime      null comment '结束时间',
    create_time   datetime      null comment '创建时间',
    operate_time  datetime      null comment '修改时间'
)
    comment '活动表' collate = utf8mb4_general_ci
                     row_format = DYNAMIC;

drop table if exists activity_rule;
create table if not exists activity_rule
(
    id               int auto_increment comment '编号'
        primary key,
    activity_id      int            null comment '活动id',
    activity_type    varchar(20)    null comment '活动类型',
    condition_amount decimal(16, 2) null comment '满减金额',
    condition_num    bigint         null comment '满减件数',
    benefit_amount   decimal(16, 2) null comment '优惠金额',
    benefit_discount decimal(10, 2) null comment '优惠折扣',
    benefit_level    bigint         null comment '优惠级别',
    create_time      datetime       null comment '创建时间',
    operate_time     datetime       null comment '修改时间'
)
    comment '活动规则表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

drop table if exists activity_sku;
create table if not exists activity_sku
(
    id           bigint auto_increment comment '编号'
        primary key,
    activity_id  bigint   null comment '活动id ',
    sku_id       bigint   null comment 'sku_id',
    create_time  datetime null comment '创建时间',
    operate_time datetime null comment '修改时间'
)
    comment '活动商品关联表' collate = utf8mb4_general_ci
                             row_format = DYNAMIC;

drop table if exists base_attr_info;
create table if not exists base_attr_info
(
    id             bigint auto_increment comment '编号'
        primary key,
    attr_name      varchar(100) not null comment '属性名称',
    category_id    bigint       null comment '分类id',
    category_level int          null comment '分类层级',
    create_time    datetime     null comment '创建时间',
    operate_time   datetime     null comment '修改时间'
)
    comment '属性表' collate = utf8mb4_general_ci
                     row_format = DYNAMIC;

drop table if exists base_attr_value;
create table if not exists base_attr_value
(
    id           bigint auto_increment comment '编号'
        primary key,
    value_name   varchar(100) not null comment '属性值名称',
    attr_id      bigint       null comment '属性id',
    create_time  datetime     null comment '创建时间',
    operate_time datetime     null comment '修改时间'
)
    comment '属性值表' collate = utf8mb4_general_ci
                       row_format = DYNAMIC;

drop table if exists base_category1;
create table if not exists base_category1
(
    id           bigint auto_increment comment '一级品类id'
        primary key,
    name         varchar(10) not null comment '一级品类名称',
    create_time  datetime    null comment '创建时间',
    operate_time datetime    null comment '修改时间'
)
    comment '一级品类表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

drop table if exists base_category2;
create table if not exists base_category2
(
    id           bigint auto_increment comment '二级品类id'
        primary key,
    name         varchar(200) not null comment '二级品类名称',
    category1_id bigint       null comment '一级品类编号',
    create_time  datetime     null comment '创建时间',
    operate_time datetime     null comment '修改时间'
)
    comment '二级品类表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

drop table if exists base_category3;
create table if not exists base_category3
(
    id           bigint auto_increment comment '三级品类id'
        primary key,
    name         varchar(200) not null comment '三级品类名称',
    category2_id bigint       null comment '二级品类编号',
    create_time  datetime     null comment '创建时间',
    operate_time datetime     null comment '修改时间'
)
    comment '三级品类表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

drop table if exists base_dic;
create table if not exists base_dic
(
    dic_code     varchar(10)  not null comment '编号'
        primary key,
    dic_name     varchar(100) null comment '编码名称',
    parent_code  varchar(10)  null comment '父编号',
    create_time  datetime     null comment '创建日期',
    operate_time datetime     null comment '修改日期'
)
    collate = utf8mb4_general_ci
    row_format = DYNAMIC;

drop table if exists base_frontend_param;
create table if not exists base_frontend_param
(
    id           bigint auto_increment comment '编号'
        primary key,
    code         varchar(100) not null comment '属性名称',
    delete_id    bigint       null comment '分类id',
    create_time  datetime     null comment '创建时间',
    operate_time datetime     null comment '修改时间'
)
    comment '前端数据保护表' collate = utf8mb4_general_ci
                             row_format = DYNAMIC;

drop table if exists base_province;
create table if not exists base_province
(
    id           bigint      not null comment 'id'
        primary key,
    name         varchar(20) null comment '省份名称',
    region_id    varchar(20) null comment '地区id',
    area_code    varchar(20) null comment '地区编码',
    iso_code     varchar(20) null comment '旧版国际标准地区编码，供可视化使用',
    iso_3166_2   varchar(20) null comment '新版国际标准地区编码，供可视化使用',
    create_time  datetime    null comment '创建时间',
    operate_time datetime    null comment '修改时间'
)
    comment '省份表' collate = utf8mb4_general_ci
                     row_format = DYNAMIC;

drop table if exists base_region;
create table if not exists base_region
(
    id           varchar(20) null comment '地区id',
    region_name  varchar(20) null comment '地区名称',
    create_time  datetime    null comment '创建时间',
    operate_time datetime    null
)
    comment '地区表' collate = utf8mb4_general_ci
                     row_format = DYNAMIC;

drop table if exists base_sale_attr;
create table if not exists base_sale_attr
(
    id           bigint auto_increment comment '编号'
        primary key,
    name         varchar(20) not null comment '销售属性名称',
    create_time  datetime    null comment '创建时间',
    operate_time datetime    null comment '修改时间'
)
    comment '基本销售属性表' collate = utf8mb4_general_ci
                             row_format = DYNAMIC;

drop table if exists base_sale_attr_value;
create table if not exists base_trademark
(
    id           bigint auto_increment comment '编号'
        primary key,
    tm_name      varchar(100) not null comment '品牌名称',
    logo_url     varchar(200) null comment '品牌logo的图片路径',
    create_time  datetime     null comment '创建时间',
    operate_time datetime     null comment '修改时间'
)
    comment '品牌表' collate = utf8mb4_general_ci
                     row_format = DYNAMIC;

drop table if exists cart_info;
create table if not exists cart_info
(
    id           bigint auto_increment comment '编号'
        primary key,
    user_id      varchar(200)   null comment '用户id',
    sku_id       bigint         null comment 'skuid',
    cart_price   decimal(10, 2) null comment '放入购物车时价格',
    sku_num      int            null comment '数量',
    img_url      varchar(200)   null comment '商品图片地址',
    sku_name     varchar(200)   null comment 'sku名称 (冗余)',
    is_checked   int            null comment '是否被选中',
    create_time  datetime       null comment '创建时间',
    operate_time datetime       null comment '修改时间',
    is_ordered   bigint         null comment '是否已经下单',
    order_time   datetime       null comment '下单时间'
)
    comment '购物车表' collate = utf8mb4_general_ci
                       row_format = DYNAMIC;

drop index idx_uid on cart_info;
create index idx_uid on cart_info (user_id);


drop table if exists cms_banner;
create table if not exists cms_banner
(
    id           bigint auto_increment comment 'ID'
        primary key,
    title        varchar(20)  default ''  null comment '标题',
    image_url    varchar(500) default ''  not null comment '图片地址',
    link_url     varchar(500) default ''  null comment '链接地址',
    sort         int unsigned default '0' not null comment '排序',
    create_time  datetime                 null comment '创建时间',
    operate_time datetime                 null comment '修改时间'
)
    comment '首页banner表' row_format = DYNAMIC;

drop table if exists comment_info;
create table if not exists comment_info
(
    id           bigint auto_increment comment '编号'
        primary key,
    user_id      bigint        null comment '用户id',
    nick_name    varchar(20)   null comment '用户昵称',
    head_img     varchar(200)  null,
    sku_id       bigint        null comment 'skuid',
    spu_id       bigint        null comment 'spuid',
    order_id     bigint        null comment '订单编号',
    appraise     varchar(10)   null comment '评价 1 好评 2 中评 3 差评',
    comment_txt  varchar(2000) null comment '评价内容',
    create_time  datetime      null comment '创建时间',
    operate_time datetime      null comment '修改时间'
)
    comment '商品评论表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

create table if not exists coupon_info
(
    id               bigint auto_increment comment '购物券编号'
        primary key,
    coupon_name      varchar(100)   null comment '购物券名称',
    coupon_type      varchar(10)    null comment '购物券类型 1 现金券 2 折扣券 3 满减券 4 满件打折券',
    condition_amount decimal(10, 2) null comment '满额数',
    condition_num    bigint         null comment '满件数',
    activity_id      bigint         null comment '活动编号',
    benefit_amount   decimal(16, 2) null comment '减免金额',
    benefit_discount decimal(10, 2) null comment '折扣',
    create_time      datetime       null comment '创建时间',
    range_type       varchar(10)    null comment '范围类型 1、商品(spuid) 2、品类(三级分类id) 3、品牌',
    limit_num        int default 0  not null comment '最多领用次数',
    taken_count      int default 0  not null comment '已领用次数',
    start_time       datetime       null comment '可以领取的开始时间',
    end_time         datetime       null comment '可以领取的结束时间',
    operate_time     datetime       null comment '修改时间',
    expire_time      datetime       null comment '过期时间',
    range_desc       varchar(500)   null comment '范围描述'
)
    comment '优惠券信息表' collate = utf8mb4_general_ci
                           row_format = DYNAMIC;


create table if not exists coupon_range
(
    id           bigint auto_increment comment '购物券编号'
        primary key,
    coupon_id    bigint      default 0  not null comment '优惠券id',
    range_type   varchar(10) default '' not null comment '范围类型 1、商品(spuid) 2、品类(三级分类id) 3、品牌',
    range_id     bigint      default 0  not null,
    create_time  datetime               null comment '创建时间',
    operate_time datetime               null comment '修改时间'
)
    comment '优惠券范围表' collate = utf8mb4_general_ci
                           row_format = DYNAMIC;


drop table if exists coupon_use;
create table if not exists coupon_use
(
    id            bigint auto_increment comment '编号'
        primary key,
    coupon_id     bigint      null comment '购物券ID',
    user_id       bigint      null comment '用户ID',
    order_id      bigint      null comment '订单ID',
    coupon_status varchar(10) null comment '购物券状态（1：未使用 2：已使用）',
    get_time      datetime    null comment '获取时间',
    using_time    datetime    null comment '使用时间',
    used_time     datetime    null comment '支付时间',
    expire_time   datetime    null comment '过期时间',
    create_time   datetime    null comment '创建时间',
    operate_time  datetime    null comment '修改时间'
)
    comment '优惠券领用表' collate = utf8mb4_general_ci
                           row_format = DYNAMIC;


create table if not exists favor_info
(
    id           bigint auto_increment comment '编号'
        primary key,
    user_id      bigint     null comment '用户id',
    sku_id       bigint     null comment 'skuid',
    spu_id       bigint     null comment 'spuid',
    is_cancel    varchar(1) null comment '是否已取消 0 正常 1 已取消',
    create_time  datetime   null comment '创建时间',
    operate_time datetime   null comment '修改时间'
)
    comment '商品收藏表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

create table if not exists financial_sku_cost
(
    id          varchar(20)    not null
        primary key,
    sku_id      bigint         null comment 'sku_id',
    sku_name    varchar(20)    null comment 'sku名称',
    busi_date   varchar(20)    null comment '业务日期',
    is_lastest  varchar(2)     null comment '是否最近',
    sku_cost    decimal(16, 2) null comment '商品结算成本',
    create_time datetime       null comment '创建时间'
)
    collate = utf8mb4_general_ci
    row_format = DYNAMIC;

create table if not exists order_detail
(
    id                    bigint auto_increment comment '编号'
        primary key,
    order_id              bigint         null comment '订单id',
    sku_id                bigint         null comment 'sku_id',
    sku_name              varchar(200)   null comment 'sku名称（冗余）',
    img_url               varchar(200)   null comment '图片链接（冗余）',
    order_price           decimal(10, 2) null comment '购买价格(下单时sku价格）',
    sku_num               bigint         null comment '购买个数',
    create_time           datetime       null comment '创建时间',
    split_total_amount    decimal(16, 2) null,
    split_activity_amount decimal(16, 2) null,
    split_coupon_amount   decimal(16, 2) null,
    operate_time          datetime       null comment '修改时间'
)
    comment '订单明细表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

create table if not exists order_detail_activity
(
    id               bigint auto_increment comment '编号'
        primary key,
    order_id         bigint   null comment '订单id',
    order_detail_id  bigint   null comment '订单明细id',
    activity_id      bigint   null comment '活动id',
    activity_rule_id bigint   null comment '活动规则id',
    sku_id           bigint   null comment 'skuid',
    create_time      datetime null comment '创建时间',
    operate_time     datetime null comment '修改时间'
)
    comment '订单明细活动关联表' collate = utf8mb4_general_ci
                                 row_format = DYNAMIC;

create table if not exists order_detail_coupon
(
    id              bigint auto_increment comment '编号'
        primary key,
    order_id        bigint   null comment '订单id',
    order_detail_id bigint   null comment '订单明细id',
    coupon_id       bigint   null comment '购物券id',
    coupon_use_id   bigint   null comment '购物券领用id',
    sku_id          bigint   null comment 'skuid',
    create_time     datetime null comment '创建时间',
    operate_time    datetime null comment '修改时间'
)
    comment '订单明细优惠券关联表' collate = utf8mb4_general_ci
                                   row_format = DYNAMIC;

create table if not exists order_info
(
    id                     bigint auto_increment comment '编号'
        primary key,
    consignee              varchar(100)   null comment '收货人',
    consignee_tel          varchar(20)    null comment '收件人电话',
    total_amount           decimal(10, 2) null comment '总金额',
    order_status           varchar(20)    null comment '订单状态',
    user_id                bigint         null comment '用户id',
    payment_way            varchar(20)    null comment '付款方式',
    delivery_address       varchar(1000)  null comment '送货地址',
    order_comment          varchar(200)   null comment '订单备注',
    out_trade_no           varchar(50)    null comment '订单交易编号（第三方支付用）',
    trade_body             varchar(200)   null comment '订单描述(第三方支付用)',
    create_time            datetime       null comment '创建时间',
    operate_time           datetime       null comment '操作时间',
    expire_time            datetime       null comment '失效时间',
    process_status         varchar(20)    null comment '进度状态',
    tracking_no            varchar(100)   null comment '物流单编号',
    parent_order_id        bigint         null comment '父订单编号',
    img_url                varchar(200)   null comment '图片链接',
    province_id            int            null comment '省份id',
    activity_reduce_amount decimal(16, 2) null comment '活动减免金额',
    coupon_reduce_amount   decimal(16, 2) null comment '优惠券减免金额',
    original_total_amount  decimal(16, 2) null comment '原始总金额',
    feight_fee             decimal(16, 2) null comment '运费金额',
    feight_fee_reduce      decimal(16, 2) null comment '运费减免金额',
    refundable_time        datetime       null comment '可退款时间（签收后30天）'
)
    comment '订单表' collate = utf8mb4_general_ci
                     row_format = DYNAMIC;

create index idx_uid_status
    on order_info (order_status, user_id);

create table if not exists order_refund_info
(
    id                 bigint auto_increment comment '编号'
        primary key,
    user_id            bigint         null comment '用户id',
    order_id           bigint         null comment '订单id',
    sku_id             bigint         null comment 'skuid',
    refund_type        varchar(20)    null comment '退款类型',
    refund_num         bigint         null comment '退货件数',
    refund_amount      decimal(16, 2) null comment '退款金额',
    refund_reason_type varchar(200)   null comment '原因类型',
    refund_reason_txt  varchar(20)    null comment '原因内容',
    refund_status      varchar(10)    null comment '退款状态（0：待审批 1：已退款）',
    create_time        datetime       null comment '创建时间',
    operate_time       datetime       null comment '修改时间'
)
    comment '退单表' collate = utf8mb4_general_ci
                     row_format = DYNAMIC;

create table if not exists order_status_log
(
    id           bigint auto_increment comment '编号'
        primary key,
    order_id     bigint      null comment '订单id',
    order_status varchar(11) null comment '订单状态',
    create_time  datetime    null comment '创建时间',
    operate_time datetime    null comment '修改时间'
)
    comment '订单状态流水表' collate = utf8mb4_general_ci
                             row_format = DYNAMIC;

create table if not exists payment_info
(
    id               int auto_increment comment '编号'
        primary key,
    out_trade_no     varchar(50)    null comment '对外业务编号',
    order_id         bigint         null comment '订单id',
    user_id          bigint         null comment '用户id',
    payment_type     varchar(20)    null comment '支付类型（微信 支付宝）',
    trade_no         varchar(50)    null comment '交易编号',
    total_amount     decimal(10, 2) null comment '支付金额',
    subject          varchar(200)   null comment '交易内容',
    payment_status   varchar(20)    null comment '支付状态',
    create_time      datetime       null comment '创建时间',
    callback_time    datetime       null comment '回调时间',
    callback_content text           null comment '回调信息',
    operate_time     datetime       null comment '修改时间'
)
    comment '支付信息表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

create table if not exists promotion_pos
(
    id             bigint       not null comment '营销坑位id'
        primary key,
    pos_location   varchar(200) null comment '营销坑位位置',
    pos_type       varchar(20)  null comment '营销坑位类型：banner,宫格,列表, 瀑布',
    promotion_type varchar(20)  null comment '营销类型：算法、固定、搜索',
    create_time    datetime     null comment '创建时间',
    operate_time   datetime     null comment '修改时间'
)
    comment '营销坑位表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

create table if not exists promotion_refer
(
    id           bigint       not null comment '外部营销渠道id'
        primary key,
    refer_name   varchar(200) null comment '外部营销渠道名称',
    create_time  datetime     null comment '创建时间',
    operate_time datetime     null comment '修改时间'
)
    comment '营销渠道表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

create table if not exists refund_payment
(
    id               int auto_increment comment '编号'
        primary key,
    out_trade_no     varchar(50)    null comment '对外业务编号',
    order_id         bigint         null comment '订单id',
    sku_id           bigint         null comment 'skuid',
    payment_type     varchar(20)    null comment '支付类型（微信 支付宝）',
    trade_no         varchar(50)    null comment '交易编号',
    total_amount     decimal(10, 2) null comment '退款金额',
    subject          varchar(200)   null comment '交易内容',
    refund_status    varchar(30)    null comment '退款状态',
    create_time      datetime       null comment '创建时间',
    callback_time    datetime       null comment '回调时间',
    callback_content text           null comment '回调信息',
    operate_time     datetime       null comment '修改时间'
)
    comment '退款支付表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

create index idx_order_id
    on refund_payment (order_id);

create index idx_out_trade_no
    on refund_payment (out_trade_no);

create table if not exists seckill_goods
(
    id              bigint auto_increment
        primary key,
    spu_id          bigint         null comment 'spu_id',
    sku_id          bigint         null comment 'sku_id',
    sku_name        varchar(100)   null comment '标题',
    sku_default_img varchar(150)   null comment '商品图片',
    price           decimal(10, 2) null comment '原价格',
    cost_price      decimal(10, 2) null comment '秒杀价格',
    create_time     datetime       null comment '添加日期',
    check_time      datetime       null comment '审核日期',
    status          varchar(1)     null comment '审核状态',
    start_time      datetime       null comment '开始时间',
    end_time        datetime       null comment '结束时间',
    num             int            null comment '秒杀商品数',
    stock_count     int            null comment '剩余库存数',
    sku_desc        varchar(2000)  null comment '描述'
)
    collate = utf8mb4_general_ci
    row_format = DYNAMIC;

create table if not exists sku_attr_value
(
    id           bigint auto_increment comment '编号'
        primary key,
    attr_id      bigint      null comment '平台属性id（冗余）',
    value_id     bigint      null comment '平台属性值id',
    sku_id       bigint      null comment 'skuid',
    attr_name    varchar(30) null comment '平台属性名称',
    value_name   varchar(30) null comment '平台属性值名称',
    create_time  datetime    null comment '创建时间',
    operate_time datetime    null comment '修改时间'
)
    comment 'sku平台属性值关联表' collate = utf8mb4_general_ci
                                  row_format = DYNAMIC;

create table if not exists sku_image
(
    id           bigint auto_increment comment '编号'
        primary key,
    sku_id       bigint        null comment 'skuid',
    img_name     varchar(200)  null comment '图片名称（冗余）',
    img_url      varchar(300)  null comment '图片路径(冗余)',
    spu_img_id   bigint        null comment 'spu图片id',
    is_default   varchar(4000) null comment '是否默认',
    create_time  datetime      null comment '创建时间',
    operate_time datetime      null comment '修改时间'
)
    comment '库存单元图片表' collate = utf8mb4_general_ci
                             row_format = DYNAMIC;

create table if not exists sku_info
(
    id              bigint auto_increment comment 'skuid'
        primary key,
    spu_id          bigint            null comment 'spuid',
    price           decimal           null comment '价格',
    sku_name        varchar(200)      null comment 'sku名称',
    sku_desc        varchar(2000)     null comment '商品规格描述',
    weight          decimal(10, 2)    null comment '重量',
    tm_id           bigint            null comment '品牌id(冗余)',
    category3_id    bigint            null comment '三级品类id（冗余）',
    sku_default_img varchar(300)      null comment '默认显示图片地址(冗余)',
    is_sale         tinyint default 0 not null comment '是否在售（1：是 0：否）',
    create_time     datetime          null comment '创建时间',
    operate_time    datetime          null comment '修改时间'
)
    comment 'sku表' collate = utf8mb4_general_ci
                    row_format = DYNAMIC;

create table if not exists sku_sale_attr_value
(
    id                   bigint auto_increment comment '编号'
        primary key,
    sku_id               bigint      null comment 'sku_id',
    spu_id               int         null comment 'spu_id(冗余)',
    sale_attr_value_id   bigint      null comment '销售属性值id',
    sale_attr_id         bigint      null comment '销售属性id',
    sale_attr_name       varchar(30) null comment '销售属性名称',
    sale_attr_value_name varchar(30) null comment '销售属性值名称',
    create_time          datetime    null comment '创建时间',
    operate_time         datetime    null comment '修改时间'
)
    comment 'sku销售属性值表' collate = utf8mb4_general_ci
                              row_format = DYNAMIC;

create table if not exists spu_image
(
    id           bigint auto_increment comment '编号'
        primary key,
    spu_id       bigint       null comment '商品id',
    img_name     varchar(200) null comment '图片名称',
    img_url      varchar(300) null comment '图片路径',
    create_time  datetime     null comment '创建时间',
    operate_time datetime     null comment '修改时间'
)
    comment 'spu图片表' collate = utf8mb4_general_ci
                        row_format = DYNAMIC;

create table if not exists spu_info
(
    id           bigint auto_increment comment 'spu_id'
        primary key,
    spu_name     varchar(200)  null comment 'spu名称',
    description  varchar(1000) null comment '描述信息',
    category3_id bigint        null comment '三级品类id',
    tm_id        bigint        null comment '品牌id',
    create_time  datetime      null comment '创建时间',
    operate_time datetime      null comment '修改时间'
)
    comment 'spu表' collate = utf8mb4_general_ci
                    row_format = DYNAMIC;

create table if not exists spu_poster
(
    id           bigint auto_increment comment '编号'
        primary key,
    spu_id       bigint            null comment '商品id',
    img_name     varchar(200)      null comment '文件名称',
    img_url      varchar(200)      null comment '文件路径',
    create_time  datetime          not null comment '创建时间',
    operate_time datetime          not null comment '更新时间',
    is_deleted   tinyint default 0 not null comment '逻辑删除 1（true）已删除， 0（false）未删除'
)
    comment '商品海报表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

create table if not exists spu_sale_attr
(
    id                bigint auto_increment comment '编号(业务中无关联)'
        primary key,
    spu_id            bigint      null comment '商品id',
    base_sale_attr_id bigint      null comment '销售属性id',
    sale_attr_name    varchar(20) null comment '销售属性名称(冗余)',
    create_time       datetime    null comment '创建时间',
    operate_time      datetime    null comment '修改时间'
)
    comment 'spu销售属性表' collate = utf8mb4_general_ci
                            row_format = DYNAMIC;

create table if not exists spu_sale_attr_value
(
    id                   bigint auto_increment comment '销售属性值编号'
        primary key,
    spu_id               bigint       null comment 'spuid',
    base_sale_attr_id    bigint       null comment '销售属性id',
    sale_attr_value_name varchar(200) null comment '销售属性值名称',
    sale_attr_name       varchar(200) null comment '销售属性名称(冗余)',
    create_time          datetime     null comment '创建时间',
    operate_time         datetime     null comment '修改时间'
)
    comment 'spu销售属性值表' collate = utf8mb4_general_ci
                              row_format = DYNAMIC;

create table if not exists user_address
(
    id           bigint auto_increment comment '编号'
        primary key,
    user_id      bigint       null comment '用户id',
    province_id  bigint       null comment '省份id',
    user_address varchar(500) null comment '用户地址',
    consignee    varchar(40)  null comment '收件人',
    phone_num    varchar(40)  null comment '联系方式',
    is_default   varchar(1)   null comment '是否是默认',
    create_time  datetime     null comment '创建时间',
    operate_time datetime     null comment '修改时间'
)
    comment '用户地址表' collate = utf8mb4_general_ci
                         row_format = DYNAMIC;

create table if not exists user_info
(
    id           bigint auto_increment comment '编号'
        primary key,
    login_name   varchar(200) null comment '用户名称',
    nick_name    varchar(200) null comment '用户昵称',
    passwd       varchar(200) null comment '用户密码',
    name         varchar(200) null comment '用户姓名',
    phone_num    varchar(200) null comment '手机号',
    email        varchar(200) null comment '邮箱',
    head_img     varchar(200) null comment '头像',
    user_level   varchar(200) null comment '用户级别',
    birthday     date         null comment '用户生日',
    gender       varchar(1)   null comment '性别 M男,F女',
    create_time  datetime     null comment '创建时间',
    operate_time datetime     null comment '修改时间',
    status       varchar(200) null comment '状态'
)
    comment '用户表' collate = utf8mb4_general_ci
                     row_format = DYNAMIC;

create table if not exists ware_info
(
    id       bigint       not null
        primary key,
    name     varchar(200) null,
    address  varchar(200) null,
    areacode varchar(20)  null
)
    collate = utf8mb4_general_ci
    row_format = DYNAMIC;

create table if not exists ware_order_task
(
    id               bigint auto_increment comment '编号'
        primary key,
    order_id         bigint        null comment '订单编号',
    consignee        varchar(100)  null comment '收货人',
    consignee_tel    varchar(20)   null comment '收货人电话',
    delivery_address varchar(1000) null comment '送货地址',
    order_comment    varchar(200)  null comment '订单备注',
    payment_way      varchar(2)    null comment '付款方式 1:在线付款 2:货到付款',
    task_status      varchar(20)   null comment '工作单状态',
    order_body       varchar(200)  null comment '订单描述',
    tracking_no      varchar(200)  null comment '物流单号',
    create_time      datetime      null comment '创建时间',
    ware_id          bigint        null comment '仓库编号',
    task_comment     varchar(500)  null comment '工作单备注'
)
    comment '库存工作单表 库存工作单表' collate = utf8mb4_general_ci
                                        row_format = DYNAMIC;

create table if not exists ware_order_task_detail
(
    id            bigint auto_increment comment '编号'
        primary key,
    sku_id        bigint       null comment 'sku_id',
    sku_name      varchar(200) null comment 'sku名称',
    sku_num       int          null comment '购买个数',
    task_id       bigint       null comment '工作单编号',
    refund_status varchar(20)  null
)
    comment '库存工作单明细表 库存工作单明细表' collate = utf8mb4_general_ci
                                                row_format = DYNAMIC;

create table if not exists ware_sku
(
    id           bigint auto_increment comment '编号'
        primary key,
    sku_id       bigint       null comment 'skuid',
    warehouse_id bigint       null comment '仓库id',
    stock        int          null comment '库存数',
    stock_name   varchar(200) null comment '存货名称',
    stock_locked int          null comment '锁定库存数'
)
    comment 'sku与仓库关联表' collate = utf8mb4_general_ci
                              row_format = DYNAMIC;

create table if not exists z_log
(
    id  bigint auto_increment
        primary key,
    log varchar(4000) null
)
    collate = utf8mb4_general_ci
    row_format = DYNAMIC;

