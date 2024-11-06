from models.models import db
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


ERROR_PARAMETER='Error, some of the parameters given are not right.'

def get_data_for_graphic(crypto, columna, rango='day', dates=[None, None]):
    """
        Parámetros:
            -crypto: Código de la crypto deseada
            -columna: Columna que se quiera representar
            -(Opcional)rango: Calcula el rango de tiempos según se seleccione 'hour', 'day', 'week', o 'month' donde el final del rango es ahora.
            -(Opcional)dates: Rango de fechas a calcular la grafica.
    """
    if crypto not in db:
        raise Exception(ERROR_PARAMETER)
    
    if columna not in ['v', 'q', 'V', 'Q']:
        raise Exception(ERROR_PARAMETER)
    
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
    res = db[crypto].find({
                    #'id': id
                    #'$and': [
                    #    #{f'{sensor}.time': {'$gte': dates[0], '$lte': dates[1]}}
                    #    {f'{sensor}.time': {'$gte': dates[1]}}
                    #]
                })
    res_list = list(res)
    processed_data = []
    for doc in res_list:
        #if '_id' in doc:
        #    del doc['_id']
        if columna in doc:
            processed_data.append({
                'value': doc[columna],
                'time': doc['time'].isoformat()
            })

    values = [entry['value'] for entry in processed_data]
    times = [datetime.fromisoformat(entry['time']) for entry in processed_data]

    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker='o', linestyle='-', color='b')

    plt.xlabel('Time')
    plt.ylabel(columna)
    plt.title(f'{columna} Data Over Time')
    plt.xticks(rotation=45)
    plt.grid(True)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return buf