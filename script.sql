create table addresses
(
    id         int auto_increment
        primary key,
    username   varchar(50)                         not null,
    name       varchar(100)                        not null,
    address    varchar(255)                        not null,
    phone      varchar(20)                         not null,
    postcode   varchar(20)                         not null,
    city       varchar(100)                        not null,
    created_at timestamp default CURRENT_TIMESTAMP not null,
    member_id  int                                 null
);

create index fk_member_id
    on addresses (member_id);

create index username
    on addresses (username);

create table balance_transactions
(
    id                   int auto_increment
        primary key,
    user_id              int            not null,
    amount               decimal(10, 2) not null,
    transaction_datetime datetime       not null,
    member_id            int            not null
);

create index fk_member_id
    on balance_transactions (member_id);

create index user_id
    on balance_transactions (user_id);

create table countryregion
(
    id   int auto_increment
        primary key,
    name varchar(255) not null
);

create table freighttemplate
(
    id                     int auto_increment
        primary key,
    country_region_id      int            null,
    transportation_id      int            null,
    first_weight_rate      decimal(10, 2) not null,
    additional_weight_rate decimal(10, 2) not null
);

create index country_region_id
    on freighttemplate (country_region_id);

create index transportation_id
    on freighttemplate (transportation_id);

create table orders
(
    id                            int auto_increment
        primary key,
    user_id                       int                                                          not null,
    tracking_number               varchar(50)                                                  not null,
    international_tracking_number varchar(50)                                                  null,
    shipping_address              varchar(255)                                                 not null,
    city                          varchar(100)                                                 not null,
    delivery_method               varchar(20)                                                  not null,
    courier_company               varchar(100)                                                 not null,
    is_sensitive                  varchar(20)                                                  not null,
    remarks                       text                                                         null,
    created_at                    timestamp   default CURRENT_TIMESTAMP                        not null,
    volume                        decimal(10, 2)                                               null,
    weight                        decimal(10, 2)                                               null,
    payment_amount                decimal(10, 2)                                               null,
    order_status                  varchar(20) default '待支付''已支付''待发货''已发货''已签收' not null,
    member_id                     int                                                          not null,
    transaction_datetime          datetime                                                     null
);

create index member_id
    on orders (member_id);

create index user_id
    on orders (user_id);

create table packages
(
    id              int auto_increment
        primary key,
    member_id       varchar(20)                                                                                 null,
    warehouse_name  varchar(100)                                                                                not null,
    item_name       varchar(255)                                                                                null,
    weight          decimal(10, 2)                                                                              null,
    size            varchar(50)                                                                                 null,
    quantity        int                                                                                         null,
    status          enum ('未入库', '已入库', '待处理', '已打包', '已发货', '已收货') default '未入库'          null,
    tracking_number varchar(50)                                                                                 null,
    courier_company varchar(100)                                                                                null,
    note            text                                                                                        null,
    created_at      timestamp                                                         default CURRENT_TIMESTAMP not null,
    order_id        int                                                                                         null,
    cargo_type      enum ('敏感货', '普货')                                           default '普货'            null
);

create index fk_order_id
    on packages (order_id);

create index member_id
    on packages (member_id);

create index warehouse_name
    on packages (warehouse_name);

create table thresholdsetting
(
    id                  int auto_increment
        primary key,
    freight_template_id int            null,
    threshold_value     decimal(10, 2) not null,
    extra_rate          decimal(10, 2) not null
);

create index freight_template_id
    on thresholdsetting (freight_template_id);

create table transportation
(
    id   int auto_increment
        primary key,
    name varchar(255) not null
);

create table users
(
    id         int auto_increment
        primary key,
    username   varchar(50)                         not null,
    password   varchar(255)                        not null,
    wechat     varchar(50)                         not null,
    email      varchar(100)                        not null,
    phone      varchar(20)                         not null,
    member_id  varchar(20)                         not null,
    created_at timestamp default CURRENT_TIMESTAMP not null
);

create table wallets
(
    id        int auto_increment
        primary key,
    user_id   int                         not null,
    balance   decimal(10, 2) default 0.00 not null,
    member_id varchar(20)                 null
);

create index fk_users_member_id
    on wallets (member_id);

create index user_id
    on wallets (user_id);

create definer = root@localhost trigger sync_member_id
    after insert
    on wallets
    for each row
BEGIN
    UPDATE your_database_name.users
    SET member_id = NEW.member_id
    WHERE id = NEW.user_id;
END;

create table warehouses
(
    id                       int auto_increment
        primary key,
    warehouse_name           varchar(100)                        not null,
    warehouse_address        varchar(255)                        not null,
    warehouse_contact_person varchar(50)                         not null,
    warehouse_phone_number   varchar(20)                         not null,
    warehouse_postcode       varchar(20)                         not null,
    created_at               timestamp default CURRENT_TIMESTAMP not null
);


