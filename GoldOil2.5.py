# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 18:26:02 2022

@author: Six
"""

#importing libraries 
import pandas as pd 
import statsmodels.distributions.empirical_distribution as stECDF
import scipy.stats as st

#Importe file
data=pd.read_excel('GoldandOilData.xlsx',sheet_name='Price') #read the data into a panda DataFrame
data['W']=data['Gold']+10*data['Oil']
Loss= data['W'].diff(-1)
Loss=Loss.dropna()

Loss=Loss.tail(1500)

#Size of the sample
n=len(Loss)

#Computation of rth order
alpha=0.95
r=alpha*n
r=int(r) #Amin r is the smallest value of the loss sample

#Compute the empirical distribution of the Loss
ED=stECDF.ECDF(Loss)

#Compute the median and confidence intervals of the VaR
VaRMed=29.3
pMed = st.binom.cdf(r, n, ED(VaRMed))

VaRInf=33
pInf = st.binom.cdf(r, n, ED(VaRInf))

VaRSup=25
pSup = st.binom.cdf(r, n, ED(VaRSup))



# f = lambda x: st.binom.cdf(r, n, ED(x))-0.5

# u=op.fsolve(f,50,xtol=0.5)