from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy 
# from flask_migrate import Migrate
# from sqlalchemy import Enum
# from sqlalchemy import func
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from portal_job.models import *
from portal_job.routes.user_management import *
from portal_job.routes.job_management import *
from portal_job.routes.timeline import *
from portal_job.routes.reporting import *
# app = Flask(__name__)

# app.config['SECRET_KEY'] = 'secret'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/portal-job'
# db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

# migrate = Migrate(app, db)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(255), nullable=False, unique=True)
#     email = db.Column(db.String(255), nullable=False, unique=True)
#     password = db.Column(db.String(255), nullable=False)
#     user_type = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
#     updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())
    
#     def is_active(self):
#         return True
#     def get_id(self):
#         return self.id
#     def is_authenticated(self):
#         return True
    
# class Company(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id_user = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
#     name = db.Column(db.String(255), nullable=False)
#     detail_company = db.Column(db.Text, nullable=False)
#     number = db.Column(db.String(25), nullable=False)
#     country = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
#     updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

#     jobs = db.relationship('Job', backref='company', lazy=True)

# class Jobseeker(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id_user = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
#     name = db.Column(db.String(255), nullable=False)
#     major = db.Column(db.String(255), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     address = db.Column(db.String(255), nullable=False)
#     number = db.Column(db.String(25), nullable=False)
#     exprience = db.Column(db.Integer, nullable=True)
#     name_company = db.Column(db.String(255), nullable=True)
#     field_work = db.Column(db.String(255), nullable=True)
#     created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
#     updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

#     timeline = db.relationship('Timeline', uselist=False, backref='jobseeker', lazy=True)

# class Job(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id_company = db.Column(db.Integer, db.ForeignKey('company.id'))
#     name_job = db.Column(db.String(255), nullable=False)
#     detail = db.Column(db.Text, nullable=False)
#     exprience = db.Column(db.Integer, nullable=False)
#     major = db.Column(db.String(255), nullable=False, default='Unknown')
#     date_posted = db.Column(db.Date, nullable=False)
#     last_application = db.Column(db.Date, nullable=True)
#     created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
#     updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

# class Timeline(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     id_job = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
#     id_jobseeker = db.Column(db.Integer, db.ForeignKey('jobseeker.id'), nullable=False)
#     apply_job = db.Column(Enum('pending', 'approved', 'rejected', name='apply_job_enum'), nullable=False, default='pending')
#     created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp())
#     updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp())

#     job = db.relationship('Job', backref='timeline', lazy=True)


##################-Login Manager-----########################################

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

#login
@app.route('/login/', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return {'message': 'Anda Perlu Logout dahulu'}
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash (user.password, password):
        login_user(user)
        return jsonify({'message': 'login successful'}), 200
    else:
        return jsonify({'message': 'login failed'}), 400
    
#logout    
@app.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'logout successful'}),200


###################-Management User--#######################################

# @app.route('/user/', methods=['POST'])
# def create_user():
#     data = User (
#         username = request.form['username'],
#         email = request.form['email'],
#         password = generate_password_hash(request.form['password']),
#         user_type = request.form['user_type']
#     )
#     db.session.add(data)
#     db.session.commit()
#     return {'message': 'User created successfully'}

# @app.route('/user/', methods=['GET'])
# def get_user():
#     data = [
#         {'id' : data.id,
#         'username' : data.username,
#         'email' : data.email,
#         'password' : data.password,
#         'user_type' : data.user_type,
#         'created_at' : data.created_at,
#         'updated_at' : data.updated_at
#         } for data in User.query.all()
#     ]
#     return jsonify(data)

# @app.route('/user/<id>', methods=['PUT'])
# def update_user(id):
#     data = User.query.get(id)
#     if data :
#         data.username = request.form['username'],
#         data.email = request.form['email'],
#         data.password = generate_password_hash(request.form['password'])
#         db.session.commit()
#         return { '': 'Update Success' }
    
# @app.route('/user/<id>', methods=['DELETE'])
# def delete_user(id):
#     data = User.query.get(id)
#     if data :
#         db.session.delete(data)
#         db.session.commit()
#         return { '': 'Delete Success' }
#     else :
#         return { '': 'Delete Not Success' }

# @app.route('/search/', methods=['GET'])
# @login_required
# def get_search():
#     if current_user.user_type == 'company':
#         major = request.args.get('major')
#         exprience = request.args.get('exprience')
#         # jobseekers = Jobseeker.query.filter_by(major=major, exprience=exprience).all()

#         # Inisialisasi query tanpa filter
#         query = Jobseeker.query
        
#         # menambahkan filter 
#         if major:
#             query = query.filter_by(major=major)
#         if exprience:
#             query = query.filter_by(exprience=exprience)
        
#         # mengambil hasilnya
#         jobseekers = query.all()

#         # hasil pencarian menjadi data yang dapat direturn dalam format JSON
#         search_results = []
#         for jobseeker in jobseekers:
#             jobseeker_data = {
#                 'id': jobseeker.id,
#                 'name': jobseeker.name,
#                 'major': jobseeker.major,
#                 'age': jobseeker.age,
#                 'created_at': jobseeker.created_at,
#                 'updated_at': jobseeker.updated_at
#                 # 'address': jobseeker.address,
#                 # 'number': jobseeker.number,
#                 # 'exprience': jobseeker.exprience,
#                 # 'name_company': jobseeker.name_company,
#                 # 'field_work': jobseeker.field_work
#             }
#             search_results.append(jobseeker_data)
#         return jsonify(search_results)
#     else:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
#         return {'message': 'Tidak bisa diakses'}


########################----------------Job Management########################

# @app.route('/company/', methods=['POST'])
# @login_required
# def create_company():
#     if current_user.user_type == 'company':
#         data = Company (
#             id_user = request.form['id_user'],
#             name = request.form['name'],
#             detail_company = request.form['detail_company'],
#             number = request.form['number'],
#             country = request.form['country']
#         )
#         db.session.add(data)
#         db.session.commit()
#         return {'message': 'Successfully created company'}

# @app.route('/company/', methods=['GET'])
# @login_required
# def get_company():
#     if current_user.user_type == 'company':
#         data = [
#             {'id': data.id,
#             'id_user': data.id_user,
#             'name_company': data.name,
#             'detail_company': data.detail_company,
#             'number': data.number,
#             'country': data.country,
#             'created_at': data.created_at,
#             'updated_at': data.updated_at
#             } for data in Company.query.all()
#         ]
#         return jsonify(data)

# @app.route('/company/<id>', methods=['PUT'])
# @login_required
# def update_company(id):
#     if current_user.user_type == 'company':
#         data = Company.query.get(id)
#         if data :
#             data.name = request.form['name_company'],
#             data.detail_company = request.form['detail_company'],
#             data.number = request.form['number'],
#             data.country = request.form['country']
#             db.session.commit()
#             return { '' : 'Update Success'}
    
# @app.route('/company/<id>', methods=['DELETE'])
# @login_required
# def delete_company(id):
#     if current_user.user_type == 'company':
#         data = Company.query.get(id)
#         if data :
#             db.session.delete(data)
#             db.session.commit()
#             return {'': 'Delete Success'}
#         else :
#             return {'': 'Delete Not Success'}


# @app.route('/jobseeker/', methods=['GET'])
# @login_required
# def get_jobseeker():
#     if current_user.user_type == 'jobseeker':
#         data = [
#             {'id': data.id,
#             'id_user': data.id_user,
#             'name': data.name,
#             'major': data.major,
#             'age': data.age,
#             'address': data.address,
#             'number': data.number,
#             'exprience': data.exprience,
#             'name_company': data.name_company,
#             'field_work': data.field_work,
#             'created_at': data.created_at,
#             'updated_at': data.updated_at
#             } for data in Jobseeker.query.all()
#         ]
#         return jsonify(data)

# @app.route('/jobseeker/', methods=['POST'])
# @login_required
# def create_jobseeker():
#     if current_user.user_type == 'jobseeker':
#         data = Jobseeker (
#             id_user = request.form['id_user'],
#             name = request.form['name'],
#             major = request.form['major'],
#             age = request.form['age'],
#             address = request.form['address'],
#             number = request.form['number'],
#             exprience = 0 if request.form['exprience'] == '' else request.form['exprience'] ,
#             name_company = request.form['name_company'],
#             field_work = request.form['field_work']
#         )
#         db.session.add(data)
#         db.session.commit()
#         return {'message': 'Successfully Created Jobseeker'}

# @app.route('/jobseeker/<id>', methods=['PUT'])
# @login_required
# def update_jobseeker(id):
#     if current_user.user_type == 'jobseeker':
#         data = Jobseeker.query.get(id)
#         if data :
#             data.name = request.form['name'],
#             data.major = request.form['major'],
#             data.age = request.form['age'],
#             data.address = request.form['address'],
#             data.number = request.form['number'],
#             data.exprience = request.form['exprience'],
#             data.name_company = request.form['name_company'],
#             data.field_work = request.form['field_work']
#             db.session.commit()
#             return {'': 'Update Success'}

# @app.route('/jobseeker/<id>', methods=['DELETE'])
# @login_required
# def delete_jobseeker(id):
#     if current_user.user_type == 'jobseeker':
#         data = Jobseeker.query.get(id)
#         if data :
#             db.session.delete(data)
#             db.session.commit()
#             return {'': 'Delete Success'}
#         else :
#             return {'': 'Delete Not Success'}


# @app.route('/job/', methods=['POST'])
# @login_required
# def create_job():
#     if current_user.user_type == 'company':
#         data = Job (
#             id_company = request.form['id_company'],
#             name_job = request.form['name_job'],
#             detail = request.form['detail'],
#             exprience = request.form['exprience'],
#             major = request.form['major'],
#             date_posted = request.form['date_posted'],
#             last_application = request.form['last_application']
#         )
#         db.session.add(data)
#         db.session.commit()
#         return {'message': 'Successfully Created Job'}

# @app.route('/job/<id>/', methods=['GET'])
# @login_required
# def get_jobs(id):
#     if current_user.user_type == 'company':
#         job = Job.query.filter_by(id=id).first()
#         if not job:
#             return jsonify({'message': 'Job not found'}), 404
#         company = Company.query.get(job.id_company)
#         data = {
#             'id': job.id,
#             'id_company': job.id_company,
#             'name_job': job.name_job,
#             'detail': job.detail,
#             'exprience': job.exprience,
#             'major': job.major,
#             'date_posted': job.date_posted.strftime('%d-%m-%Y'),
#             'last_application': job.last_application.strftime('%d-%m-%Y') if job.last_application else None,
#             'company': {
#                 'name': company.name,
#                 'details': company.detail_company,
#                 'number': company.number,
#                 'country': company.country
#             },
#             'created_at': job.created_at,
#             'updated_at': job.updated_at
#         } 
#         return jsonify(data)
#     else:
#         return {'Message': "Access denied"}
    
# @app.route('/job/', methods=['GET'])
# @login_required
# def get_job():
#     if current_user.user_type == 'company':
#         company = Company.query.filter_by(id_user=current_user.id).first()
#         if company:
#             jobs = Job.query.filter_by(id_company=company.id).all()
#             data = [
#                 {
#                     'id': job.id,
#                     'id_company': job.id_company,
#                     'name_job': job.name_job,
#                     'detail': job.detail,
#                     'exprience': job.exprience,
#                     'major': job.major,
#                     'date_posted': job.date_posted.strftime('%d-%m-%Y'),
#                     'last_application': job.last_application.strftime('%d-%m-%Y') if job.last_application else None,
#                     'created_at': job.created_at,
#                     'updated_at': job.updated_at
#                 }
#                 for job in jobs
#             ]
#             return jsonify(data)
#         else:
#             return {'Message': "Access denied"}
#     else:
#         return {'Message': 'Anda Harus login sebagai Company'}

# @app.route('/job/<id>', methods=['PUT'])
# @login_required
# def update_job(id):
#     if current_user.user_type == 'company':
#         data = Job.query.get(id)
#         if data :
#             data.name_job = request.form['name_job'],
#             data.detail = request.form['detail'],
#             data.exprience = request.form['exprience'],
#             data.major = request.form['major'],
#             data.date_posted = request.form['date_posted']
#             data.date_last_application = request.form['last_application']
#             db.session.commit()
#             return {'' : 'Update Success'}

# @app.route('/job/<id>', methods=['DELETE'])
# @login_required
# def delete_job(id):
#     if current_user.user_type == 'company':
#         data = Job.query.get(id)
#         if data :
#             db.session.delete(data)
#             db.session.commit()
#             return {'': 'Delete Success'}
#         else : 
#             return {'': 'Delete Not Succes'}


# @app.route('/timeline/', methods=['GET'])
# def get_timeline():
#     data = [
#         {
#             'id': data.id,
#             'id_job': data.id_job,
#             'id_jobseeker' : data.id_jobseeker,
#             'apply_job' : data.apply_job,
#             'created_at' : data.created_at,
#             'updated_at' : data.updated_at
#         } for data in Timeline.query.all()
#     ]
#     return jsonify(data)

############################-----Timeline-----###################

# @app.route('/list-job/', methods=['GET'])
# def get_list_job():
#     jobs = Job.query.all()
#     list_job = []
#     for job in jobs:
#         list_job.append({
#             'id' : job.id,
#             'id_company' : job.id_company,
#             'name_job': job.name_job,
#             'detail': job.detail,
#             'exprience': job.exprience,
#             'major' : job.major,
#             'date_posted' : job.date_posted.strftime('%d-%m-%Y'),
#             'last_application': job.last_application.strftime('%Y-%m-%d'),
#             'company': {
#                 'name': job.company.name,
#                 'country': job.company.country
#             },
#             'created_at': job.created_at,
#             'updated_at': job.updated_at
#         })
#     return {'job': list_job}
# @app.route('/search-job/', methods=['GET'])
# def get_search_job():
#     major = request.args.get('major')
#     exprience = request.args.get('exprience')

#     query = Job.query
#     if major:
#         query = query.filter_by(major=major)
#     if exprience:
#         query = query.filter_by(exprience=exprience)

#     jobs = query.all()
#     search_results = []
#     for job in jobs:
#         list_job = {
#             'id' : job.id,
#             'id_company' : job.id_company,
#             'name_job': job.name_job,
#             'detail': job.detail,
#             'exprience': job.exprience,
#             'major' : job.major,
#             'date_posted' : job.date_posted.strftime('%d-%m-%Y'),
#             'last_application': job.last_application.strftime('%d-%m-%Y'),
#             'company': {
#                 'name': job.company.name,
#                 'country': job.company.country,
#             },
#             'created_at': job.created_at,
#             'updated_at': job.updated_at
#         }
#         search_results.append(list_job)
#     return jsonify(search_results)

# @app.route('/detail-job/<id>/', methods=['GET'])
# def get_detail_job(id):
#     job = Job.query.filter_by(id=id).first()
#     if not job:
#         return jsonify({'message': 'Job not found'}), 404
    
#     data = {
#         'id': job.id,
#         'id_company': job.id_company,
#         'name_job': job.name_job,
#         'detail': job.detail,
#         'exprience': job.exprience,
#         'major': job.major,
#         'date_posted': job.date_posted.strftime('%d-%m-%Y'),
#         'last_application': job.last_application.strftime('%d-%m-%Y') if job.last_application else None,
#         'company': {
#             'name': job.company.name,
#             'details': job.company.detail_company,
#             'number': job.company.number,
#             'country': job.company.country
#         },
#         'created_at': job.created_at,
#         'updated_at': job.updated_at
#     } 
#     return jsonify(data)

# @app.route('/apply-job/', methods=['POST'])
# def create_apply_job():
#     data = request.json

#     job = Jobseeker.query.filter_by (
#         id= data['id']
#         # id_user= job.id_user,
#         # name = data.name,
#         # major = data.major,
#         # age = data.age,
#         # address = data.address,
#         # number = data.number,
#         # exprience = data.exprience,
#         # name_company = data.name_company,
#         # field_work = data.field_work
        
#     ).first()
#     db.session.add(job)
#     db.session.commit()
#     for element in data ['timeline']:
#         timelines = Timeline(
#             id_jobseeker= job.id,
#             id_job = element['id_job'],
#             apply_job=element['apply_job']
#         ) 
#         db.session.add(timelines)
#     db.session.commit()
#     return {'message': 'Success'}





#################################------Reporting--------------####################

####mengecek status job yang sudah di lamar

# @app.route('/apply-job/', methods=['GET'])
# @login_required
# def get_apply_job():
#     if current_user.user_type == 'jobseeker':
#         jobseeker = Jobseeker.query.filter_by(id_user=current_user.id).first()
#         if not jobseeker:
#             return jsonify({'message': 'Jobseeker data not found'}), 404
#         data = Timeline.query.filter_by(id_jobseeker=jobseeker.id).all()
#         if not data:
#             return jsonify({'message': 'Job applications not found'}), 404
#         list_timeline = []
#         for timeline in data:
#             list_timeline.append({
#                 'id': timeline.id,
#                 'id_job': timeline.id_job,
#                 'id_jobseeker': timeline.id_jobseeker,
#                 'status': timeline.apply_job,
#                 'job': {
#                     'name_job': timeline.job.name_job,
#                     'detail' : timeline.job.detail,
#                     'major' : timeline.job.major,

#                     'company':{
#                         'name': timeline.job.company.name,
#                         'country' : timeline.job.company.country
#                     }
#                 },
#                 'created_at': timeline.created_at,
#                 'updated_at': timeline.updated_at
#             }) 
#         return {'apply_job': list_timeline}
    

# @app.route('/report-apply/<int:id>', methods=['PUT'])
# @login_required
# def update_report_apply(id):
#     if current_user.user_type == 'company':
#         data = request.json

#         jobseeker = Jobseeker.query.get_or_404(id)


#         for element in data.get('timeline', []):
#             timeline = Timeline.query.filter_by(id_jobseeker=jobseeker.id, id_job=element['id_job']).first()

#             timeline.apply_job = element['apply_job']
#             db.session.add(timeline)
#         db.session.commit()

#         return {'message': 'Success'}

# @app.route('/report/<int:id_jobseeker>', methods=['GET'])
# def get_report_jobseeker(id_jobseeker):
#     jobseekers = Jobseeker.query.filter_by(id=id_jobseeker).all()
    
#     list_jobseeker = []
#     for jobseeker in jobseekers:
        
#         list_jobseeker.append({
#             'name': jobseeker.name,
#             'major': jobseeker.major,
#             'age': jobseeker.age,
#             'address': jobseeker.address,
#             'number': jobseeker.number,
#             'exprience': jobseeker.exprience,
#             'name_company': jobseeker.name_company,
#             'field_Work': jobseeker.field_work,
#             'created_at': jobseeker.created_at,
#             'updated_at': jobseeker.updated_at
#         })

#     return jsonify({'jobseeker': list_jobseeker})


# @app.route('/report/<int:company_id>/job', methods=['GET'])

# def company_jobs(company_id):
#         # Ambil data pekerjaan yang dibuat oleh perusahaan dengan id tertentu
#         company_job = Job.query.filter_by(id_company=company_id).all()


#         jobs_data = []
#         for job in company_job:
#             # Hitung jumlah jobseeker yang melamar pada pekerjaan
#             total_worker = Timeline.query.filter_by(id_job=job.id).count()
        
#             jobseeker_data = []
#             for timeline in job.timeline:
#                 # Siapkan data jobseeker untuk setiap timeline
#                 jobseeker_data.append({
#                     'id': timeline.jobseeker.id,
#                     'name': timeline.jobseeker.name,
#                     'major': timeline.jobseeker.major,
#                     'age': timeline.jobseeker.age,
#                     'address': timeline.jobseeker.address,
#                     'number': timeline.jobseeker.number,
#                     'exprience': timeline.jobseeker.exprience,
#                     'name_company': timeline.jobseeker.name_company,
#                     'field_work': timeline.jobseeker.field_work,
#                     'created_at': timeline.jobseeker.created_at,
#                     'updated_at': timeline.jobseeker.updated_at
#                 })

#             #data pekerjaan dan jumlah jobseeker yang melamar
#             job_data = {
#                 'job_id': job.id,
#                 'name_job': job.name_job,
#                 'detail': job.detail,
#                 'exprience': job.exprience,
#                 'date_posted': job.date_posted.strftime('%d-%m-%Y'),
#                 'major': job.major,
#                 'total_worker': total_worker,
#                 'jobseekers': jobseeker_data,
#                 'created_at': job.created_at,
#                 'updated_at': job.updated_at
#             }
#             jobs_data.append(job_data)

#         return jsonify(jobs_data)


if __name__ == "__main__":
    app.run(debug=True)