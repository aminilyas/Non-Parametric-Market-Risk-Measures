# -*- coding: utf-8 -*-
"""

@author: Six
"""

#importing libraries
import numpy as np
import pandas as pd 
import scipy.stats as st
import scipy.interpolate as inter
import scipy.optimize as op

#Importe file
data=pd.read_excel('GoldandOilData.xlsx',sheet_name='Price') #read the data into a panda DataFrame
data['W']=data['Gold']+10*data['Oil']
LP= data['W'].diff(-1)
LP=LP.dropna()

LP=LP.tail(1500)

#Size of the sample
M=len(LP)

#Computation of rth order
alpha=0.95
r=alpha*M
r=int(r)

#Compute the empirical distribution of the Loss
p = np.linspace(0,1,M) #create a vector of quantiles, i.e. numbers belonging to (0,1), of size M, the lenght of the sample                  
LossSorted = sorted(LP) #sort the loss is ascending order
Cdf = inter.interp1d(LossSorted,p) #create the quantile function of the loss

#Compute the median and confidence intervals of the VaR
fMed = lambda x: 1- st.binom.cdf(r, M, Cdf(x))-0.5
VarMed=op.fsolve(fMed,30,xtol=0.01)
fCISup = lambda x: 1-st.binom.cdf(r, M, Cdf(x))-0.025
VaRCIInf=op.fsolve(fCISup,30,xtol=0.01)
fCIInf = lambda x: 1- st.binom.cdf(r, M, Cdf(x))-0.975
VaRCISup=op.fsolve(fCIInf,30,xtol=0.01)

print('95% VaR (median of the 95%VaR distribution) =',VarMed[0])
print('95% Confidence Interval = ', VaRCIInf[0] ,",", VaRCISup[0])
