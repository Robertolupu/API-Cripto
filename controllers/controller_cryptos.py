from utils.utils import get_data_for_graphic, checktoken
from flask import jsonify, send_file, request
from models.models import db, ERROR_PARAMETER
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') 


def get_graphic():

    response = checktoken(request.headers.get('token'))

    if not response['valid']:
        return jsonify(response), 401

    try:
        dates = [datetime.fromisoformat(request.args.get('ini_time')), datetime.fromisoformat(request.args.get('fin_time'))]

    except:
        dates = [None, None]

    try:
        buf = get_data_for_graphic(
            request.args.get('crypto'),
            request.args.get('column'),
            request.args.get('rango') if request.args.get('rango') is not None else 'day',
            dates
        )

        return send_file(buf, mimetype='image/png', as_attachment=False, download_name='plot.png')
    
    except Exception as e:

        return jsonify({'valid': False, 'error': str(e)}), 400
    
def get_value():
    """
        Devuelve valor actual de esa crypto:
        Params:
            crypto: Nombre de la crypto
            (opcional)date: Fecha específica del dato en formato iso. Se devuelve el dato immediatamente anterior a la fecha en caso de no haber coincidencias. 
    """

    response = checktoken(request.headers.get('token'))

    if not response['valid']:
        return jsonify(response), 401

    try:
        crypto = request.args.get('crypto')

        if crypto not in db.list_collection_names():
            raise Exception(ERROR_PARAMETER)
        
        try:
            value_date = datetime.fromisoformat(request.args.get('date'))

        except Exception as e:
            logging.info(str(e))
            value_date = datetime.now()
        

        result = db[crypto].find({'time': {'$lte': value_date}}).sort('time', -1).limit(1)
        
        value = next(result, None)
        if value is not None:
            return jsonify({'valid': True, 'value': value['v']}), 200
        
        else: 
            return jsonify({'valid': False, 'error': 'No value forund for indicated parameters.'}), 400

    
    except Exception as e:

        return jsonify({'valid': False, 'error': str(e)}), 400