from flask import request, jsonify
from flask_login import login_required, current_user
from portal_job.models import *

@app.route('/apply-job/', methods=['GET'])
@login_required
def get_apply_job():
    if current_user.user_type == 'jobseeker':
        jobseeker = Jobseeker.query.filter_by(id_user=current_user.id).first()
        if not jobseeker:
            return jsonify({'message': 'Jobseeker data not found'}), 404
        data = Timeline.query.filter_by(id_jobseeker=jobseeker.id).order_by(Timeline.id.desc()).all()
        if not data:
            return jsonify({'message': 'Job applications not found'}), 404
        list_timeline = []
        for timeline in data:
            list_timeline.append({
                'id': timeline.id,
                'id_job': timeline.id_job,
                'id_jobseeker': timeline.id_jobseeker,
                'status': timeline.apply_job,
                'job': {
                    'name_job': timeline.job.name_job,
                    'detail' : timeline.job.detail,
                    'major' : timeline.job.major,

                    'company':{
                        'name': timeline.job.company.name,
                        'country' : timeline.job.company.country
                    }
                },
                'created_at': timeline.created_at,
                'updated_at': timeline.updated_at
            }) 
        return {'apply_job': list_timeline}
    

@app.route('/report-apply/<int:id>', methods=['PUT'])
@login_required
def update_report_apply(id):
    if current_user.user_type == 'company':
        data = request.json

        jobseeker = Jobseeker.query.get_or_404(id)


        for element in data.get('timeline', []):
            timeline = Timeline.query.filter_by(id_jobseeker=jobseeker.id, id_job=element['id_job']).first()

            timeline.apply_job = element['apply_job']
            db.session.add(timeline)
        db.session.commit()

        return {'message': 'Success'}

@app.route('/report/<int:id_jobseeker>', methods=['GET'])
def get_report_jobseeker(id_jobseeker):
    jobseekers = Jobseeker.query.filter_by(id=id_jobseeker).all()
    
    list_jobseeker = []
    for jobseeker in jobseekers:
        
        list_jobseeker.append({
            'name': jobseeker.name,
            'major': jobseeker.major,
            'age': jobseeker.age,
            'address': jobseeker.address,
            'number': jobseeker.number,
            'exprience': jobseeker.exprience,
            'name_company': jobseeker.name_company,
            'field_Work': jobseeker.field_work,
            'created_at': jobseeker.created_at,
            'updated_at': jobseeker.updated_at
        })

    return jsonify({'jobseeker': list_jobseeker})


@app.route('/report/<int:company_id>/job', methods=['GET'])

def company_jobs(company_id):
        # Ambil data pekerjaan yang dibuat oleh perusahaan dengan id tertentu
        company_job = Job.query.filter_by(id_company=company_id).all()


        jobs_data = []
        for job in company_job:
            # Hitung jumlah jobseeker yang melamar pada pekerjaan
            total_worker = Timeline.query.filter_by(id_job=job.id).count()
        
            jobseeker_data = []
            for timeline in job.timeline:
                # Siapkan data jobseeker untuk setiap timeline
                jobseeker_data.append({
                    'id': timeline.jobseeker.id,
                    'name': timeline.jobseeker.name,
                    'major': timeline.jobseeker.major,
                    'age': timeline.jobseeker.age,
                    'address': timeline.jobseeker.address,
                    'number': timeline.jobseeker.number,
                    'exprience': timeline.jobseeker.exprience,
                    'name_company': timeline.jobseeker.name_company,
                    'field_work': timeline.jobseeker.field_work,
                    'created_at': timeline.jobseeker.created_at,
                    'updated_at': timeline.jobseeker.updated_at
                })

            #data pekerjaan dan jumlah jobseeker yang melamar
            job_data = {
                'job_id': job.id,
                'name_job': job.name_job,
                'detail': job.detail,
                'exprience': job.exprience,
                'date_posted': job.date_posted.strftime('%d-%m-%Y'),
                'major': job.major,
                'total_worker': total_worker,
                'jobseekers': jobseeker_data,
                'created_at': job.created_at,
                'updated_at': job.updated_at
            }
            jobs_data.append(job_data)

        return jsonify(jobs_data)