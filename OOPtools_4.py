from GM import Data
import pandas as pd
from pandas.tseries.offsets import BDay
import numpy as np
import datetime
import matplotlib.pyplot as plt
import time




class PatternRec:
    def __init__(self, tickerSymbol, patternLength= 60, outcomeLength= 20, startDate= '2005-2-2',correlation =.8):
        self.ticker = tickerSymbol
        self.pL = patternLength
        self.oL = outcomeLength
        self.startDate = startDate
        self.corr = correlation
        self.obj = Data(self.ticker,self.startDate)
        self.s = self.obj.getData()['Close'].pct_change().cumsum().dropna()*100
        self.s.name = 'percentCum'


    def pRec(self):
        i= len(self.s)
        self.valoreAtteso= np.nan
        self.dfPast = pd.DataFrame(self.s[i-self.pL:i])
        firstdayFut = self.dfPast.index[-1]+BDay(1)
        self.dfFut = pd.DataFrame(index=pd.date_range(firstdayFut, periods=self.oL, freq='B'), columns=['out'])
        j = i -self.pL
        while j > self.pL:
            st = self.s.index[j].strftime('%y-%m-%d')
            pat = self.s[j-self.pL:j]
            self.dfPast[st] = pat.values
            c = self.dfPast['percentCum'].corr(self.dfPast[st])
            if c < self.corr:
                self.dfPast = self.dfPast.drop(st, axis= 1)
                j-=1
            else:
                self.dfFut[st]= self.s[j:j+self.oL].values
                j-=self.pL
        self.dfFut = self.dfFut.drop('out',1)
        if self.dfFut.shape[1] >=5:

            self.rets = self.dfFut.apply(lambda x: x[-1]- x[0])
            positiveOut = [i  for i in self.rets if i > 0]
            negativeOut = [i  for i in self.rets if i < 0]
            positivePercent = (len(positiveOut)*100.)/len(self.rets)
            if  positivePercent > 65:
                self.valoreAtteso =np.mean(positiveOut)
            elif positivePercent < 35:
                self.valoreAtteso = np.mean(negativeOut)
            else:
                self.valoreAtteso = np.nan
                self.maxVal = np.max(positiveOut)
                self.minVal = np.min(negativeOut)

            print 'pattern simili:\t\t{0}\nritorni positivi:\t{1} %\nmedia outcome:\t\t{2}'.format(len(self.rets),positivePercent,self.valoreAtteso)
        return self.valoreAtteso

    def plotPatterns(self):
        dfTot = pd.concat([self.dfPast, self.dfFut])
        dfPlot = pd.DataFrame(index = dfTot.index, columns=['plot'])
        for serie in  dfTot.iteritems():
            plotSeries = serie[1].apply(lambda x: x -(serie[1][len(self.dfPast)-1]-self.dfPast['percentCum'][-1]))
            dfPlot[serie[0]]= plotSeries
        dfPlot = dfPlot.drop('plot', 1)
        dfPlot.plot(colormap='jet')
        plt.axvline(x= self.dfPast.index[-1],color='grey')
        plt.show()

    def scan(self):
        columns = np.arange(30, 90, 10)
        outcomeIndex = np.arange(7, 21, 2)
        resoultFrame = pd.DataFrame(index = outcomeIndex, columns= columns)
        for eachOl in outcomeIndex:
            for eachPl in columns:
                o = PatternRec(self.ticker, eachPl,eachOl,self.startDate)
                outcome = o.pRec()
                resoultFrame[eachPl][eachOl]= outcome
                print 'calcolo\t{0}\t{1}\t{2}'.format(eachOl, eachPl,outcome)
        print resoultFrame
        title = '{0} dal {1}'.format(self.ticker, self.startDate)
        resoultFrame.plot(kind='bar')
        plt.legend(shadow=True)
        plt.xlabel('Numero giorni previsione')
        plt.ylabel('Rendimento percentuale previsto')
        plt.title(title)
        plt.show()


if __name__ == '__main__':
    o = PatternRec(tickerSymbol='SPY')
