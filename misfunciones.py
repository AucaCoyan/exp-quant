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
    # ordeno segun la primera columna
    data = data.sort_values('timestamp')
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
    url += '&outputsize=compact'
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
    a = get_daily('GGAL')
    print(a)
    # print(calcDifVolumen(a))
