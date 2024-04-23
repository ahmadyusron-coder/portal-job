from flask import request, jsonify
from portal_job.models import *
from flask_login import login_required, current_user

@app.route('/company/', methods=['POST'])
@login_required
def create_company():
    if current_user.user_type == 'company':
        data = Company (
            id_user = request.form['id_user'],
            name = request.form['name'],
            detail_company = request.form['detail_company'],
            number = request.form['number'],
            country = request.form['country']
        )
        db.session.add(data)
        db.session.commit()
        return {'message': 'Successfully created company'}

@app.route('/company/', methods=['GET'])
@login_required
def get_company():
    if current_user.user_type == 'company':
        data = [
            {'id': data.id,
            'id_user': data.id_user,
            'name_company': data.name,
            'detail_company': data.detail_company,
            'number': data.number,
            'country': data.country,
            'created_at': data.created_at,
            'updated_at': data.updated_at
            } for data in Company.query.order_by(Company.id.desc()).all()
        ]
        return jsonify(data)

@app.route('/company/<id>', methods=['PUT'])
@login_required
def update_company(id):
    if current_user.user_type == 'company':
        data = Company.query.get(id)
        if data :
            data.name = request.form['name_company'],
            data.detail_company = request.form['detail_company'],
            data.number = request.form['number'],
            data.country = request.form['country']
            db.session.commit()
            return { '' : 'Update Success'}
    
@app.route('/company/<id>', methods=['DELETE'])
@login_required
def delete_company(id):
    if current_user.user_type == 'company':
        data = Company.query.get(id)
        if data :
            db.session.delete(data)
            db.session.commit()
            return {'': 'Delete Success'}
        else :
            return {'': 'Delete Not Success'}


@app.route('/jobseeker/', methods=['GET'])
@login_required
def get_jobseeker():
    if current_user.user_type == 'jobseeker':
        data = [
            {'id': data.id,
            'id_user': data.id_user,
            'name': data.name,
            'major': data.major,
            'age': data.age,
            'address': data.address,
            'number': data.number,
            'exprience': data.exprience,
            'name_company': data.name_company,
            'field_work': data.field_work,
            'created_at': data.created_at,
            'updated_at': data.updated_at
            } for data in Jobseeker.query.all()
        ]
        return jsonify(data)

@app.route('/jobseeker/', methods=['POST'])
@login_required
def create_jobseeker():
    if current_user.user_type == 'jobseeker':
        data = Jobseeker (
            id_user = request.form['id_user'],
            name = request.form['name'],
            major = request.form['major'],
            age = request.form['age'],
            address = request.form['address'],
            number = request.form['number'],
            exprience = 0 if request.form['exprience'] == '' else request.form['exprience'] ,
            name_company = request.form['name_company'],
            field_work = request.form['field_work']
        )
        db.session.add(data)
        db.session.commit()
        return {'message': 'Successfully Created Jobseeker'}

@app.route('/jobseeker/<id>', methods=['PUT'])
@login_required
def update_jobseeker(id):
    if current_user.user_type == 'jobseeker':
        data = Jobseeker.query.get(id)
        if data :
            data.name = request.form['name'],
            data.major = request.form['major'],
            data.age = request.form['age'],
            data.address = request.form['address'],
            data.number = request.form['number'],
            data.exprience = request.form['exprience'],
            data.name_company = request.form['name_company'],
            data.field_work = request.form['field_work']
            db.session.commit()
            return {'': 'Update Success'}

@app.route('/jobseeker/<id>', methods=['DELETE'])
@login_required
def delete_jobseeker(id):
    if current_user.user_type == 'jobseeker':
        data = Jobseeker.query.get(id)
        if data :
            db.session.delete(data)
            db.session.commit()
            return {'': 'Delete Success'}
        else :
            return {'': 'Delete Not Success'}


@app.route('/job/', methods=['POST'])
@login_required
def create_job():
    if current_user.user_type == 'company':
        data = Job (
            id_company = request.form['id_company'],
            name_job = request.form['name_job'],
            detail = request.form['detail'],
            exprience = request.form['exprience'],
            major = request.form['major'],
            date_posted = request.form['date_posted'],
            last_application = request.form['last_application']
        )
        db.session.add(data)
        db.session.commit()
        return {'message': 'Successfully Created Job'}

@app.route('/job/<id>/', methods=['GET'])
@login_required
def get_jobs(id):
    if current_user.user_type == 'company':
        job = Job.query.filter_by(id=id).first()
        if not job:
            return jsonify({'message': 'Job not found'}), 404
        company = Company.query.get(job.id_company)
        data = {
            'id': job.id,
            'id_company': job.id_company,
            'name_job': job.name_job,
            'detail': job.detail,
            'exprience': job.exprience,
            'major': job.major,
            'date_posted': job.date_posted.strftime('%d-%m-%Y'),
            'last_application': job.last_application.strftime('%d-%m-%Y') if job.last_application else None,
            'company': {
                'name': company.name,
                'details': company.detail_company,
                'number': company.number,
                'country': company.country
            },
            'created_at': job.created_at,
            'updated_at': job.updated_at
        } 
        return jsonify(data)
    else:
        return {'Message': "Access denied"}
    
@app.route('/job/', methods=['GET'])
@login_required
def get_job():
    if current_user.user_type == 'company':
        company = Company.query.filter_by(id_user=current_user.id).first()
        if company:
            jobs = Job.query.filter_by(id_company=company.id).all()
            data = [
                {
                    'id': job.id,
                    'id_company': job.id_company,
                    'name_job': job.name_job,
                    'detail': job.detail,
                    'exprience': job.exprience,
                    'major': job.major,
                    'date_posted': job.date_posted.strftime('%d-%m-%Y'),
                    'last_application': job.last_application.strftime('%d-%m-%Y') if job.last_application else None,
                    'created_at': job.created_at,
                    'updated_at': job.updated_at
                }
                for job in jobs
            ]
            return jsonify(data)
        else:
            return {'Message': "Access denied"}
    else:
        return {'Message': 'Anda Harus login sebagai Company'}

@app.route('/job/<id>', methods=['PUT'])
@login_required
def update_job(id):
    if current_user.user_type == 'company':
        data = Job.query.get(id)
        if data :
            data.name_job = request.form['name_job'],
            data.detail = request.form['detail'],
            data.exprience = request.form['exprience'],
            data.major = request.form['major'],
            data.date_posted = request.form['date_posted']
            data.date_last_application = request.form['last_application']
            db.session.commit()
            return {'' : 'Update Success'}

@app.route('/job/<id>', methods=['DELETE'])
@login_required
def delete_job(id):
    if current_user.user_type == 'company':
        data = Job.query.get(id)
        if data :
            db.session.delete(data)
            db.session.commit()
            return {'': 'Delete Success'}
        else : 
            return {'': 'Delete Not Succes'}


@app.route('/timeline/', methods=['GET'])
def get_timeline():
    data = [
        {
            'id': data.id,
            'id_job': data.id_job,
            'id_jobseeker' : data.id_jobseeker,
            'apply_job' : data.apply_job,
            'created_at' : data.created_at,
            'updated_at' : data.updated_at
        } for data in Timeline.query.all()
    ]
    return jsonify(data)