# -*- coding: utf-8 -*-
"""
@Time    : 2021/7/1 13:07
@Author  : 和泳毅
@FileName: app.py
@SoftWare: PyCharm
"""
from flask import Flask, render_template, request, abort
import config
import numpy as np
import datetime
from db_init import db, db2
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import func
from models import Bank, Client, Employee, SavingAccount, CheckingAccount, Loan, Apply, \
    Account, Contact, Department, Own, Service, Checking, User
import time

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

cursor = db2.cursor()


@app.route('/')
def hello_world():
    return render_template('login.html')


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if request.form.get('type') == 'signup':
            name = request.form.get('name')
            key = request.form.get('password')

            newUser = User(
                username=name,
                userkey=key,
            )

            db.session.add(newUser)
            db.session.commit()
            return render_template('login.html')
        elif request.form.get('type') == 'login':

            name = request.form.get('name')
            key = request.form.get('password')
            UserNotExist = db.session.query(User).filter_by(username=name).scalar() is None

            if UserNotExist == 1:
                error_title = '登录错误'
                error_message = '用户名不存在'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            user_result = db.session.query(User).filter_by(username=name).first()
            if user_result.userkey == key:
                return render_template('index.html')
            else:
                error_title = '登录错误'
                error_message = '密码错误'
                return render_template('404.html', error_title=error_title, error_message=error_message)
    return render_template('login.html')


@app.route('/index')
def index():
    return render_template('index.html')


# 支行管理
@app.route('/bank', methods=['GET', 'POST'])
def bank():
    labels = ['支行号', '支行名', '支行资产', '所在城市']
    result_query = db.session.query(Bank)
    result = result_query.all()
    if request.method == 'GET':
        return render_template('bank.html', labels=labels, content=result)
    else:
        if request.form.get('type') == 'query':
            bank_id = request.form.get('id')
            bank_name = request.form.get('name')
            bank_city = request.form.get('city')
            bank_asset = request.form.get('assets')

            if bank_id != "":
                result_query = result_query.filter(Bank.B_ID == bank_id)
            if bank_name != "":
                result_query = result_query.filter(Bank.B_Name == bank_name)
            if bank_asset != "":
                result_query = result_query.filter(Bank.Assets == bank_asset)
            if bank_city != "":
                result_query = result_query.filter(Bank.City == bank_city)

            result = result_query.all()

            return render_template('bank.html', labels=labels, content=result)

        elif request.form.get('type') == 'update':
            old_num = request.form.get('key')
            bank_name = request.form.get('bank_name')
            bank_asset = request.form.get('bank_asset')
            bank_city = request.form.get('bank_city')
            bank_result = db.session.query(Bank).filter_by(B_ID=old_num).first()
            bank_result.B_Name = bank_name
            bank_result.Assets = bank_asset
            bank_result.City = bank_city
            db.session.commit()

        elif request.form.get('type') == 'delete':
            old_num = request.form.get('key')

            BankNotExist = db.session.query(Employee).filter_by(B_Name=old_num).scalar() is None

            if BankNotExist != 1:
                error_title = '删除错误'
                error_message = '支行在存在关联员工'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            BankNotExist = db.session.query(Account).filter_by(B_Name=old_num).scalar() is None

            if BankNotExist != 1:
                error_title = '删除错误'
                error_message = '支行在存在关联账户'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            BankNotExist = db.session.query(Loan).filter_by(B_Name=old_num).scalar() is None

            if BankNotExist != 1:
                error_title = '删除错误'
                error_message = '支行在存在关联贷款'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            BankNotExist = db.session.query(Checking).filter_by(B_Name=old_num).scalar() is None

            if BankNotExist != 1:
                error_title = '删除错误'
                error_message = '支行在存在关联信息'
                return render_template('404.html', error_title=error_title, error_message=error_message)
            bank_result = db.session.query(Bank).filter_by(B_ID=old_num).first()
            db.session.delete(bank_result)
            db.session.commit()

        elif request.form.get('type') == 'insert':
            bank_id = request.form.get('id')
            bank_name = request.form.get('name')
            bank_asset = request.form.get('estate')
            bank_city = request.form.get('city')

            newBank = Bank(
                B_ID=bank_id,
                B_Name=bank_name,
                Assets=bank_asset,
                City=bank_city
            )

            db.session.add(newBank)
            db.session.commit()

    result = db.session.query(Bank).all()

    return render_template('bank.html', labels=labels, content=result)


# 客户管理
@app.route('/client', methods=['GET', 'POST'])
def client():
    labels1 = ['客户ID', '客户姓名', '客户电话', '客户住址', '联系人姓名', '联系人电话', '联系人邮箱', '关系']
    labels2 = ['客户ID', '员工ID', '服务类型']
    result_query1 = db.session.query(Client, Contact).filter(Client.C_ID == Contact.C_ID)
    result_query2 = db.session.query(Client, Service).filter(Client.C_ID == Service.C_ID)
    result1 = result_query1.all()
    result2 = result_query2.all()

    if request.method == 'GET':
        return render_template('client.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
    else:
        if request.form.get('type') == 'query1':
            clientID = request.form.get('clientID')
            clientName = request.form.get('name')
            clientPhone = request.form.get('phone')
            clientAddress = request.form.get('address')
            coname = request.form.get('cname')
            cophone = request.form.get('cphone')
            coemail = request.form.get('cemail')
            corelation = request.form.get('crelation')

            if clientID != '':
                result_query1 = result_query1.filter(Client.C_ID == clientID)
            if clientName != '':
                result_query1 = result_query1.filter(Client.C_Name == clientName)
            if clientPhone != '':
                result_query1 = result_query1.filter(Client.C_Tel == clientPhone)
            if clientAddress != '':
                result_query1 = result_query1.filter(Client.C_Addr == clientAddress)
            if coname != '':
                result_query1 = result_query1.filter(Contact.Co_Name == coname)
            if cophone != '':
                result_query1 = result_query1.filter(Contact.Co_Tel == cophone)
            if coemail != '':
                result_query1 = result_query1.filter(Contact.Co_Email == coemail)
            if corelation != '':
                result_query1 = result_query1.filter(Contact.Relation == corelation)

            result1 = result_query1.all()

            return render_template('client.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)

        elif request.form.get('type') == 'query2':
            clientID = request.form.get('clientID')
            employeeID = request.form.get('staffId')
            stype = request.form.get('Type')

            if clientID != '':
                result_query2 = result_query2.filter(Service.C_ID == clientID)
            if employeeID != '':
                result_query2 = result_query2.filter(Service.E_ID == employeeID)
            if stype != '':
                result_query2 = result_query2.filter(Service.S_Type == stype)

            result2 = result_query2.all()

            return render_template('client.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)

        elif request.form.get('type') == 'update1':
            clientID = request.form.get('key')
            clientName = request.form.get('name')
            clientPhone = request.form.get('phone')
            clientAddress = request.form.get('address')
            coname = request.form.get('cname')
            cophone = request.form.get('cphone')
            coemail = request.form.get('cemail')
            corelation = request.form.get('crelation')
            Client_result = db.session.query(Client).filter_by(C_ID=clientID).first()
            Contact_result = db.session.query(Contact).filter_by(C_ID=clientID).first()
            Client_result.C_Name = clientName
            Client_result.C_Tel = clientPhone
            Client_result.C_Addr = clientAddress
            Contact_result.Co_Name = coname
            Contact_result.Co_Email = coemail
            Contact_result.Co_Tel = cophone
            Contact_result.Relation = corelation

            db.session.commit()

        elif request.form.get('type') == 'update2':
            clientID = request.form.get('key')
            employeeID = request.form.get('staffId')
            stype = request.form.get('Type')

            Service_result = db.session.query(Service).filter_by(C_ID=clientID).first()
            Service_result.E_ID = employeeID
            Service_result.S_Type = stype

            db.session.commit()

        elif request.form.get('type') == 'delete1':
            clientID = request.form.get('key')
            client_result = db.session.query(Client).filter_by(C_ID=clientID).first()
            contact_result = db.session.query(Contact).filter_by(C_ID=clientID).first()
            service_result = db.session.query(Service).filter_by(C_ID=clientID).first()

            CheckingNotExist = db.session.query(Checking).filter_by(C_ID=clientID).scalar() is None

            if CheckingNotExist != 1:
                error_title = '删除错误'
                error_message = '客户在存在关联账户'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            ApplyNotExist = db.session.query(Apply).filter_by(C_ID=clientID).scalar() is None

            if ApplyNotExist != 1:
                error_title = '删除错误'
                error_message = '客户在存在贷款记录'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            serviceNotExist = db.session.query(Service).filter_by(C_ID=clientID).scalar() is None

            if serviceNotExist != 1:
                db.session.delete(service_result)
                db.session.commit()

            db.session.delete(contact_result)
            db.session.commit()

            db.session.delete(client_result)
            db.session.commit()

        elif request.form.get('type') == 'delete2':
            clientID = request.form.get('key')
            service_result = db.session.query(Service).filter_by(C_ID=clientID).first()

            db.session.delete(service_result)
            db.session.commit()

        elif request.form.get('type') == 'insert2':
            clientID = request.form.get('clientID')
            employeeID = request.form.get('staffId')
            stype = request.form.get('Type')

            newService = Service(
                C_ID=clientID,
                E_ID=employeeID,
                S_Type=stype
            )

            db.session.add(newService)
            db.session.commit()

            result2 = db.session.query(Client, Service).filter(Client.C_ID == Service.C_ID).all()

            return render_template('client.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)

        elif request.form.get('type') == 'insert1':
            clientID = request.form.get('clientID')
            clientName = request.form.get('name')
            clientPhone = request.form.get('phone')
            clientAddress = request.form.get('address')
            coname = request.form.get('cname')
            cophone = request.form.get('cphone')
            coemail = request.form.get('cemail')
            corelation = request.form.get('crelation')

            newClient = Client(
                C_ID=clientID,
                C_Name=clientName,
                C_Tel=clientPhone,
                C_Addr=clientAddress
            )

            newContact = Contact(
                C_ID=clientID,
                Co_Name=coname,
                Co_Tel=cophone,
                Co_Email=coemail,
                Relation=corelation
            )

            db.session.add(newClient)
            db.session.add(newContact)
            db.session.commit()

    result1 = db.session.query(Client, Contact).filter(Client.C_ID == Contact.C_ID).all()
    return render_template('client.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)


# 员工管理
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    labels1 = ['员工ID', '员工姓名', '员工电话', '员工住址', '雇佣日期', '所在支行', '部门号', '部门名称', '部门类型', '部门经理ID']
    labels2 = ['部门号', '部门名称', '部门类型', '部门经理ID']
    result_query = db.session.query(Employee, Department).filter(Employee.D_ID == Department.D_ID)
    result = result_query.all()

    result_query2 = db.session.query(Department)
    result2 = result_query2.all()

    if request.method == 'GET':
        return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)
    else:
        if request.form.get('type') == 'query1':
            ID = request.form.get('staffID')
            name = request.form.get('name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            date = request.form.get('date')
            Bank = request.form.get('bank')
            departID = request.form.get('departId')
            departName = request.form.get('departName')
            departType = request.form.get('departType')
            ManagerID = request.form.get('ManagerId')

            if ID != '':
                result_query = result_query.filter(Employee.E_ID == ID)
            if name != '':
                result_query = result_query.filter(Employee.E_Name == name)
            if phone != '':
                result_query = result_query.filter(Employee.E_Tel == phone)
            if address != '':
                result_query = result_query.filter(Employee.E_Addr == address)
            if date != '':
                date = date.split('-')
                date = datetime.date(
                    int(date[0]), int(date[1]), int(date[2]))
                result_query = result_query.filter(Employee.Work_Date == date)
            if Bank != '':
                result_query = result_query.filter(Employee.B_Name == Bank)
            if departID != '':
                result_query = result_query.filter(Employee.D_ID == departID)
            if departName != '':
                result_query = result_query.filter(Department.D_Name == departName)
            if departType != '':
                result_query = result_query.filter(Department.D_Type == departType)
            if ManagerID != '':
                result_query = result_query.filter(Department.Manager_ID == ManagerID)

            result = result_query.all()

            return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)

        elif request.form.get('type') == 'query2':
            departID = request.form.get('departId')
            departName = request.form.get('departName')
            departType = request.form.get('departType')
            ManagerID = request.form.get('ManagerId')

            if departID != '':
                result_query2 = result_query2.filter(Employee.D_ID == departID)
            if departName != '':
                result_query2 = result_query2.filter(Department.D_Name == departName)
            if departType != '':
                result_query2 = result_query2.filter(Department.D_Type == departType)
            if ManagerID != '':
                result_query2 = result_query2.filter(Department.Manager_ID == ManagerID)

            result = result_query.all()
            result2 = result_query2.all()

            return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)

        elif request.form.get('type') == 'update1':
            oldID = request.form.get('key')

            phone = request.form.get('phone')
            address = request.form.get('address')
            Bank = request.form.get('bank')
            departID = request.form.get('departId')

            employee_result = db.session.query(Employee).filter_by(E_ID=oldID).first()

            employee_result.D_ID = departID
            employee_result.B_Name = Bank
            employee_result.E_Tel = phone
            employee_result.E_Addr = address

            db.session.commit()

        elif request.form.get('type') == 'update2':
            oldID = request.form.get('key')

            departName = request.form.get('departName')
            departType = request.form.get('departType')
            ManagerID = request.form.get('ManagerId')

            Department_result = db.session.query(Department).filter_by(D_ID=oldID).first()

            Department_result.D_Name = departName
            Department_result.D_Type = departType
            Department_result.Manager_ID = ManagerID

            db.session.commit()

        elif request.form.get('type') == 'delete1':
            oldID = request.form.get('key')

            EmployeeNotExist = db.session.query(Service).filter_by(E_ID=oldID).scalar() is None

            if EmployeeNotExist != 1:
                error_title = '删除错误'
                error_message = '员工在存在关联服务关系'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            employee_result = db.session.query(Employee).filter_by(E_ID=oldID).first()

            db.session.delete(employee_result)
            db.session.commit()

        elif request.form.get('type') == 'delete2':
            oldID = request.form.get('key')

            DepartmentNotExist = db.session.query(Employee).filter_by(D_ID=oldID).scalar() is None

            if DepartmentNotExist != 1:
                error_title = '删除错误'
                error_message = '部门在存在关联员工'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            Department_result = db.session.query(Department).filter_by(D_ID=oldID).first()

            db.session.delete(Department_result)
            db.session.commit()

        elif request.form.get('type') == 'insert1':
            ID = request.form.get('staffID')
            name = request.form.get('name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            date = request.form.get('date')
            Bank = request.form.get('bank')
            departID = request.form.get('departId')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))

            newStaff = Employee(
                E_ID=ID,
                D_ID=departID,
                E_Name=name,
                B_Name=Bank,
                E_Tel=phone,
                E_Addr=address,
                Work_Date=date
            )

            db.session.add(newStaff)
            db.session.commit()
            result = db.session.query(Employee, Department).filter(Employee.D_ID == Department.D_ID).all()
            return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)

        elif request.form.get('type') == 'insert2':
            departID = request.form.get('departId')
            departName = request.form.get('departName')
            departType = request.form.get('departType')
            ManagerID = request.form.get('ManagerId')

            newDepartment = Department(
                D_ID=departID,
                D_Name=departName,
                D_Type=departType,
                Manager_ID=ManagerID,
            )

            db.session.add(newDepartment)
            db.session.commit()

    result = db.session.query(Employee, Department).filter(Employee.D_ID == Department.D_ID).all()
    result2 = db.session.query(Department).all()
    return render_template('employee.html', labels1=labels1, labels2=labels2, content=result, content2=result2)


# 账户管理
@app.route('/account', methods=['GET', 'POST'])
def account():
    labels1 = ['账户号', '客户ID', '客户姓名', '开户支行', '开户时间', '账户余额', '最近访问时间', '利率', '货币类型']
    labels2 = ['账户号', '客户ID', '客户姓名', '开户支行', '开户时间', '账户余额', '最近访问时间', '透支额度']

    content1_query = db.session.query(Account, SavingAccount, Own, Client).filter(
        Account.A_ID == SavingAccount.A_ID).filter(
        Own.A_ID == Account.A_ID).filter(Client.C_ID == Own.C_ID)
    content2_query = db.session.query(CheckingAccount, Account, Own, Client).filter(
        CheckingAccount.A_ID == Account.A_ID).filter(
        Account.A_ID == Own.A_ID).filter(Own.C_ID == Client.C_ID)

    content1 = content1_query.all()
    content2 = content2_query.all()

    if request.method == 'GET':
        return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)
    else:
        if request.form.get('type') == 'squery':
            accID = request.form.get('accId')
            clientID = request.form.get('clientID')
            clientName = request.form.get('clientName')
            BankName = request.form.get('bank')
            openDate = request.form.get('openDate')
            balance = request.form.get('balance')
            VisitedDate = request.form.get('VisitDate')
            interestRate = request.form.get('interest')
            currType = request.form.get('currType')

            if accID != "":
                content1_query = content1_query.filter(Account.A_ID == accID)
            if clientID != "":
                content1_query = content1_query.filter(Client.C_ID == clientID)
            if clientName != "":
                content1_query = content1_query.filter(Client.C_Name == clientName)
            if BankName != "":
                content1_query = content1_query.filter(Account.B_Name == BankName)
            if openDate != "":
                openDate = openDate.split('-')
                openDate = datetime.date(
                    int(openDate[0]), int(openDate[1]), int(openDate[2]))
                content1_query = content1_query.filter(Account.Opening_Date == openDate)
            if VisitedDate != "":
                VisitedDate = VisitedDate.split('-')
                VisitedDate = datetime.date(
                    int(VisitedDate[0]), int(VisitedDate[1]), int(VisitedDate[2]))
                content1_query = content1_query.filter(Own.Visited_Date == VisitedDate)
            if balance != "":
                content1_query = content1_query.filter(Account.Balance == float(balance))
            if interestRate != "":
                content1_query = content1_query.filter(SavingAccount.Interest_Rate == float(interestRate))
            if currType != "":
                content1_query = content1_query.filter(SavingAccount.Currency_Type == currType)

            content1 = content1_query.all()

            return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1,
                                   content2=content2)

        elif request.form.get('type') == 'cquery':
            accID = request.form.get('accId')
            clientID = request.form.get('clientID')
            clientName = request.form.get('clientName')
            BankName = request.form.get('bank')
            openDate = request.form.get('openDate')
            balance = request.form.get('balance')
            VisitedDate = request.form.get('VisitDate')
            overDraft = request.form.get('overDraft')

            if accID != "":
                content2_query = content2_query.filter(Account.A_ID == accID)
            if clientID != "":
                content2_query = content2_query.filter(Client.C_ID == clientID)
            if clientName != "":
                content2_query = content2_query.filter(Client.C_Name == clientName)
            if BankName != "":
                content2_query = content2_query.filter(Account.B_Name == BankName)
            if openDate != "":
                openDate = openDate.split('-')
                openDate = datetime.date(
                    int(openDate[0]), int(openDate[1]), int(openDate[2]))
                content2_query = content2_query.filter(Account.Opening_Date == openDate)
            if VisitedDate != "":
                VisitedDate = VisitedDate.split('-')
                VisitedDate = datetime.date(
                    int(VisitedDate[0]), int(VisitedDate[1]), int(VisitedDate[2]))
                content2_query = content2_query.filter(Own.Visited_Date == VisitedDate)
            if balance != "":
                content2_query = content2_query.filter(Account.Balance == float(balance))
            if overDraft != "":
                content2_query = content2_query.filter(CheckingAccount.Overdraft == float(overDraft))

            content2 = content2_query.all()

            return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1,
                                   content2=content2)

        elif request.form.get('type') == 'saddAcc':
            accID = request.form.get('accId')
            clientID = request.form.get('clientID')
            BankName = request.form.get('bank')
            openDate = request.form.get('openDate')
            balance = request.form.get('balance')
            interestRate = request.form.get('interest')
            currType = request.form.get('currType')

            openDate = openDate.split('-')
            openDate = datetime.date(
                int(openDate[0]), int(openDate[1]), int(openDate[2]))

            VisitedDate = time.strftime("%Y-%m-%d", time.localtime()).split('-')
            VisitedDate = datetime.date(
                int(VisitedDate[0]), int(VisitedDate[1]), int(VisitedDate[2]))

            CheckingNotExist = db.session.query(Checking).filter_by(C_ID=clientID).filter_by(
                B_Name=BankName).filter_by(A_Type=1).scalar() is None

            if CheckingNotExist != 1:
                error_title = '开户错误'
                error_message = '客户在该银行已存在一个储蓄账户'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            newChecking = Checking(
                C_ID=clientID,
                B_Name=BankName,
                A_Type=1,
                A_ID=accID,
            )
            db.session.add(newChecking)
            db.session.commit()

            AccountNotExist = db.session.query(Account.A_ID).filter_by(A_ID=accID).scalar()
            if AccountNotExist is None:
                newAccount = Account(
                    A_ID=accID,
                    B_Name=BankName,
                    Balance=balance,
                    Opening_Date=openDate,
                )

                db.session.add(newAccount)
                db.session.commit()

                newLilAccount = SavingAccount(
                    A_ID=accID,
                    Interest_Rate=interestRate,
                    Currency_Type=currType
                )
                db.session.add(newLilAccount)
                db.session.commit()

            newOwn = Own(
                C_ID=clientID,
                Visited_Date=VisitedDate,
                A_ID=accID,
            )

            db.session.add(newOwn)
            db.session.commit()

        elif request.form.get('type') == 'caddAcc':
            accID = request.form.get('accId')
            clientID = request.form.get('clientID')
            BankName = request.form.get('bank')
            openDate = request.form.get('openDate')
            balance = request.form.get('balance')
            overDraft = request.form.get('overDraft')

            openDate = openDate.split('-')
            openDate = datetime.date(
                int(openDate[0]), int(openDate[1]), int(openDate[2]))

            VisitedDate = time.strftime("%Y-%m-%d", time.localtime()).split('-')
            VisitedDate = datetime.date(
                int(VisitedDate[0]), int(VisitedDate[1]), int(VisitedDate[2]))

            CheckingNotExist = db.session.query(Checking).filter_by(C_ID=clientID).filter_by(
                B_Name=BankName).filter_by(A_Type=0).scalar() is None

            if CheckingNotExist != 1:
                error_title = '开户错误'
                error_message = '客户在该银行已存在一个支票账户'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            newChecking = Checking(
                C_ID=clientID,
                B_Name=BankName,
                A_Type=0,
                A_ID=accID,
            )
            db.session.add(newChecking)
            db.session.commit()

            AccountNotExist = db.session.query(Account.A_ID).filter_by(A_ID=accID).scalar()
            if AccountNotExist is None:
                newAccount = Account(
                    A_ID=accID,
                    B_Name=BankName,
                    Balance=balance,
                    Opening_Date=openDate,
                )
                db.session.add(newAccount)
                db.session.commit()

                newLilAccount = CheckingAccount(
                    A_ID=accID,
                    Overdraft=overDraft,
                )
                db.session.add(newLilAccount)
                db.session.commit()

            newOwn = Own(
                C_ID=clientID,
                Visited_Date=VisitedDate,
                A_ID=accID,
            )
            db.session.add(newOwn)
            db.session.commit()

        elif request.form.get('type') == 'supdate':
            oldAccount = request.form.get('key')
            balance = request.form.get('sBalance')
            interestRate = request.form.get('sInterest')
            currType = request.form.get('sCType')

            SavingAccount_result = db.session.query(SavingAccount).filter_by(A_ID=oldAccount).first()
            Account_result = db.session.query(Account).filter_by(A_ID=oldAccount).first()

            Account_result.Balance = balance
            SavingAccount_result.Interest_Rate = interestRate
            SavingAccount_result.Currency_Type = currType
            db.session.commit()

        elif request.form.get('type') == 'cupdate':
            oldAccount = request.form.get('key')
            balance = request.form.get('cBalance')
            overDraft = request.form.get('cOver')

            CheckingAccount_result = db.session.query(CheckingAccount).filter_by(A_ID=oldAccount).first()
            Account_result = db.session.query(Account).filter_by(A_ID=oldAccount).first()

            Account_result.Balance = balance
            CheckingAccount_result.Overdraft = overDraft
            db.session.commit()

        elif request.form.get('type') == 'sdelete':
            oldAccount = request.form.get('key')

            Account_result = db.session.query(Account).filter_by(A_ID=oldAccount).first()
            SavingAccount_result = db.session.query(SavingAccount).filter_by(A_ID=oldAccount).first()
            Own_result = db.session.query(Own).filter_by(A_ID=oldAccount).first()

            db.session.delete(Own_result)
            db.session.commit()

            db.session.delete(SavingAccount_result)
            db.session.commit()

            db.session.delete(Account_result)
            db.session.commit()

        elif request.form.get('type') == 'cdelete':
            oldAccount = request.form.get('key')

            Account_result = db.session.query(Account).filter_by(A_ID=oldAccount).first()
            CheckingAccount_result = db.session.query(CheckingAccount).filter_by(A_ID=oldAccount).first()
            Own_result = db.session.query(Own).filter_by(A_ID=oldAccount).first()

            db.session.delete(Own_result)
            db.session.commit()

            db.session.delete(CheckingAccount_result)
            db.session.commit()

            db.session.delete(Account_result)
            db.session.commit()

    content1 = db.session.query(Account, SavingAccount, Own, Client).filter(
        Account.A_ID == SavingAccount.A_ID).filter(
        Own.A_ID == Account.A_ID).filter(Client.C_ID == Own.C_ID).all()
    content2 = db.session.query(CheckingAccount, Account, Own, Client).filter(
        CheckingAccount.A_ID == Account.A_ID).filter(
        Account.A_ID == Own.A_ID).filter(Own.C_ID == Client.C_ID).all()

    return render_template('account.html', labels1=labels1, labels2=labels2, content1=content1, content2=content2)


# 贷款管理
@app.route('/debt', methods=['GET', 'POST'])
def debt():
    labels1 = ['贷款号', '发放支行', '贷款金额', '贷款状态']
    labels2 = ['支付号', '贷款号', '客户ID', '支付金额', '支付日期']

    content_query1 = db.session.query(Loan)
    content_query2 = db.session.query(Apply)
    result1 = content_query1.all()
    result2 = content_query2.all()

    if request.method == 'GET':
        return render_template('debt.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
    else:
        if request.form.get('type') == 'main_query':
            num = request.form.get('num')
            Bank = request.form.get('bank')
            money = request.form.get('money')
            state = request.form.get('state')

            if num != '':
                content_query1 = content_query1.filter(Loan.L_ID == num)
            if Bank != '':
                content_query1 = content_query1.filter(Loan.B_Name == Bank)
            if money != '':
                content_query1 = content_query1.filter(Loan.L_Amount == money)
            if state != '':
                content_query1 = content_query1.filter(Loan.L_Status == state)

            result1 = content_query1.all()

            return render_template('debt.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)

        elif request.form.get('type') == 'update':
            oldNum = request.form.get('key')
            money = request.form.get('money')
            date = request.form.get('date')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))

            Apply_result = db.session.query(Apply).filter_by(P_ID=oldNum).first()
            Loan_result = db.session.query(Loan).filter_by(L_ID=Apply_result.L_ID).first()
            sum_money = Loan_result.P_already - Apply_result.P_Amount

            if Loan_result.L_Status == 1:
                if sum_money + float(money) <= Loan_result.L_Amount:
                    Loan_result.P_already = sum_money + float(money)
                    Apply_result.P_Amount = money
                    Apply_result.Pay_Date = date

                    db.session.commit()
                    if sum_money + float(money) == Loan_result.L_Amount:
                        Loan_result.L_Status = 2

                        db.session.commit()
                else:
                    error_title = '更新错误'
                    error_message = '支付总金额大于贷款金额'
                    return render_template('404.html', error_title=error_title, error_message=error_message)
            else:
                error_title = '更新错误'
                error_message = '只能更新正在发放的贷款信息'
                return render_template('404.html', error_title=error_title, error_message=error_message)

        elif request.form.get('type') == 'delete':
            oldNum = request.form.get('key')

            loan_result = db.session.query(Loan).filter_by(L_ID=oldNum).first()

            if loan_result.L_Status == 1:
                error_title = '删除错误'
                error_message = '不可删除正在发放的贷款信息'
                return render_template('404.html', error_title=error_title, error_message=error_message)
            elif loan_result.L_Status == 2:
                Apply_result = db.session.query(Apply).filter_by(L_ID=oldNum).delete()
                db.session.commit()
            db.session.delete(loan_result)
            db.session.commit()

        elif request.form.get('type') == 'insert':
            num = request.form.get('num')
            Bank = request.form.get('bank')
            money = request.form.get('money')

            newLoan = Loan(
                L_ID=num,
                B_Name=Bank,
                L_Amount=money,
                L_Status=0,
                P_already=0,
            )

            db.session.add(newLoan)
            db.session.commit()

        elif request.form.get('type') == 'query':
            loanNum = request.form.get('loanNum')
            clientID = request.form.get('clientID')
            payID = request.form.get('payID')
            date = request.form.get('date')
            money = request.form.get('money')

            if loanNum != '':
                content_query2 = content_query2.filter(Apply.L_ID == loanNum)
            if clientID != '':
                content_query2 = content_query2.filter(Apply.C_ID == clientID)
            if payID != '':
                content_query2 = content_query2.filter(Apply.P_ID == payID)
            if date != '':
                content_query2 = content_query2.filter(Apply.Pay_Date == date)
            if money != '':
                content_query2 = content_query2.filter(Apply.P_Amount == money)

            result2 = content_query2.all()

            return render_template('debt.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)

        elif request.form.get('type') == 'give':
            loanNum = request.form.get('loanNum')
            clientID = request.form.get('clientID')
            payID = request.form.get('payID')
            date = request.form.get('date')
            money = request.form.get('money')

            date = date.split('-')
            date = datetime.date(
                int(date[0]), int(date[1]), int(date[2]))

            Loan_result = db.session.query(Loan).filter_by(L_ID=loanNum).first()

            if Loan_result.L_Status == 0:
                if float(money) <= Loan_result.L_Amount:
                    Loan_result.L_Status = 1
                    Loan_result.P_already = money

                    newApply = Apply(
                        C_ID=clientID,
                        L_ID=loanNum,
                        P_ID=payID,
                        P_Amount=money,
                        Pay_Date=date
                    )
                    db.session.add(newApply)
                    db.session.commit()
                    if float(money) == Loan_result.L_Amount:
                        Loan_result.L_Status = 2

                        db.session.commit()

                else:
                    error_title = '发放错误'
                    error_message = '支付总金额大于贷款金额'
                    return render_template('404.html', error_title=error_title, error_message=error_message)

            elif Loan_result.L_Status == 1:

                sum_money = Loan_result.P_already

                if sum_money + float(money) <= Loan_result.L_Amount:
                    Loan_result.P_already = sum_money + float(money)

                    newApply = Apply(
                        C_ID=clientID,
                        L_ID=loanNum,
                        P_ID=payID,
                        P_Amount=money,
                        Pay_Date=date
                    )

                    db.session.add(newApply)
                    db.session.commit()
                    if sum_money + float(money) == Loan_result.L_Amount:
                        Loan_result.L_Status = 2
                        db.session.commit()

                else:
                    error_title = '发放错误'
                    error_message = '支付总金额大于贷款金额'
                    return render_template('404.html', error_title=error_title, error_message=error_message)
            else:
                error_title = '发放错误'
                error_message = '贷款已发放完毕'
                return render_template('404.html', error_title=error_title, error_message=error_message)

    content_query1 = db.session.query(Loan)
    content_query2 = db.session.query(Apply)
    result1 = content_query1.all()
    result2 = content_query2.all()

    return render_template('debt.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)


# 业务统计
@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    bank_list = [['蜀山路支行', 100, 100, 100, 100], ['肥西路支行', 100, 100, 100, 100],
                 ['朝阳区支行', 100, 100, 100, 100], ['天府路支行', 100, 100, 100, 100]]

    bank_all = db.session.query(Bank).all()
    new_bank_list = []
    for i in bank_all:
        new_bank_list.append([i.B_Name])

    if request.method == 'GET':
        return render_template('statistics.html', bank_list=bank_list)
    else:
        # i[0]: 支行名
        # i[1]: 储蓄总额
        # i[2]: 贷款总额
        # i[3]: 储蓄总人
        # i[4]: 贷款总人
        if request.form.get('type') == 'year':

            year = request.form.get('year1')

            if int(year) > 2021 or int(year) < 1990:
                error_title = '输入错误'
                error_message = '年份输入错误'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            for i in new_bank_list:
                cx = cursor.callproc('cxyear', (int(year), i[0], None, None))
                dk = cursor.callproc('dkyear', (int(year), i[0], None, None))
                i.append(cx[2])  # i[1]
                i.append(dk[2])  # i[2]
                i.append(cx[3])  # i[3]
                i.append(dk[3])  # i[4]

        elif request.form.get('type') == 'season':

            year = request.form.get('year2')
            season = request.form.get('season')

            if int(year) > 2021 or int(year) < 1990:
                error_title = '输入错误'
                error_message = '年份输入错误'
                return render_template('404.html', error_title=error_title, error_message=error_message)
            if int(season) > 4 or int(season) < 1:
                error_title = '输入错误'
                error_message = '季度输入错误'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            for i in new_bank_list:
                cx = cursor.callproc('cxseason', (int(year), int(season), i[0], None, None))
                dk = cursor.callproc('dkseason', (int(year), int(season), i[0], None, None))
                i.append(cx[3])  # i[1]
                i.append(dk[3])  # i[2]
                i.append(cx[4])  # i[3]
                i.append(dk[4])  # i[4]

        elif request.form.get('type') == 'month':

            year = request.form.get('year3')
            month = request.form.get('month')

            if int(year) > 2021 or int(year) < 1990:
                error_title = '输入错误'
                error_message = '年份输入错误'
                return render_template('404.html', error_title=error_title, error_message=error_message)
            if int(month) > 12 or int(month) < 1:
                error_title = '输入错误'
                error_message = '月份输入错误'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            for i in new_bank_list:
                ck = cursor.callproc('cxmonth', (int(year), int(month), i[0], None, None))
                dk = cursor.callproc('dkmonth', (int(year), int(month), i[0], None, None))
                i.append(ck[3])  # i[1]
                i.append(dk[3])  # i[2]
                i.append(ck[4])  # i[3]
                i.append(dk[4])  # i[4]

    bank_list = new_bank_list
    return render_template('statistics.html', bank_list=bank_list)


@app.route('/404')
def not_found():
    return render_template('404.html', error_title='错误标题', error_message='错误信息')


@app.errorhandler(Exception)
def err_handle(e):
    error_message = ''
    error_title = ''
    if (type(e) == IndexError):
        error_title = '填写错误'
        error_message = '日期格式错误! (yyyy-mm-dd)'
    elif (type(e) == AssertionError):
        error_title = '删除错误'
        error_message = '删除条目仍有依赖！'
    elif (type(e) == sqlalchemy.exc.IntegrityError):
        error_title = '更新/插入错误'
        error_message = str(e._message())
    return render_template('404.html', error_title=error_title, error_message=error_message)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)