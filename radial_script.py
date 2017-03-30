import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt

data=pd.read_csv("C:\\Users\\shabieh2\\Desktop\\work_files\\flash proj\\1.csv")

plt.plot(data.x,data.y,'ro')

plt.show()

lm=LinearRegression(fit_intercept=True)

var=[]
rsq=[]
mean=[]
length=[]

sdata=list(set(data.sector))

for i in range(0,len(sdata)):
    
    sectori=data[data.sector==sdata[i]]
    
    var.append(np.var(sectori.x))
    mean.append(np.mean(sectori.x))
    lm.fit(sectori[['x']],sectori.y)
    
    if len(sectori)<2:
        rsq.append("inf")
    else:
        rsq.append(lm.score(sectori[['x']],sectori.y))
    
    length.append(len(sectori))
    

data=data.sort_values(by=['sector','Radius'])


vardf=pd.DataFrame(var)
meandf=pd.DataFrame(mean)
sectordf= pd.DataFrame(sdata)
lengthdf=pd.DataFrame(length)
rsqdf=pd.DataFrame(rsq)


result_joined=pd.concat([sectordf,lengthdf,vardf,meandf,rsqdf],axis=1)

result_joined.columns=['sector','sector_defects','x_var','x_mean','R-squared']

data=data.merge(result_joined,on='sector',how='left')

data = data.sort_values(by=['sector','Radius'])

data['radius-delta']= data['Radius']-data['Radius'].shift(-1)

data['radius-diff']= np.where(np.logical_and(data['radius-delta']< 5,data['radius-delta'] > -5),'Y','N')

data['continuity']=np.where(data['radius-diff']=="Y",1,0)

data['defect_length']=0

for i in range(1,len(data)):
    
    if data.loc[i,'continuity']==data.loc[i-1,'continuity'] \
    and data.loc[i,'sector']==data.loc[i-1,'sector'] \
    and data.loc[i,'continuity']==1:
        
            data.loc[i,'defect_length']=data.loc[i-1,'defect_length']+1
    



    







