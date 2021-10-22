import pandas as pd
import requests
# import json

def token():
    """ 
    # Definicion de token
    TODO: add secrets library
    """
    tokenlist = ['2RG2NEF3IPXMIPX3', 'ZOW97SMSE5U3FPYU']
    return tokenlist[0]


def checkRequest():
    # print(r.url)
    # print(r.status_code)
    pass

def arreglarData(data):
    """Toma una matriz y la transforma para que la pueda usar mejor
    Orden:
    Open - High - Low - Close - Volume (MlnDollars)

    Args:
        data ([type]): [description]
    """
    # ordeno segun la primera columna
    data.index.name = 'timestamp'
    data = data.sort_values('timestamp')
    data.index = pd.to_datetime(data.index)
    # TODO: tiene formato como datetime? sino agregarlo
    # le doy formato float a la tabla OHLCV
    data['1. open'] =   data['1. open'].astype(float)
    data['2. high'] =   data['2. high'].astype(float)
    data['3. low'] =    data['3. low'].astype(float)
    data['4. close'] =  data['4. close'].astype(float)
    data['5. volume'] = (data['5. volume'].astype(int)/1000000).round(2)
    # renombro las columnas a OHLCV
    data = data.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'}
        )
    return data


def get_intraday(symbol, interval='15min',  size='compact'):
    """Get intraday values from Alphavantage

    Args:
        symbol ([type]): [description]
        interval (str, optional): [description]. Defaults to '15min'.
    """
    function = 'TIME_SERIES_INTRADAY' 

    # acá hago el request
    url = 'http://www.alphavantage.co/query'
    parametros = {'function' : function,
                  'symbol' : symbol,
                  'interval' : interval,
                  'outputsize' : size,
                  'apikey' : token()
                }
    r = requests.get(url, params=parametros)
    print(r.url)

    # pido solamente los datos de precios
    # TODO: todavia tiene 15min de invervalo, hacer el ciclo para ponerlo como argumento de la funcion
    data = r.json()['Time Series (15min)']

    # lo convierto en un DF
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    dataDF = arreglarData(dataDF)
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
    url += '&outputsize=' + output
    url += '&apikey=' + token()
    
    r = requests.get(url)

    # pido solamente los datos de precios
    data = r.json()['Time Series (Daily)']
    # le doy formato en pandas a partir del JSON
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    
    # TODO: Necesito cambiar de nombre el index a 'timestamp'
    dataDF = pd.Index.rename('timestamp', inplace=True)
    
    # lo mando a arreglar data
    dataDF = arreglarData(dataDF)
    return dataDF


def getDailyAdj(symbol, size='compact'):
    """Get the daily values, and adjust them.

    Args:
        symbol (str): ticker to look for
        size (str): compact

    Returns:
        [type]: [description]
    """
    function='TIME_SERIES_DAILY_ADJUSTED'

    # acá hago el request
    url = 'http://www.alphavantage.co/query'
    parametros = {'function' : function,
                  'symbol' : symbol,
                  'outputsize' : size,
                  'apikey' : token()
                }
    r = requests.get(url, params=parametros)

    # pido solamente los datos de precios
    data = r.json()['Time Series (Daily)']

    # lo convierto en un DF
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    
    # FIXME tiene 8 columnas: OHLC + ajusted close + voluen (fuera de lugar) + dividend amount + split coeficient
    # dataDF = arreglarData(dataDF)
    
    # data.columns = []
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

    # primero fijarse si la columna 'volume' existe
    # luego paso verificar si está la columna Diferencia de Volumen
    if 'volume' not in data.columns:
        raise Exception("No se encontró la columna 'volume' ")
    else:
        # Luego agrego la columna con diferencia de volumen
        data['difVolumen'] = data['volume'].diff()
        return data

def leerExcel(nombreArchivo):
    data = pd.read_excel(nombreArchivo)
    data = data.sort_values('timestamp', ascending=True)
    data.set_index('timestamp', inplace=True)
    return data


def get_Alphavantage(symbol):
    """Get JSON dict from Alphavantage

    Args:
        symbol ([type]): [description]
    """
    function = 'GLOBAL_QUOTE' 
    urlBase = 'https://www.alphavantage.co/query' 
    url = urlBase+ '?function=' + function
    url += '&symbol=' + str(symbol)
    url += '&apikey=' + token()
    
    r = requests.get(url)

    # pido solamente los datos de precios
    data = r.json()
    return data


def search_Alphavantage(keyword):
    """Search from Alphavantage

    Args:
        symbol ([type]): [description]
    """
    function = 'SYMBOL_SEARCH' 
    urlBase = 'https://www.alphavantage.co/query' 
    url = urlBase+ '?function=' + function
    url += '&keywords=' + str(keyword)
    url += '&apikey=' + token()
    
    r = requests.get(url)

    # pido solamente los datos de precios
    data = r.json()
    return data


if __name__ == "__main__":

    a = search_Alphavantage('galicia')
    #a = getDailyAdj('IBM', 'compact')
    print(a)
    # print(calcDifVolumen(a))
