from flask import request, jsonify
from portal_job.models import *

@app.route('/list-job/', methods=['GET'])
def get_list_job():
    jobs = Job.query.all()
    list_job = []
    for job in jobs:
        list_job.append({
            'id' : job.id,
            'id_company' : job.id_company,
            'name_job': job.name_job,
            'detail': job.detail,
            'exprience': job.exprience,
            'major' : job.major,
            'date_posted' : job.date_posted.strftime('%d-%m-%Y'),
            'last_application': job.last_application.strftime('%Y-%m-%d'),
            'company': {
                'name': job.company.name,
                'country': job.company.country
            },
            'created_at': job.created_at,
            'updated_at': job.updated_at
        })
    return {'job': list_job}
@app.route('/search-job/', methods=['GET'])
def get_search_job():
    major = request.args.get('major')
    exprience = request.args.get('exprience')

    query = Job.query
    if major:
        query = query.filter_by(major=major)
    if exprience:
        query = query.filter_by(exprience=exprience)

    jobs = query.all()
    search_results = []
    for job in jobs:
        list_job = {
            'id' : job.id,
            'id_company' : job.id_company,
            'name_job': job.name_job,
            'detail': job.detail,
            'exprience': job.exprience,
            'major' : job.major,
            'date_posted' : job.date_posted.strftime('%d-%m-%Y'),
            'last_application': job.last_application.strftime('%d-%m-%Y'),
            'company': {
                'name': job.company.name,
                'country': job.company.country,
            },
            'created_at': job.created_at,
            'updated_at': job.updated_at
        }
        search_results.append(list_job)
    return jsonify(search_results)

@app.route('/detail-job/<id>/', methods=['GET'])
def get_detail_job(id):
    job = Job.query.filter_by(id=id).first()
    if not job:
        return jsonify({'message': 'Job not found'}), 404
    
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
            'name': job.company.name,
            'details': job.company.detail_company,
            'number': job.company.number,
            'country': job.company.country
        },
        'created_at': job.created_at,
        'updated_at': job.updated_at
    } 
    return jsonify(data)

@app.route('/apply-job/', methods=['POST'])
def create_apply_job():
    data = request.json

    job = Jobseeker.query.filter_by (
        id= data['id']
        # id_user= job.id_user,
        # name = data.name,
        # major = data.major,
        # age = data.age,
        # address = data.address,
        # number = data.number,
        # exprience = data.exprience,
        # name_company = data.name_company,
        # field_work = data.field_work
        
    ).first()
    db.session.add(job)
    db.session.commit()
    for element in data ['timeline']:
        timelines = Timeline(
            id_jobseeker= job.id,
            id_job = element['id_job'],
            apply_job='pending'
        ) 
        db.session.add(timelines)
    db.session.commit()
    return {'message': 'Success'}