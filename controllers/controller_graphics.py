from utils.utils import get_data_for_graphic, checktoken
from flask import jsonify, send_file, request


def get_graphic():

    response = checktoken(request.headers.get('token'))

    if not response['valid']:
        return jsonify(response), 401

    try:
        buf = get_data_for_graphic(
            request.args.get('crypto'),
            request.args.get('column'),
            request.args.get('rango') if request.args.get('rango') is not None else 'day',
            [request.args.get('ini_time'), request.args.get('fin_time')]
        )

        return send_file(buf, mimetype='image/png', as_attachment=False, download_name='plot.png')
    
    except Exception as e:

        return jsonify({'valid': False, 'error': str(e)}), 400