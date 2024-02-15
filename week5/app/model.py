from app import db

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32), nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)

    loans = db.relationship('Loan', backref='student', lazy='dynamic')

    def __repr__(self):
        return f"student('{self.username}', '{self.lastname}', '{self.firstname}' , '{self.email}')"

class Device(db.Model):
    __tablename__ = 'devices'
    device_id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(20), nullable=False, unique=True, index=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True) #是否激活
    loans = db.relationship('Loan', backref='device', lazy='dynamic')

    def __repr__(self):
        return f"device('{self.device_id},'{self.device_name}','{self.is_active}')"


class Loan(db.Model):
    __tablename__ = 'loans'
    loan_id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.device_id'), nullable=False)
    borrowdatetime = db.Column(db.DateTime, nullable=False)
    returndatetime = db.Column(db.DateTime, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)

    # device = db.relationship('Device', back_populates="loans")

    def __repr__(self):
        return f"loan('{self.device_id}', '{self.borrowdatetime}' , '{self.returndatetime}', '{self.student}')"



