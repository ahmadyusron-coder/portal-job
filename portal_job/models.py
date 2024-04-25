from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from sqlalchemy import Enum
from sqlalchemy import func
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/portal-job'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    def is_active(self):
        return True
    def get_id(self):
        return self.id
    def is_authenticated(self):
        return True
    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    name = db.Column(db.String(255), nullable=False)
    detail_company = db.Column(db.Text, nullable=False)
    number = db.Column(db.String(25), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

    jobs = db.relationship('Job', backref='company', lazy=True)

class Jobseeker(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    name = db.Column(db.String(255), nullable=False)
    major = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(25), nullable=False)
    exprience = db.Column(db.Integer, nullable=True)
    name_company = db.Column(db.String(255), nullable=True)
    field_work = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

    timeline = db.relationship('Timeline', uselist=False, backref='jobseeker', lazy=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_company = db.Column(db.Integer, db.ForeignKey('company.id'))
    name_job = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    exprience = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(255), nullable=False, default='Unknown')
    date_posted = db.Column(db.Date, nullable=False)
    last_application = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

class Timeline(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_job = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    id_jobseeker = db.Column(db.Integer, db.ForeignKey('jobseeker.id'), nullable=False)
    apply_job = db.Column(Enum('pending', 'approved', 'rejected', name='apply_job_enum'), nullable=False, default='pending')
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

    job = db.relationship('Job', backref='timeline', lazy=True)
