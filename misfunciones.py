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

"""
# definición de variables
symbol = 'AAPL'
"""
# concatenar el link
def get_intraday(symbol, interval='15min'):
    """Get intraday values from Alphavantage

    Args:
        symbol ([type]): [description]
        interval (str, optional): [description]. Defaults to '15min'.
    """
    function = 'TIME_SERIES_INTRADAY' 

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
    # r = requests.get(url)
    print(r.json())

    data = r.json()['Time Series (15min)'] 

    dataDF = pd.DataFrame.from_dict(data, orient='index')
    dataDF

if __name__ == "__main__":
    get_intraday('AAPL')
