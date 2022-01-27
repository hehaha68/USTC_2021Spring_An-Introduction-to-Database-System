# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/29 18:07
@Author  : 和泳毅
@FileName: models.py
@SoftWare: PyCharm
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 用户管理
class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), primary_key=True)
    userkey = db.Column(db.String(50), nullable=False)


# 账户
class Account(db.Model):
    __tablename__ = 'account'

    A_ID = db.Column(db.String(50), primary_key=True)
    B_Name = db.Column(db.ForeignKey('bank.B_Name', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False,
                       index=True)
    Balance = db.Column(db.Float)
    Opening_Date = db.Column(db.Date)

    bank = db.relationship('Bank', primaryjoin='Account.B_Name == Bank.B_Name', backref='accounts')


# 支票账户
class CheckingAccount(db.Model):
    __tablename__ = 'checking_account'

    A_ID = db.Column(db.ForeignKey('account.A_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
    Overdraft = db.Column(db.Float)


# 储蓄账户
class SavingAccount(db.Model):
    __tablename__ = 'saving_account'

    A_ID = db.Column(db.ForeignKey('account.A_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
    Interest_Rate = db.Column(db.Float)
    Currency_Type = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))


# 贷款发放
class Apply(db.Model):
    __tablename__ = 'apply'

    C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
                     nullable=False)
    L_ID = db.Column(db.ForeignKey('loan.L_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
                     nullable=False, index=True)
    P_ID = db.Column(db.String(50), primary_key=True)
    P_Amount = db.Column(db.Float)
    Pay_Date = db.Column(db.Date)

    client = db.relationship('Client', primaryjoin='Apply.C_ID == Client.C_ID', backref='applies')
    loan = db.relationship('Loan', primaryjoin='Apply.L_ID == Loan.L_ID', backref='applies')


# 支行
class Bank(db.Model):
    __tablename__ = 'bank'

    B_ID = db.Column(db.Integer, nullable=False, unique=True)
    B_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), primary_key=True)
    City = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False)
    Assets = db.Column(db.Float, nullable=False)


# 客户
class Client(db.Model):
    __tablename__ = 'client'

    C_ID = db.Column(db.String(50), primary_key=True)
    C_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False)
    C_Tel = db.Column(db.Integer)
    C_Addr = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))


# 联系人
class Contact(db.Model):
    __tablename__ = 'contact'

    C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
                     nullable=False)
    Co_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), primary_key=True, nullable=False)
    Co_Email = db.Column(db.String(50))
    Co_Tel = db.Column(db.Integer)
    Relation = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))

    client = db.relationship('Client', primaryjoin='Contact.C_ID == Client.C_ID', backref='contacts')


# 部门
class Department(db.Model):
    __tablename__ = 'department'

    D_ID = db.Column(db.String(50), primary_key=True)
    D_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False)
    D_Type = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))
    Manager_ID = db.Column(db.String(50))


# 雇员
class Employee(db.Model):
    __tablename__ = 'employee'

    E_ID = db.Column(db.String(50), primary_key=True)
    E_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False)
    B_Name = db.Column(db.ForeignKey('bank.B_Name', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False,
                       index=True)
    D_ID = db.Column(db.ForeignKey('department.D_ID', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    E_Tel = db.Column(db.Integer)
    E_Addr = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))
    Work_Date = db.Column(db.Date)

    bank = db.relationship('Bank', primaryjoin='Employee.B_Name == Bank.B_Name', backref='employees')
    department = db.relationship('Department', primaryjoin='Employee.D_ID == Department.D_ID', backref='employees')


# 贷款
class Loan(db.Model):
    __tablename__ = 'loan'

    L_ID = db.Column(db.String(50), primary_key=True)
    B_Name = db.Column(db.ForeignKey('bank.B_Name', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False,
                       index=True)
    L_Amount = db.Column(db.Float, nullable=False)
    L_Status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    P_already = db.Column(db.Float)

    bank = db.relationship('Bank', primaryjoin='Loan.B_Name == Bank.B_Name', backref='loans')


# 客户-账户
class Own(db.Model):
    __tablename__ = 'own'

    C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
                     nullable=False)
    Visited_Date = db.Column(db.Date)
    A_ID = db.Column(db.ForeignKey('account.A_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)

    account = db.relationship('Account', primaryjoin='Own.A_ID == Account.A_ID', backref='owns')
    client = db.relationship('Client', primaryjoin='Own.C_ID == Client.C_ID', backref='owns')


# 开户约束
class Checking(db.Model):
    __tablename__ = 'checking'

    C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
                     nullable=False)
    B_Name = db.Column(db.ForeignKey('bank.B_Name', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
                       nullable=False, index=True)
    A_Type = db.Column(db.Integer, primary_key=True, nullable=False)
    A_ID = db.Column(db.String(50), primary_key=True)

    bank = db.relationship('Bank', primaryjoin='Checking.B_Name == Bank.B_Name', backref='checkings')
    client = db.relationship('Client', primaryjoin='Checking.C_ID == Client.C_ID', backref='checkings')


# 服务关系
class Service(db.Model):
    __tablename__ = 'service'

    C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
                     nullable=False)
    E_ID = db.Column(db.ForeignKey('employee.E_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
                     nullable=False, index=True)
    S_Type = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))

    client = db.relationship('Client', primaryjoin='Service.C_ID == Client.C_ID', backref='services')
    employee = db.relationship('Employee', primaryjoin='Service.E_ID == Employee.E_ID', backref='services')
