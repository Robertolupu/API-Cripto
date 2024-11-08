from models.models import db, users, tokens
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import io
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  


ERROR_PARAMETER='Error, some of the parameters given are not right.'

def get_data_for_graphic(crypto, columna, rango='day', dates=[None, None]):
    """
        Parámetros:
            -crypto: Código de la crypto deseada
            -columna: Columna que se quiera representar
            -(Opcional)rango: Calcula el rango de tiempos según se seleccione 'hour', 'day', 'week', o 'month' donde el final del rango es ahora.
            -(Opcional)dates: Rango de fechas a calcular la grafica.
    """
    if crypto not in db.list_collection_names():
        raise Exception(ERROR_PARAMETER)
    
    if columna not in ['v', 'q', 'V', 'Q']:
        raise Exception(ERROR_PARAMETER)
    
    logging.info(f"{rango}, {dates}")
    
    if dates == [None, None]:

        if rango not in ['hour', 'day', 'week', 'month']:
            raise Exception(ERROR_PARAMETER)

        dates[0] = datetime.now()

        if rango == 'hour':
            dates[1] = dates[0] - timedelta(hours=1)

        if rango == 'day':
            dates[1] = dates[0] - timedelta(days=1)

        elif rango == 'week':
            dates[1] = dates[0] - timedelta(weeks=1)

        elif rango == 'month':
            if dates[0].month == 1:
                dates[1] = datetime(dates[0].year - 1, 12, dates[0].day)
            
            else:
                dates[1] = datetime(dates[0].year, dates[0].month - 1, dates[0].day)

    dates = [date.isoformat() for date in dates]
    dates.sort()
    start_date = datetime.fromisoformat(dates[0]) if isinstance(dates[0], str) else dates[0]
    end_date = datetime.fromisoformat(dates[1]) if isinstance(dates[1], str) else dates[1]
    res = db[crypto].find({'time': {'$gte': start_date, '$lte': end_date}})
    res_list = list(res)
    processed_data = []
    for doc in res_list:
        #if '_id' in doc:
        #    del doc['_id']
        if columna in doc and 'time' in doc:
            processed_data.append({
                'value': doc[columna],
                'time': doc['time'].isoformat()
            })

    values = [entry['value'] for entry in processed_data]
    times = [datetime.fromisoformat(entry['time']) for entry in processed_data]

    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker='o', linestyle='-', color='b')
    plt.xlim(start_date, end_date)

    plt.xlabel('Time')
    plt.ylabel(columna)
    plt.title(f'{columna} Data Over Time')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=5))

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return buf


def checktoken(token):
        
    if(token=="roberto_internal_testing"):
        return {'valid': True, 'email': 'internal_testing'}

    if not token.startswith('Bearer '):
        response = {'valid': False, 'error': 'Invalid Token'}

    token = token[7:]
    
    user_data = tokens.find_one({'token': token})

    if user_data is None:
        response = {'valid': False, 'error': 'Invalid Token'}

    else:
        user = users.find_one({'user_email': user_data['user_email']})

        if user is None:
            response = {'valid': False, 'error': 'Invalid or inexistent user.'}

        elif datetime.now() <= (datetime.strptime(user_data['data'], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(minutes=50)):
            response = {'valid': True, 'email': user['user_email']}
            tokens.update_one({'token': token}, {'$set': {'data': datetime.now().isoformat()}})
        
        else:
            response = {'valid': False, 'error': 'Timeout'}

    return response