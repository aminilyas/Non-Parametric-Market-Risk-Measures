# -*- coding: utf-8 -*-
"""
@author: Six
"""

#importing libraries 
import pandas as pd 
import numpy as np

#importe file
data=pd.read_excel('GoldandOilData.xlsx',sheet_name='Price') #read the data into a panda DataFrame

#Compute L&P
data['L']=data['Gold'].diff(periods=-1)+10*data['Oil'].diff(periods=-1) #compute the L&P of gold
LP=data['L'].dropna() #supress the NaN of the L&P
print(LP) #print the L&P on the screen to chek and compare with Excel

#Compute the Value at Risk for the 97% confidence level
historic_var97 = LP.quantile(.97)
print('The historical VaR of the gold and oil portfolio at 97% is:', historic_var97)

#Compute the Value at Risk for the 95% confidence level
historic_var95 = LP.quantile(.95)
print('The historical VaR of the gold and oil portfolio at 95% is:', historic_var95)

#Compute the Expected Shortfall for the 95% confidence level
N1=10**3
step=(1-0.95)/N1
alphaVec=np.linspace(0.95+step, 1-step, N1-1)
VaRVec=LP.quantile(alphaVec)
ES=VaRVec.mean()
print('The Expected Shortfall for a confidence level of 95% and for N =', N1,', is', ES)
