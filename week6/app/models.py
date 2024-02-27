from app import db


class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32), nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    loans = db.relationship('Loan', backref='student', lazy='dynamic')
    is_active = db.Column(db.Boolean, default=True)

    # Loan指定另一个关系中的模型名称
    # backref 反向引用 使得在Loan数据库中可以访问Student类中相同的对象
    # dynamic 指定关系的加载方式 这种方式不会立即从数据库加载所有相关对象，而是等到你实际访问它们时才加载。

    # relationship 表示数据库模型之间的关系定义 需要有相对应的


    def __repr__(self):
        return f"student('{self.username}', '{self.lastname}', '{self.firstname}' , '{self.email}')"


class Loan(db.Model):
    __tablename__ = 'loans'
    loan_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    device_id = db.Column(db.Integer, nullable=False)
    borrowdatetime = db.Column(db.DateTime, nullable=False)
    returndatetime = db.Column(db.DateTime, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    # 模型之间通过student_id相互连接

    def __repr__(self):
        return f"loan('{self.device_id}', '{self.borrowdatetime}' , '{self.returndatetime}', '{self.student}')"



class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String())
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    bankaccounts = db.relationship('BankAccount', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"user('{self.username}', '{self.email}"

class BankAccount(db.Model):
    __tablename__ = 'bankaccounts'
    bank_account_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    bank_name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    account_deposit = db.Column(db.Integer, nullable=False)
    transaction = db.relationship('Transaction', backref='bankaccount', lazy='dynamic')

    def __repr__(self):
        return f"bankaccount('{self.bank_name}', '{self.bank_id}', '{self.bank_user_id},{self.account_deposit})"

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bankaccounts.bank_account_id'), nullable=False)
    object_id = db.Column(db.Integer, nullable=False)
    account_withdraw = db.Column(db.Integer)
    account_deposit = db.Column(db.Integer)
    transaction_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"transaction ('{self.transaction_id}', '{self.bank_id}', '{self.amount}', '{self.transaction_date}')"



