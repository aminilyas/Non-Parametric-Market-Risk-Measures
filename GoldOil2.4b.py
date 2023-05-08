# -*- coding: utf-8 -*-
"""
%matplotlib
@author: Six
"""

#importing libraries 
import pandas as pd 
import numpy as np
import arch as ar
import matplotlib.pyplot as plt

#importe file
data=pd.read_excel('GoldandOilData.xlsx',sheet_name='Price') #read the data into a panda DataFrame
data['W']=data['Gold']+10*data['Oil']

#Compute the geometric returns
nSample=len(data['W'])
dataW1=data.W[1:nSample]
dataW1= dataW1.reset_index(drop=True)
dataW2=data.W[0:nSample-1]
dataW2= dataW2.reset_index(drop=True)
Ret=np.log(dataW1/dataW2)
Ret100=Ret*100

#GARCH(1,1) model
garch = ar.arch_model(Ret100) #create a garch(1,1) model
garch_fitted = garch.fit() #fit the garch(1,1) model to the data
print(garch_fitted.summary()) #print a summary of the fit
garch_fitted.plot() #plot the fitted volatility and the residuals

#Computation of the next variance / volatility
forecasts = garch_fitted.forecast(reindex = False)
forcastVol=forecasts.variance.iloc[0,0]**0.5/100*252**0.5 #Amin value is typically arround 15%, jere it is 12.934%

#Computation and plot of the fitted volatility
fittedVol=garch_fitted.conditional_volatility/100*252**0.5 #Amin for all the date
#Drawing of the distribution (density) of the SP500 returns
plt.figure(2) #creation of the object figure(1)
plt.plot(fittedVol,'-g') #plot the (kernel) density of VaR in green
plt.legend(['Fitted Volatility'])
plt.title('Fitted Volatility of the portfolio') #give a title to figure(2)

#Computation of the adjusted VaR and the non adjusted VaR (for volatility)
RetAdj=Ret*forcastVol/fittedVol
LossRelAdj=pd.DataFrame(data=-RetAdj)
LossRel=pd.DataFrame(data=-Ret)

RelAdjVar95=LossRelAdj.quantile(0.95) #Amin var at 95% at 1USD
RelVar95=LossRel.quantile(0.95)

Holding=data['W'].mean()
VaR95Adj=Holding*RelAdjVar95[0]
VaR95=Holding*RelVar95[0]

print('The Volatility-weighted 95% Value at Risk is', VaR95Adj)
print('The non Volatility-weighted 95% Value at Risk is', VaR95)