from flask import request, jsonify
from models.models import users, tokens
import jwt
from datetime import timedelta, datetime


def login():

    data = request.get_json()
    user_email = data['user_email']
    user_password = data['user_password']
    doc = users.find_one({'user_email': user_email})
    
    if doc and doc['user_password'] == user_password:##MANAGE ENCRIPTED PASSWORD
    
        token = jwt.encode({'username': user_email}, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), algorithm='HS256')
        response = {'valid': True, 'user_given_name': doc['user_given_name'], 'token': token, 'user_email':user_email}
        entry = {
            "vallid": True,
            "token": token,
            "data": datetime.now().isoformat(),
            "user_email": user_email
        }
        res = tokens.insert_one(entry)
        return jsonify(response), 200
    
    else:

        response = {'valid': False, 'error': 'Email or password incorrect.'}
        return jsonify(response), 400



def register():

    data = request.get_json()
    user_email = data['user_email']
    doc = users.find_one({'user_email': user_email})

    if doc:
    
        return jsonify({'valid': False, 'error': f'email "{user_email}" already has an account'}), 400
    
    entry = {
        "user_surname": data['user_surname'],
        "user_given_name": data['user_given_name'],
        "user_email": user_email,
        "user_phone": data['user_phone'],
        "user_city": data['user_city'],
        "user_address": data['user_address'],
        "user_password": data['user_password'],##ENCRIPT PASSWORD
        "registration_time": datetime.now()
    }

    try:

        id = users.insert_one(entry).inserted_id
        return jsonify({'valid': True}), 200
    
    except Exception as description_error:
    
        return jsonify(response = {'valid': False, 'error': str(description_error)}), 400
