import pandas as pd
import requests
import json

def token():
    """ 
    # Definicion de token
    TODO: add secrets library
    """
    
    tokenlist = ['2RG2NEF3IPXMIPX3', 'ZOW97SMSE5U3FPYU']
    return tokenlist[1]

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
    dataDF = pd.DataFrame.from_dict(data, orient='index')
    return dataDF

def leerExcel(nombreArchivo):
    data = pd.read_excel(nombreArchivo)
    data = data.sort_values('timestamp', ascending=True)
    data.set_index('timestamp', inplace=True)
    return data

def arreglarData(data):
    """Toma una matriz y la transforma para que la pueda usar mejor
    Orden:
    Open - High - Low - Close - Volume (MlnDollars)

    Args:
        data ([type]): [description]
    """
if __name__ == "__main__":
    print(get_daily('AAPL'))
    pass
