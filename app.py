from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from sqlalchemy import Enum
from sqlalchemy import ForeignKey


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/Portal-job'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(255), nullable=False)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    name = db.Column(db.String(255), nullable=False)
    detail_company = db.Column(db.Text, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(255), nullable=False)

class Jobseeker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    name = db.Column(db.String(255), nullable=False)
    major = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    exprience = db.Column(db.String(255), nullable=True)
    name_company = db.Column(db.String(255), nullable=True)
    field_work = db.Column(db.Integer, nullable=True)

    timeline = db.relationship('Timeline', uselist=False, backref='jobseeker', lazy=True)
# class Job(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id_company = db.Column(db.Integer, nullable=False) 
#     name_job = db.Column(db.String(255), nullable=False)
#     detail = db.Column(db.Text, nullable=False)
#     exprience = db.Column(db.Integer, nullable=False)
#     date_posted = db.Column(db.Date, nullable=False)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_company = db.Column(db.Integer, db.ForeignKey('company.id'))
    name_job = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    exprience = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.Date, nullable=False)



# class CompanyJob(db.Model):
#     id_job = db.Column(db.Integer, ForeignKey('job.id'), primary_key=True)
#     id_company = db.Column(db.Integer, ForeignKey('company.id'), primary_key=True)


class CompanyJob(db.Model):
    id_job = db.Column(db.Integer, db.ForeignKey('job.id'), primary_key=True)
    id_company = db.Column(db.Integer, db.ForeignKey('company.id'), primary_key=True)


# class Timeline(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id_job = db.Column(db.Integer, nullable=False)
#     id_jobseeker = db.Column(db.Integer, nullable=False)
#     apply_job = db.Column(Enum("apply_status", name="apply_status", values=["pending", "accept", "rejected"]))

class Timeline(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_job = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    id_jobseeker = db.Column(db.Integer, db.ForeignKey('jobseeker.id'), nullable=False)
    apply_job = db.Column(Enum("apply_status", name="apply_status", values=["pending", "accept", "rejected"]))

if __name__ == "__main__":
    app.run(debug=True)