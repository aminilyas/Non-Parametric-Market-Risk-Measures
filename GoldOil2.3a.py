# -*- coding: utf-8 -*-
"""

@author: Six
"""

#importing libraries 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

#importe file
data=pd.read_excel('GoldandOilData.xlsx',sheet_name='Price') #read the data into a panda DataFrame

#Compute L&P
data['L']=data['Gold'].diff(periods=-1)+10*data['Oil'].diff(periods=-1) #compute the L&P of gold
LP=data['L'].dropna() #supress the NaN of the L&P

LP=LP.tail(1500)

print(LP) #print the L&P on the screen to chek and compare with Excel

#Bootstrap
M = len(LP)


#Bootstrapping
N=10**3
sampleVec=np.random.choice(LP, size=(M,N),replace=True)

# #95%VaR of each sample
sampleVec = pd.DataFrame(sampleVec) #transforming the numpy sampleVec to a DataFrame sampleVec to use the quantile function
VaRDistr = sampleVec.quantile(q=0.95,axis=1)
# print('95%VaR of the',N,'samples :\n',VaRDistr)

#95%ES of each sample
N2=1000
step=(1-0.95)/N2
alpha=np.linspace(0.95+step, 1-step, N2-1)
ESVec=sampleVec.quantile(q=alpha,axis=1)
ESDistr=ESVec.mean()

#Computation of the 95%VaR as the median of 95%VaR distribution
VaR95=VaRDistr.quantile(0.5)
print('95% VaR (median of the 95%VaR distribution) =',VaR95)
#Computation of the lower bound of the 95% confidence interval
InfCIVaR=VaRDistr.quantile(.025)
#Computation of the higher bound of the 95% confidence interval
SupCIVaR=VaRDistr.quantile(.975)
print('Confidence Interval = ', InfCIVaR ,",", SupCIVaR)

#Computation of the 95%ES as the median of 95%ES distribution
ES95=ESDistr.quantile(0.5)
print('95%ES (median of the 95%ES distribution) =',ES95)
#Computation of the lower bound of the 95% confidence interval
InfCIES=ESDistr.quantile(.025)
#Computation of the higher bound of the 95% confidence interval
SupCIES=ESDistr.quantile(.975)
print('Confidence Interval = ', InfCIES ,",", SupCIES)

#Density estimation through gaussian kernel
kdeVaR=st.gaussian_kde(VaRDistr)
kdeES=st.gaussian_kde(ESDistr)

#Preparation of the plotting
VaRDistrMin=VaRDistr.min() #take the minimum of the distribution of the VaR 
VaRDistrMax=VaRDistr.max() #take maximum of the distribution of the VaR 
VaRrange = np.linspace(VaRDistrMin, VaRDistrMax, 10000) #create an array of 10000 VaR equally spaced between the minimum and the maximum of the VaR Distribution
VaRSmooth = kdeVaR(VaRrange) # create an array of densities which values correspond to those of the returns in rEquity

ESDistrMin=ESDistr.min() #take the minimum of the distribution of the ES 
ESDistrMax=ESDistr.max() #take maximum of the distribution of the ES 
ESrange = np.linspace(ESDistrMin, ESDistrMax, 10000) #create an array of 10000 ES equally spaced between the minimum and the maximum of the ES Distribution
ESSmooth = kdeES(ESrange) # create an array of densities which values correspond to those of the returns in rEquity

#Drawing of the distributions of VaR and ES
plt.figure(1) #creation of the object figure(1)
plt.plot(VaRrange,VaRSmooth,'-g') #plot the (kernel) density of VaR in green
plt.legend('VaR')
plt.title('Density of the VaR of the gold and oil portfolio') #give a title to figure(1)

plt.figure(2) #creation of the object figure(1)
plt.plot(ESrange,ESSmooth,'-b') #plot the (kernel) density of ES in blue
plt.legend('ES')
plt.title('Density of the ES of the gold and oil portfolio') #give a title to figure(1)
