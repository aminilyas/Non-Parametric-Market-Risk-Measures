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

#Compute weights
size=len(LP)
lbd=0.94
pos = np.arange(1,size+1)
weight = lbd**(size-pos)*(1-lbd)/(1-lbd**size)

#Create a DataFrame made of the Loss LP and the weights
dataI = {'LP': LP,'Weight': weight}
dataO=pd.DataFrame(dataI)

#Sort dataO with the Loss in descending order
dataO=dataO.sort_values(by=['LP'], ascending=False)
dataO = dataO.reset_index(drop=True)

#Create a column of cumulative weight
dataO['CumWeight']=dataO['Weight'].cumsum()

#Compute the age weighted VaR
result_index = dataO['CumWeight'].sub(0.05).abs().idxmin() #find the index such that data in CumWeight are the closest to 0.05
VaR95=dataO['LP'][result_index] #compute the age weighted VaR that corresponds to the position result_index
print('The Age-weighted 95% Value at Risk is', VaR95)