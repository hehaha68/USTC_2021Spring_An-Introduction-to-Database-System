drop database if exists exp3;
create database exp3;
use exp3;

create table 储蓄开户 
(
   身份证号                 varchar(20)             not null,
   名字                   varchar(20)             not null,
   账户号                  INTEGER              not null,
   最近访问日期               DATE,
   constraint PK_储蓄开户 primary key (身份证号, 名字, 账户号)
);

create table 储蓄_支行_客户
(
   身份证号                 varchar(20)             not null,
   名字                   varchar(20)             not null,
   constraint PK_储蓄_支行_客户 primary key (身份证号, 名字)
);

/*==============================================================*/
/* Table: 储蓄账户                                                  */
/*==============================================================*/
create table 储蓄账户 
(
   账户号                  INTEGER              not null,
   开户日期                 DATE,
   余额                   DECIMAL(8,2),
   货币类型                 varchar(50),
   利率                   DOUBLE,
   constraint PK_储蓄账户 primary key (账户号)
);


/*==============================================================*/
/* Table: 贷款开户                                                  */
/*==============================================================*/
create table 支票开户 
(
   身份证号                 varchar(20)             not null,
   名字                   varchar(20)             not null,
   账户号                  INTEGER              not null,
   最近访问日期_贷款            DATE,
   constraint PK_贷款开户 primary key (身份证号, 名字, 账户号)
);

create table 贷款_支行_客户
(
   身份证号                 varchar(20)             not null,
   名字                   varchar(20)             not null,
   constraint PK_贷款_支行_客户 primary key (身份证号, 名字)
);

/*==============================================================*/
/* Table: 贷款账户                                                  */
/*==============================================================*/
create table 支票账户 
(
   账户号                  INTEGER              not null,
   开户日期                 DATE,
   余额                   DECIMAL(8,2),
   透支额                  DECIMAL(8,2),
   constraint PK_贷款账户 primary key (账户号)
);


/*==============================================================*/
/* Table: 员工                                                    */
/*==============================================================*/
create table 员工 
(
   身份证号              varchar(20)             not null,
   员工_身份证号            varchar(20),
   姓名                  varchar(50),
   电话号码                varchar(50),
   家庭住址               varchar(50),
   开始工作日期              DATE,
   constraint PK_员工 primary key (身份证号)
);


/*==============================================================*/
/* Table: 客户                                                    */
/*==============================================================*/
create table 客户 
(
   客户身份证号                 varchar(20)             not null,
   身份证号                varchar(20),
   姓名                   varchar(50),
   联系电话                 varchar(50),
   家庭住址                 varchar(50),
   联系人姓名                varchar(50)                 not null,
   联系人手机号               varchar(50),
   联系人Email           varchar(50),
   联系人与客户关系             varchar(50),
   负责人类型                varchar(50),
   constraint PK_客户 primary key (客户身份证号)
);


/*==============================================================*/
/* Table: 债务                                                   */
/*==============================================================*/


/*==============================================================*/
/* Table: 支付情况                                                  */
/*==============================================================*/
create table 支付情况 
(
   贷款号                  INTEGER              not null,
   身份证号                 varchar(20)             not null,
   金额1                  DECIMAL(8,2),
   日期付款                 DATE,
   时间						VARCHAR(20),
   constraint PK_支付情况 primary key (贷款号, 身份证号,日期付款,时间)
);


/*==============================================================*/
/* Table: 支行                                                    */
/*==============================================================*/
create table 支行 
(
   城市                   varchar(20)             not null,
   名字                   varchar(20)             not null,
   资产                   DECIMAL(8,2)          not null,
   constraint PK_支行 primary key (名字)
);

/*==============================================================*/
/* Table: 账户                                                    */
/*==============================================================*/
create table 账户 
(
   账户号                  INTEGER              not null,
   开户日期                 DATE,
   余额                   DECIMAL(8,2),
   constraint PK_账户 primary key (账户号)
);

/*==============================================================*/
/* Table: 贷款                                                    */
/*==============================================================*/
create table 贷款 
(
   金额1                  DECIMAL(8,2),
   贷款号                  INTEGER              not null,
   名字                   varchar(20),
   constraint PK_贷款 primary key (贷款号)
);


alter table 储蓄开户
   add constraint FK_储蓄开户_储蓄开户_客户 foreign key (身份证号)
      references 客户 (客户身份证号);
      
alter table 储蓄_支行_客户
   add constraint FK_客户身份证号1 foreign key (身份证号)
      references 客户 (客户身份证号);

alter table 储蓄_支行_客户
   add constraint FK_支行1 foreign key (名字)
      references 支行 (名字);

alter table 储蓄开户
   add constraint FK_储蓄开户_储蓄开户2_支行 foreign key (名字)
      references 支行 (名字);

alter table 储蓄_支行_客户
   add constraint FK_支行2 foreign key (名字)
      references 支行 (名字);

alter table 储蓄_支行_客户
   add constraint FK_客户身份证号2 foreign key (身份证号)
      references 客户 (客户身份证号);
      
alter table 储蓄开户
   add constraint FK_储蓄开户_储蓄开户3_储蓄账户 foreign key (账户号)
      references 储蓄账户 (账户号);

alter table 储蓄账户
   add constraint FK_储蓄账户_INHERITAN_账户 foreign key (账户号)
      references 账户 (账户号);

alter table 员工
   add constraint FK_员工_领导_员工 foreign key (员工_身份证号)
      references 员工 (身份证号);

alter table 客户
   add constraint FK_客户_负责_员工 foreign key (身份证号)
      references 员工 (身份证号);

alter table 支付情况
   add constraint FK_支付情况_支付情况_贷款 foreign key (贷款号)
      references 贷款 (贷款号);

alter table 支付情况
   add constraint FK_支付情况_支付情况2_客户 foreign key (身份证号)
      references 客户 (客户身份证号);

alter table 贷款
   add constraint FK_贷款_拥有贷款_支行 foreign key (名字)
      references 支行 (名字);

alter table 支票开户
   add constraint FK_贷款开户_贷款开户_客户 foreign key (身份证号)
      references 客户 (客户身份证号);

alter table 支票开户
   add constraint FK_贷款开户_贷款开户2_支行 foreign key (名字)
      references 支行 (名字);

alter table 支票开户
   add constraint FK_贷款开户_贷款开户3_贷款账户 foreign key (账户号)
      references 支票账户 (账户号);

alter table 支票账户
   add constraint FK_贷款账户_INHERITAN_账户 foreign key (账户号)
      references 账户 (账户号);