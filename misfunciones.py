import pandas as pd
import requests
# import json

def token():
    """ 
    # Definicion de token
    TODO: add secrets library
    """
    tokenlist = ['2RG2NEF3IPXMIPX3', 'ZOW97SMSE5U3FPYU']
    return tokenlist[1]


def arreglarData(data):
    """Toma una matriz y la transforma para que la pueda usar mejor
    Orden:
    Open - High - Low - Close - Volume (MlnDollars)

    Args:
        data ([type]): [description]
    """


def get_intraday(symbol, interval='15min'):
    """Get intraday values from Alphavantage

    Args:
        symbol ([type]): [description]
        interval (str, optional): [description]. Defaults to '15min'.
    """
    function = 'TIME_SERIES_INTRADAY' 

    # concatenar el link
    urlBase = 'https://www.alphavantage.co/query'
    url = urlBase+ '?function=' + function
    url += '&symbol=' + str(symbol)
    url += '&interval=' + interval
    url += '&outputsize=compact'
    url += '&apikey=' + token()
    
    # print(url)
    # print('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo')
    # acá hago el llamado/request

    r = requests.get(url)

    data = r.json()['Time Series (15min)']
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    return dataDF


def get_daily(symbol, output='compact'):
    """Get daily values from Alphavantage

    Args:
        symbol ([type]): [description]
        output (compact or full, optional): [compact defaults into 100 values, full displays into 20+ years of historical data].
    """
    function = 'TIME_SERIES_DAILY' 
    urlBase = 'https://www.alphavantage.co/query' 
    url = urlBase+ '?function=' + function
    url += '&symbol=' + str(symbol)
    url += '&outputsize=compact'
    url += '&apikey=' + token()
    
    # print(url)
    # print('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo')
    # acá hago el llamado/request

    r = requests.get(url)

    data = r.json()['Time Series (Daily)']
    print(type(data))
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    dataDF['1. open'] =   dataDF['1. open'].astype(float)
    dataDF['2. high'] =   dataDF['2. high'].astype(float)
    dataDF['3. low'] =    dataDF['3. low'].astype(float)
    dataDF['4. close'] =  dataDF['4. close'].astype(float)
    dataDF['5. volume'] = dataDF['5. volume'].astype(int)
    # (['1. open', '2. high', '3. low', '4. close'], 1
    print(dataDF.dtypes)
    return dataDF


def AgregarMediaMovil(data, periodos):
    """Agrega una columna donde pone la media movil

    Args:
        data (df de pandas): [description]
        periodos (int): cantidad de periodos para calcular el MA
    """
    pass


def calcDifVolumen(data):
    """Agrega al df existente una columna más y mide la diferencia de volumen existente entre la rueda de hoy y la rueda de ayer

    Args:
        data ([df de pandas]): tabla de OHLCV
    """

    # Primer paso verificar si está la columna Diferencia de Volumen
    if '5. volume' not in data.columns:
        raise Exception("No se encontró la columna 'volume' ")
    else:
        # Luego agrego la columna con diferencia de volumen
        data['difVolumen'] = data['5. volume'].diff()
        return data

def leerExcel(nombreArchivo):
    data = pd.read_excel(nombreArchivo)
    data = data.sort_values('timestamp', ascending=True)
    data.set_index('timestamp', inplace=True)
    return data


if __name__ == "__main__":
    a = get_daily('AAPL')
    print(a)
    print(calcDifVolumen(a))
