/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2021/6/16 13:22:18                           */
/*==============================================================*/


drop table if exists Account;

drop table if exists Apply;

drop table if exists Bank;

drop table if exists Checking_Account;

drop table if exists Client;

drop table if exists Contact;

drop table if exists Department;

drop table if exists Employee;

drop table if exists Loan;

drop table if exists Own;

drop table if exists Payment;

drop table if exists Saving_Account;

drop table if exists Service;

/*==============================================================*/
/* Table: Account                                               */
/*==============================================================*/
create table Account
(
   A_ID          varchar(50) not null,
   B_Name        varchar(50) not null,
   Balance       float(15),
   Opening_Date  date,
   primary key (A_ID)
);

/*==============================================================*/
/* Table: Apply                                                 */
/*==============================================================*/
create table Apply
(
   C_ID         varchar(50) not null,
   L_ID         varchar(50) not null,
   P_ID         varchar(50) not null,
   P_Amount     float(15),
   Pay_Date     date,
   primary key (C_ID, L_ID, P_ID)
);

/*==============================================================*/
/* Table: Bank                                                  */
/*==============================================================*/
create table Bank(
   B_ID			int not null,
   B_Name       varchar(50) not null,
   City         varchar(50) not null,
   Assets       float(15) not null,
   primary key (B_Name),
   unique key AK_B_ID (B_ID));

/*==============================================================*/
/* Table: Checking_Account                                      */
/*==============================================================*/
create table Checking_Account
(
   A_ID         varchar(50) not null,
   Overdraft    float(15),
   primary key (A_ID)
);

/*==============================================================*/
/* Table: Client                                                */
/*==============================================================*/
create table Client
(
   C_ID         varchar(50) not null,
   C_Name       varchar(50) not null,
   C_Tel        int,
   C_Addr       varchar(50),
   primary key (C_ID)
);

/*==============================================================*/
/* Table: Contact                                               */
/*==============================================================*/
create table Contact
(
   C_ID         varchar(50) not null,
   Co_Name      varchar(50) not null,
   Co_Email     varchar(50),
   Co_Tel       int,
   Relation     varchar(50),
   primary key (C_ID, Co_Name)
);

/*==============================================================*/
/* Table: Department                                            */
/*==============================================================*/
create table Department
(
   D_ID         varchar(50) not null,
   D_Name       varchar(50) not null,
   D_Type       varchar(50),
   Manager_ID   varchar(50),
   primary key (D_ID)
);

/*==============================================================*/
/* Table: Employee                                              */
/*==============================================================*/
create table Employee
(
   E_ID         varchar(50) not null,
   E_Name       varchar(50) not null,
   B_Name       varchar(50) not null,
   D_ID         varchar(50),
   E_Tel        int,
   E_Addr       varchar(50),
   Work_Date    date,
   primary key (E_ID)
);

/*==============================================================*/
/* Table: Loan                                                  */
/*==============================================================*/
create table Loan
(
   L_ID         varchar(50) not null,
   B_Name       varchar(50) not null,
   L_Amount     float(15) not null,
   L_Status		int default 0 not null,
   P_already    float(15) not null,
   primary key (L_ID)
);

/*==============================================================*/
/* Table: Own                                                   */
/*==============================================================*/
create table Own
(
   C_ID         varchar(50) not null,
   Visited_Date date,
   A_ID         varchar(50),
   primary key (C_ID, A_ID)
);

/*==============================================================*/
/* Table: Checking                                        */
/*==============================================================*/
create table Checking
(
   C_ID         varchar(50) not null,
   B_Name       varchar(50) not null,
   A_Type       int not null,
   primary key (C_ID, B_Name, A_Type)
);

/*==============================================================*/
/* Table: Saving_Account                                        */
/*==============================================================*/
create table Saving_Account
(
   A_ID           varchar(50) not null,
   Interest_Rate  float(15),
   Currency_Type  varchar(50),
   primary key (A_ID)
);

/*==============================================================*/
/* Table: Service                                               */
/*==============================================================*/
create table Service
(
   C_ID         varchar(50) not null,
   E_ID         varchar(50) not null,
   S_Type       varchar(50),
   primary key (C_ID, E_ID)
);


alter table Account add constraint FK_Open foreign key (B_Name)
      references Bank (B_Name) on delete restrict on update restrict;

alter table Apply add constraint FK_Apply foreign key (C_ID)
      references Client (C_ID) on delete restrict on update restrict;

alter table Apply add constraint FK_Apply2 foreign key (L_ID)
      references Loan (L_ID) on delete restrict on update restrict;

alter table Checking_Account add constraint FK_Account_Type foreign key (A_ID)
      references Account (A_ID) on delete restrict on update restrict;

alter table Contact add constraint FK_Have foreign key (C_ID)
      references Client (C_ID) on delete restrict on update restrict;

alter table Employee add constraint FK_Belong_To foreign key (D_ID)
      references Department (D_ID) on delete restrict on update restrict;

alter table Employee add constraint FK_Employ foreign key (B_Name)
      references Bank (B_Name) on delete restrict on update restrict;

alter table Loan add constraint FK_Make_Loan foreign key (B_Name)
      references Bank (B_Name) on delete restrict on update restrict;

alter table Own add constraint FK_Own1 foreign key (C_ID)
      references Client (C_ID) on delete restrict on update restrict;

alter table Own add constraint FK_Own2 foreign key (A_ID)
      references Account (A_ID) on delete restrict on update restrict;

alter table Saving_Account add constraint FK_Account_Type2 foreign key (A_ID)
      references Account (A_ID) on delete restrict on update restrict;

alter table Service add constraint FK_Service foreign key (C_ID)
      references Client (C_ID) on delete restrict on update restrict;

alter table Service add constraint FK_Service2 foreign key (E_ID)
      references Employee (E_ID) on delete restrict on update restrict;

alter table Checking add constraint FK_Checking1 foreign key (C_ID)
      references Client (C_ID) on delete restrict on update restrict;

alter table Checking add constraint FK_Checking2 foreign key (B_Name)
      references Bank (B_Name) on delete restrict on update restrict;