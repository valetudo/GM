
__author__ = 'Giuseppe'



import os
import pandas as pd
from pandas.io.data import get_data_yahoo
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import subplots
from matplotlib.finance import candlestick
from matplotlib.dates import date2num

currentDir = os.path.curdir

class Data(object):
    def __init__(self, ticker, startDate, endDate = datetime.datetime.now().strftime('%Y-%m-%d')):
        '''
        ex: obj = Data('SPY', '2013-2-2')
        '''
        self.ticker = ticker
        self.startDate = startDate
        self.endDate = endDate
        self.start = datetime.datetime.strptime(self.startDate, '%Y-%m-%d')
        self.end = datetime.datetime.strptime(self.endDate, '%Y-%m-%d')

    def __str__(self):
        '''
        ritorna una descrizione testuale dell'oggetto
        '''
        return 'ticker:\t\t{0}\nstart date:\t{1}\nend date:\t{2}'.format(self.ticker, self.startDate, self.endDate)


    def __len__(self):
        '''
        ritorna la durata in giorni del periodo considerato
        '''

        return (self.end-self.start).days


    def __mkdirs(self,name):
        '''
        crea le cartelle e ritorna il dataframe (cartella nascosta)
        '''
        self.name = name
        fileName = self.startDate+'.csv'
        dataPath = os.path.join(currentDir,'data', self.name)
        filePath = os.path.join(currentDir,'data', self.name, fileName)
        if not os.path.exists(dataPath):
            os.makedirs(dataPath)
        if not os.path.exists(filePath):
            webdata= get_data_yahoo(self.name,self.start, self.end)
            webdata.to_csv(filePath)
            df = webdata
        else:
            df = pd.read_csv(filePath, index_col=0, parse_dates=True)
        return df


    def getData(self, plot= False, *args):
        """
        ex: obj.getData()--> crea un dataframe OHLCV
            obj.getData(True,'DIA','XLI') --> crea un dataframe di tutti e lo plotta
        """
        self.plot = plot
        if len(args)>0:
            dfList = []
            df = self.__mkdirs(self.ticker)
            dfList.append(df['Close'])
            for newTicker in args:
                df2 = self.__mkdirs(newTicker)
                dfList.append(df2['Close'])
            df = pd.concat(dfList,keys= (self.ticker,)+args, axis=1)
        else:
            df = self.__mkdirs(self.ticker)
        if self.plot == True:
            df.pct_change().cumsum().plot()
            plt.show()
        return df


    def plotCandle(self,*args):

        df = self.getData()
        df['date'] = date2num(df.index)
        fig, ax = subplots()
        candlestick(ax, df[['date', 'Open', 'Close', 'High', 'Low']].values, width=.75, colorup='g',
                    colordown='r')
        ax.xaxis_date()
        plt.xlabel('Date')
        #plt.suptitle(ticker)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        for label in ax.xaxis.get_ticklabels():
            label.set_rotation(45)
        ax.grid(True)
        plt.show()





if __name__ ==  '__main__':
    obj = Data('SPY', '2000-2-2')
