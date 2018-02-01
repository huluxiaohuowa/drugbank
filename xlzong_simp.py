
# coding: utf-8

# In[36]:


import pandas as pd
import xlrd
import xlwt
import numpy as np
from datetime import date,datetime
import plotly.plotly as py
import plotly.graph_objs as go


# In[277]:


d = pd.read_table('/jhu/target.txt',low_memory = False, dtype=np.str)


# In[278]:


d


# In[4]:


workbook = xlrd.open_workbook('/jhu/target.xlsx')


# In[5]:


print(workbook.sheet_names())


# In[6]:


sheet1= workbook.sheet_by_index(0)


# In[7]:


sheet1.cell(32259,13).value


# In[8]:


sheet1.nrows


# In[9]:


targets={}


# In[10]:


for i in range(0,32259):
    for j in range(2,12):
        if sheet1.cell(i+1,j).value is not '':
            if sheet1.cell(i+1,j).value in targets.keys():
                for k in range(13,112):
                    if sheet1.cell(i+1,k).value is not '':
                        targets[sheet1.cell(i+1,j).value].append(sheet1.cell(i+1,k).value)
            else:
                targets[sheet1.cell(i+1,j).value]=[]
                for k in range(13,112):
                    if sheet1.cell(i+1,k).value is not '':
                        targets[sheet1.cell(i+1,j).value].append(sheet1.cell(i+1,k).value)


# In[12]:


len(targets)


# In[11]:


drugs = []
for i in targets.keys():
    for j in targets[i]:
        if j not in drugs:
            drugs.append(j)


# In[14]:


len(drugs)


# In[15]:


workbook = xlwt.Workbook()


# In[16]:


sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)


# In[17]:


sheet1.write(0,0,'sparse')


# In[18]:


output = '/jhu/xlzong.txt'
writer = open(output,'w')
writer.write('sparse\t')
for i in drugs:
    writer.write(i)
    writer.write('\t')
writer.write('\n')
for k,v in targets.items():
    writer.write(k)
    writer.write('\t')
    for i in range(364):
        if drugs[i] in v:
            writer.write('1')
        else:
            writer.write('0')
        writer.write('\t')
    writer.write('\n')
writer.close()


# In[19]:


prs = []


# In[20]:


for i in targets.keys():
    prs.append(i)


# In[22]:


prs[-1]


# In[12]:


ta = np.loadtxt('/jhu/target_array.txt')


# In[24]:


ta


# In[18]:


def presim(datas,row1,row2):
    sum = 0
    for i in datas[row1,]+datas[row2,]:
        if i!=0:
            sum += 1
    if sum != 0:
        return np.dot(np.transpose(datas[row1,]),datas[row2,])/sum
    else:
        return 0


# In[294]:


jhu


# In[13]:


ta.shape


# In[2]:


def penalty(dataset,row1,row2):
    icol = []
    for i in range(len(dataset[row1,])):
        if (dataset[row1,]+dataset[row2,])[i] > 1:
            icol.append(i)

    penalty_score = 0
    penalty_array=[]
    
    
    for irow in range(dataset.shape[0]):
        score = 0
        if irow != row1 and irow != row2:
            for item in icol:
                if dataset[irow,item] != 0:
                    score +=1
        if score != 0:
            penalty_array.append(np.abs(np.tanh(float(presim(dataset,irow,row1))-float(presim(dataset,irow,row2)))))

            
    for i in penalty_array:
        penalty_score += np.power(i,2)
    if len(penalty_array) != 0:
        penalty_score /= len(penalty_array)

    return np.sqrt(penalty_score)
            
            
            
        


# In[16]:


def simp(datass,row1,row2):
    simp_score=np.power(presim(datass,row1,row2),penalty(datass,row1,row2)+1)
    return simp_score


# In[19]:


simp(ta,1,4)


# In[235]:


ta.shape


# In[20]:


z=[]


# In[21]:


for i in range(179):
    z.append([])
    for j in range(179):
        if i == j:
            z[i].append(1)
        else:
            z[i].append(simp(ta,i,j))
        


# In[232]:



trace = go.Heatmap(z=z,x=prs,y=prs)
data=[trace]
py.iplot(data, filename='basic-heatmap')


# In[24]:


import plotly
plotly.tools.set_credentials_file(username='jecing', api_key='lginq9qzVp4LTDWTv6EV')


# In[231]:


output = '/jhu/simpscore.txt'
writer = open(output,'w')
writer.write('score\t')
for i in prs:
    writer.write(i)
    writer.write('\t')
writer.write('\n')
for i in range(179):
    writer.write(prs[i])
    writer.write('\t')
    for j in range(179):
        writer.write(str(z[i][j]))
        writer.write('\t')
    writer.write('\n')

writer.close()


# In[228]:


prs[1]


# In[25]:


wb = xlrd.open_workbook('/jhu/kinase.xlsx')
s1= wb.sheet_by_index(0)
kinase = {}
for i in range(1,65787):
    if s1.cell(i,22).value not in kinase.keys():
        kinase[s1.cell(i,22).value]=[]
    else:
        if s1.cell(i,15).value not in kinase[s1.cell(i,22).value]:
            kinase[s1.cell(i,22).value].append(s1.cell(i,15).value)


# In[27]:


kp = []
for i in kinase.keys():
    kp.append(i)
kd = []
for i in kinase.keys():
    for j in kinase[i]:
        if j not in kd:
             kd.append(j)


# In[268]:


output = '/jhu/jhu.txt'
writer = open(output,'w')
writer.write('sparse\t')
for i in kd:
    writer.write(str(int(i)))
    writer.write('\t')
writer.write('\n')
for k,v in kinase.items():
    writer.write(k)
    writer.write('\t')
    for i in range(41637):
        if kd[i] in v:
            writer.write('1')
        else:
            writer.write('0')
        writer.write('\t')
    writer.write('\n')
writer.close()


# In[28]:


jhu = np.loadtxt('/jhu/jhu_array.txt')


# In[307]:


presim(jhu,0,0)


# In[29]:


zz=[]
for i in range(211):
    zz.append([])
    for j in range(211):
        if i == j:
            zz[i].append(1)
        else:
            zz[i].append(presim(jhu,i,j))


# In[309]:


zz


# In[310]:


trace = go.Heatmap(z=zz,x=kp,y=kp)
data=[trace]
py.iplot(data, filename='kinase-heatmap')


# In[311]:


jhu


# In[40]:


zz005 = []
zz01 = []
zz02 = []
zz03 = []
for i in range(211):
    zz005.append([])
    zz01.append([])
    zz02.append([])
    zz03.append([])
    for j in range(211):
        if zz[i][j]>=0.05:
            zz005[i].append(1)
        else:
            zz005[i].append(0)
        if zz[i][j]>=0.1:
            zz01[i].append(1)
        else:
            zz01[i].append(0)
        if zz[i][j]>=0.2:
            zz02[i].append(1)
        else:
            zz02[i].append(0)
        if zz[i][j]>=0.3:
            zz03[i].append(1)
        else:
            zz03[i].append(0)


# In[37]:


trace = go.Heatmap(z=zz005,x=kp,y=kp)
data=[trace]
py.iplot(data, filename='kinase-heatmap-005')


# In[38]:


trace = go.Heatmap(z=zz01,x=kp,y=kp)
data=[trace]
py.iplot(data, filename='kinase-heatmap-01')


# In[41]:


trace = go.Heatmap(z=zz02,x=kp,y=kp)
data=[trace]
py.iplot(data, filename='kinase-heatmap-02')


# In[331]:




from matplotlib import pyplot as plt

from matplotlib import cm 

from matplotlib import axes
def draw_heatmap(data,xlabels,ylabels):

    cmap = cm.Blues    

    figure=plt.figure(facecolor='w')

    ax=figure.add_subplot(1,1,1,position=[0.1,0.15,0.8,0.8])

    ax.set_yticks(range(len(ylabels)))

    ax.set_yticklabels(ylabels)

    ax.set_xticks(range(len(xlabels)))

    ax.set_xticklabels(xlabels)

    vmax=data[0][0]

    vmin=data[0][0]

    for i in data:

        for j in i:

            if j>vmax:

                vmax=j

            if j<vmin:

                vmin=j

    map=ax.imshow(data,interpolation='nearest',cmap=cmap,aspect='auto',vmin=vmin,vmax=vmax)

    cb=plt.colorbar(mappable=map,cax=None,ax=None,shrink=0.5)

    plt.show()


# In[333]:


draw_heatmap(jhu,kd,kp)

