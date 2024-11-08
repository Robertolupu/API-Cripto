from flask import jsonify, request
from models.models import tokens
from utils.utils import checktoken

def check_token():

    response = checktoken(request.headers.get('token'))

    return jsonify(response), 200 if response['valid'] else 400


def logout():
    
    data = request.get_json()
    
    try:
        tokens.delete_one({'token': data['token']})

        response = {'valid': True}
    
    except Exception as description_error:

        response = {'valid': False, 'error': str(description_error)}
    
    return jsonify(response), 200 if response['valid'] else 400