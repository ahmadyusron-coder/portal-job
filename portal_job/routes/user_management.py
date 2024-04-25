from flask import request, jsonify
from portal_job.models import *
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash



@app.route('/user/', methods=['POST'])
def create_user():
    data = User (
        username = request.form['username'],
        email = request.form['email'],
        password = generate_password_hash(request.form['password']),
        user_type = request.form['user_type']
    )
    db.session.add(data)
    db.session.commit()
    return {'message': 'User created successfully'}

@app.route('/user/', methods=['GET'])
def get_user():
    data = [
        {'id' : data.id,
        'username' : data.username,
        'email' : data.email,
        'password' : data.password,
        'user_type' : data.user_type,
        'created_at' : data.created_at,
        'updated_at' : data.updated_at
        } for data in User.query.order_by(User.id.desc()).all()
    ]
    return jsonify(data)

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    data = User.query.get(id)
    if data :
        data.username = request.form['username'],
        data.email = request.form['email'],
        data.password = generate_password_hash(request.form['password'])
        db.session.commit()
        return { '': 'Update Success' }
    
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    data = User.query.get(id)
    if data :
        db.session.delete(data)
        db.session.commit()
        return { '': 'Delete Success' }
    else :
        return { '': 'Delete Not Success' }

@app.route('/search/', methods=['GET'])
@login_required
def get_search():
    if current_user.user_type == 'company':
        major = request.args.get('major')
        exprience = request.args.get('exprience')
        # jobseekers = Jobseeker.query.filter_by(major=major, exprience=exprience).all()

        # Inisialisasi query tanpa filter
        query = Jobseeker.query
        
        # menambahkan filter 
        if major:
            query = query.filter_by(major=major)
        if exprience:
            query = query.filter_by(exprience=exprience)
        
        # mengambil hasilnya
        jobseekers = query.all()

        # hasil pencarian menjadi data yang dapat direturn dalam format JSON
        search_results = []
        for jobseeker in jobseekers:
            jobseeker_data = {
                'id': jobseeker.id,
                'name': jobseeker.name,
                'major': jobseeker.major,
                'age': jobseeker.age,
                'created_at': jobseeker.created_at,
                'updated_at': jobseeker.updated_at
                # 'address': jobseeker.address,
                # 'number': jobseeker.number,
                # 'exprience': jobseeker.exprience,
                # 'name_company': jobseeker.name_company,
                # 'field_work': jobseeker.field_work
            }
            search_results.append(jobseeker_data)
        return jsonify(search_results)
    else:
        return jsonify({'error': 'Unauthorized access'}), 403                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
        return {'message': 'Tidak bisa diakses'}