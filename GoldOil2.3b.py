# -*- coding: utf-8 -*-
"""
@author: Six

"""

#importing libraries 
import pandas as pd 
import numpy as np
import scipy.interpolate as inter

#importe file
data=pd.read_excel('GoldandOilData.xlsx',sheet_name='Price') #read the data into a panda DataFrame

#Compute L&P
data['L']=data['Gold'].diff(periods=-1)+10*data['Oil'].diff(periods=-1) #compute the L&P of gold
LP=data['L'].dropna() #supress the NaN of the L&P
print(LP) #print the L&P on the screen to chek and compare with Excel

LP=LP.tail(1500)

#Compute the inverse of the empirical CDF, i.e. the quantile function
p = np.linspace(0,1,len(LP))                  
LossSorted = sorted(LP)
ppF = inter.interp1d(p,LossSorted)

#Compute the samples
M=len(LP) #size of the samples
N=10**5 #number of samples generated
SampleU=np.random.uniform(0,1,size=(M,N))

#Compute the distribution of the VaR
SampleLoss=ppF(SampleU)

#95%VaR of each sample
SampleLoss=pd.DataFrame(SampleLoss)
VaRDistr = SampleLoss.quantile(q=.95,axis=1)

#95%ES of each sample
N2=1000
step=(1-0.95)/N2
alpha=np.linspace(0.95+step, 1-step, N2-1)
ESVec=SampleLoss.quantile(q=alpha,axis=1)
ESDistr=ESVec.mean()

#Computation of the 95%VaR as the median of 95%VaR distribution
VaR95=VaRDistr.quantile(0.5)
print('95% VaR (median of the 95%VaR distribution) =',VaR95)
#Computation of the lower bound of the confidence interval
InfCIVaR=VaRDistr.quantile(.025)
#Computation of the higher bound of the confidence interval
SupCIVaR=VaRDistr.quantile(.975)
print('Confidence Interval = ', InfCIVaR ,",", SupCIVaR)


#Computation of the 95%ES as the median of 95%ES distribution
ES95=ESDistr.quantile(0.5)
print('95%ES (median of the 95%ES distribution) =',ES95)
#Computation of the lower bound of the confidence interval
InfCIES=ESDistr.quantile(.025)
#Computation of the higher bound of the confidence interval
SupCIES=ESDistr.quantile(.975)
print('Confidence Interval = ', InfCIES ,",", SupCIES)