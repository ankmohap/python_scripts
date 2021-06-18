import sys
import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import io
import requests
import datetime
from datetime import datetime

url = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
s = requests.get(url).content

df = pd.read_csv(io.StringIO(s.decode('utf-8')))

df.set_index("Country/Region",inplace = True)

print('Enter a country name')
country=input()

df1=df.loc[country][3:]

x=df.columns.to_numpy()[3:]
y=df1.to_numpy()
arr=[0]

for i in range(0,len(y)-1):
	arr.append(abs(y[i+1]- y[i]))

x_date=['21']
for i in range(0,len(x)-1):
        objDate = datetime.strptime(x[i], '%m/%d/%y')
        x_date.append(datetime.strftime(objDate,'%d%m'))
        
ax = plt.subplot2grid((2, 2), (0, 0))
ax.plot(x,y)
plt.title('Total number of cases')

ax1 = plt.subplot2grid((2, 2), (0, 1))
ax1.plot(x,arr)
plt.title('Number of new cases everyday')

ax2 = plt.subplot2grid((2, 2), (1, 0))
plt.yscale("log")
ax2.plot(x, y)
plt.title('Total cases on log scale')

f = [np.nan]
f.append(y[0])
alpha=0.3

for t in range(1,len(y)-1):
        f.append((1-alpha)*f[-1]+alpha*y[t])
        


ax3 = plt.subplot2grid((2,2), (1,1))
ax3.plot(x,f)
plt.title('Smoothened curve tot cases')

plt.show()

