from utils.utils import get_data_for_graphic
from flask import jsonify, send_file, request


def get_graphic():

    buf = get_data_for_graphic(
        request.args.get('crypto'),
        request.args.get('column'),
        request.args.get('rango') if request.args.get('rango') is not None else 'day',
        [request.args.get('ini_time'), request.args.get('fin_time')]
    )

    return send_file(buf, mimetype='image/png', as_attachment=False, download_name='plot.png')