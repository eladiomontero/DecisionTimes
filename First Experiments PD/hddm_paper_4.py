import pandas as pd
import matplotlib.pyplot as plt
import hddm
import csv
import numpy as np
from math import exp,log,sin,pi
from loadData import loadData
import json


""" --------------------------- """
""" 		PARAMETERS			"""
""" --------------------------- """

drN = 1 # binning network experiment
drW = 5 # binning pairwise experiment
N1 = 47
NC = 60
N2 = 58
NW = 100


""" --------------------------- """
""" 		CLASSES 			"""
""" --------------------------- """


class stats(object):
    def __init__(self,statPD):
    	self.a= statPD['mean']['a']
        self.v= statPD['mean']['v']
        self.t= statPD['mean']['t']
        self.z= statPD['mean']['z']
        self.ea= statPD['std']['a']
        self.ev= statPD['std']['v']
        self.et= statPD['std']['t']
        self.ez= statPD['std']['z']

    def fromStr(self,row):
    	self.a= row[0]
        self.v= row[1]
        self.t= row[2]
        self.z= row[3]
        self.ea= row[4]
        self.ev= row[5]
        self.et= row[6]
        self.ez= row[7]

    def toStr(self):
    	return '%8f,%8f,%8f,%8f,%8f,%8f,%8f,%8f\n'%(self.a,self.v,self.t,self.z,self.ea,self.ev,self.et,self.ez)

    def error95(self):
        self.ea2= 1.96*self.ea
        self.ev2= 1.96*self.ev
        self.et2= 1.96*self.et
        self.ez2= 1.96*self.ez

""" --------------------------- """
""" 		LOAD DATA			"""
""" --------------------------- """

(data1,dataC,data2,dataW) = loadData()


""" --------------------------- """
"""	    MESSING AROUND		"""
""" --------------------------- """

# Group vs Individual fit
data1_x = data1.copy()
data1_x['subj_idx'] = data1_x['userid']

#Exp1 group
mE1 = hddm.HDDM(data1, include='z')
mE1.sample(2000, burn=20)
statE1=mE1.gen_stats() 

#Exp1 individual
mE1x = hddm.HDDM(data1_x, include='z')
mE1x.sample(2000, burn=20)
statE1x=mE1x.gen_stats() 


a_vect = [statE1x.loc['a_subj.'+str(i)]['mean'] for i in range(1,170)]


""" --------------------------- """
"""	    FIRST 5					"""
""" --------------------------- """

data1_f5 = data1_x[data1_x['round'] <= 5]
mE1_f5 = hddm.HDDM(data1_f5, include='z')
mE1_f5.sample(2000, burn=20)
statE1_f5=mE1_f5.gen_stats() 

data1_f10 = data1_x[data1_x['round'] <= 10]
mE1_f10 = hddm.HDDM(data1_f10, include='z')
mE1_f10.sample(2000, burn=20)
statE1_f10=mE1_f10.gen_stats() 

""" --------------------------- """
"""	    FIVE BY FIVE  			"""
""" --------------------------- """

stats_fivebyfive = []

for i in range(10):
	data1_f5 = data1_x[(data1_x['round'] >= 5*i) & (data1_x['round'] <= 5*(i+1))]
	mE1_f5 = hddm.HDDM(data1_f5, include='z')
	mE1_f5.sample(1000, burn=20)
	statE1_f5=mE1_f5.gen_stats() 
	stats_fivebyfive.append(statE1_f5)

""" --------------------------- """
"""	    TEN BY TEN  			"""
""" --------------------------- """

stats_tenbyten= []

for i in range(5):
	data1_f10 = data1_x[(data1_x['round'] >= 10*i) & (data1_x['round'] <= 10*(i+1))]
	mE1_f10 = hddm.HDDM(data1_f10, include='z')
	mE1_f10.sample(1000, burn=20)
	statE1_f10=mE1_f10.gen_stats() 
	stats_tenbyten.append(statE1_f10)




""" --------------------------- """
"""	    EXPERIMENT ANALYSIS		"""
""" --------------------------- """
# A figure for each experiment on the quality of the fit

#Exp1
mE1 = hddm.HDDM(data1, include='z')
mE1.sample(2000, burn=20)
statE1=mE1.gen_stats() 

#ExpC
mEC = hddm.HDDM(dataC, include='z')
mEC.sample(2000, burn=20)
statEC=mEC.gen_stats() 

#Exp2
mE2 = hddm.HDDM(data2, include='z')
mE2.sample(2000, burn=20)
statE2=mE2.gen_stats() 

#DirRec
mEW = hddm.HDDM(dataW, include='z')
mEW.sample(2000, burn=20)
statEW=mEW.gen_stats() 

s1 = stats(statE1)
sC = stats(statEC)
s2 = stats(statE2)
sW = stats(statEW)

with open('fullExp.dat','w') as outFile:
	outFile.write(s1.toStr())
	outFile.write(sC.toStr())
	outFile.write(s2.toStr())
	outFile.write(sW.toStr())


""" --------------------------- """
"""		ROUNDS ANALYSIS			"""
""" --------------------------- """
cr = []
models = []

""" 1 - ALL SUBJECTS - NETWORK """
#Exp1
left = range(1,N1+1,drN)
right = range(1+drN,N1+2,drN)
center1 = [(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i])
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	models.append(model)
	cr.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))


#Control
left = range(1,NC+1,drN)
right = range(1+drN,NC+2,drN)
centerC = [N1+(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i])
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	models.append(model)
	cr.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))



#Exp 2
left = range(1,N2+1,drN)
right = range(1+drN,N2+2,drN)
center2 = [N1+NC+(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i])
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	models.append(model)
	cr.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))




"""SAVE"""
stats = [models[i].gen_stats() for i in range(len(models))]
d = {'a' : pd.Series([s['mean']['a'] for s in stats]),
	 'v' : pd.Series([s['mean']['v'] for s in stats]),
	 't' : pd.Series([s['mean']['t'] for s in stats]),
	 'z' : pd.Series([s['mean']['z'] for s in stats]),
	 'aE' : pd.Series([s['std']['a'] for s in stats]),
	 'vE' : pd.Series([s['std']['v'] for s in stats]),
	 'tE' : pd.Series([s['std']['t'] for s in stats]),
	 'zE' : pd.Series([s['std']['z'] for s in stats]),
	 'CR': cr}

df = pd.DataFrame(d)
df.to_csv('NW_rounds.csv')

""" 1 - ALL SUBJECTS - PAIRWISE """
#First round
drW = 5
left = range(1,NW+1,drW)
right = range(1+drW,NW+2,drW)
centerW = [(left[i]+right[i])*.5-.5 for i in range(len(left))]

crW = []
modelsW = []
for i in range(len(left)):
	print '\n',i+1
	mask = (dataW['round'] >= left[i]) & (dataW['round'] < right[i])
	dataBin = dataW.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsW.append(model)
	crW.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))


statsW = [modelsW[i].gen_stats() for i in range(len(modelsW))]

d = {'a' : pd.Series([s['mean']['a'] for s in statsW]),
	 'v' : pd.Series([s['mean']['v'] for s in statsW]),
	 't' : pd.Series([s['mean']['t'] for s in statsW]),
	 'z' : pd.Series([s['mean']['z'] for s in statsW]),
	 'aE' : pd.Series([s['std']['a'] for s in statsW]),
	 'vE' : pd.Series([s['std']['v'] for s in statsW]),
	 'tE' : pd.Series([s['std']['t'] for s in statsW]),
	 'zE' : pd.Series([s['std']['z'] for s in statsW]),
	 'CR': crW}

df = pd.DataFrame(d)
df.to_csv('PW_rounds.csv')


""" --------------------------- """
"""		STRATEGY ANALYSIS		"""
""" --------------------------- """


uMCC1 = set(data1['userid'].loc[data1['strategy']== 'MCC'])
uPD1 = set(data1['userid'].loc[data1['strategy']== 'PD'])
uPC1 = set(data1['userid'].loc[data1['strategy']== 'PC'])

uMCC2 = set(data2['userid'].loc[data2['strategy']== 'MCC'])
uPD2 = set(data2['userid'].loc[data2['strategy']== 'PD'])
uPC2 = set(data2['userid'].loc[data2['strategy']== 'PC'])

uMCC = uMCC1.intersection(uMCC2) #68 users
uPD = uPD1.intersection(uPD2)    #37 users
uMCC_PD= uMCC1.intersection(uPD2)    #32 users
uPD_MCC= uPD1.intersection(uMCC2)    #22 users
#last 10 users have been PC in at least one of the two experiments
#6 MCC-> PC
#1 PD -> PC
#2 PC -> PC
#1 PC -> MDD (150)
uPC = uPC1.union(uPC2)

""" I FOCUS ON THE 2 CONSISTENT GROUPS """

crMCC = []
crPD = []`

contextMCC = []
contextPD = []

modelsMCC = []
modelsPD = []

""" 2- STABLE STRATEGY - NETWORK """
#Exp1
left = range(1,N1+1,drN)
right = range(1+drN,N1+2,drN)
center1 = [(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i]) & (data1['userid'].isin(uMCC))
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsMCC.append(model)
	crMCC.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextMCC.append(np.mean(dataBin['context'])/8)

	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i]) & (data1['userid'].isin(uPD))
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsPD.append(model)
	crPD.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextPD.append(np.mean(dataBin['context'])/8)

#Control - I basically select user by exp1 and exp2 and track them here
# I also assume they experience the same mean field in CR and context
left = range(1,NC+1,drN)
right = range(1+drN,NC+2,drN)
centerC = [N1+(left[i]+right[i])*.5-.5 for i in range(len(left))]

lastCR =  float('nan')
for i in range(len(left)):
	print '\n',i+1
	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i]) & (dataC['userid'].isin(uMCC))
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsMCC.append(model)
	crMCC.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))

	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i]) & (dataC['userid'].isin(uPD))
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsPD.append(model)
	crPD.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))

	contextMCC.append(lastCR)
	contextPD.append(lastCR)

	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i])
	dataBin = dataC.loc[mask]
	lastCR = np.mean(dataBin['response'])

#Exp 2
left = range(1,N2+1,drN)
right = range(1+drN,N2+2,drN)
center2 = [N1+NC+(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i]) & (data2['userid'].isin(uMCC))
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsMCC.append(model)
	crMCC.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextMCC.append(np.mean(dataBin['context'])/8)

	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i]) & (data2['userid'].isin(uPD))
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsPD.append(model)
	crPD.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextPD.append(np.mean(dataBin['context'])/8)



"""SAVE"""

statsMCC = [modelsMCC[i].gen_stats() for i in range(len(modelsMCC))]
dMCC = {'a' : pd.Series([s['mean']['a'] for s in statsMCC]),
	 'v' : pd.Series([s['mean']['v'] for s in statsMCC]),
	 't' : pd.Series([s['mean']['t'] for s in statsMCC]),
	 'z' : pd.Series([s['mean']['z'] for s in statsMCC]),
	 'aE' : pd.Series([s['std']['a'] for s in statsMCC]),
	 'vE' : pd.Series([s['std']['v'] for s in statsMCC]),
	 'tE' : pd.Series([s['std']['t'] for s in statsMCC]),
	 'zE' : pd.Series([s['std']['z'] for s in statsMCC]),
	 'CR': crMCC,
	 'context':contextMCC}

dfMCC = pd.DataFrame(dMCC)
dfMCC.to_csv('NW_rounds_MCC.csv')

statsPD = [modelsPD[i].gen_stats() for i in range(len(modelsPD))]
dPD = {'a' : pd.Series([s['mean']['a'] for s in statsPD]),
	 'v' : pd.Series([s['mean']['v'] for s in statsPD]),
	 't' : pd.Series([s['mean']['t'] for s in statsPD]),
	 'z' : pd.Series([s['mean']['z'] for s in statsPD]),
	 'aE' : pd.Series([s['std']['a'] for s in statsPD]),
	 'vE' : pd.Series([s['std']['v'] for s in statsPD]),
	 'tE' : pd.Series([s['std']['t'] for s in statsPD]),
	 'zE' : pd.Series([s['std']['z'] for s in statsPD]),
	 'CR': crPD,
	 'context':contextPD}

dfPD = pd.DataFrame(dPD)
dfPD.to_csv('NW_rounds_PD.csv')




""" 2b- UNSTABLE STRATEGY - NETWORK """

crMCC_PD = []
crPD_MCC = []

contextMCC_PD = []
contextPD_MCC = []

modelsMCC_PD = []
modelsPD_MCC = []

#Exp1
left = range(1,N1+1,drN)
right = range(1+drN,N1+2,drN)
center1 = [(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i]) & (data1['userid'].isin(uMCC_PD))
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsMCC_PD.append(model)
	crMCC_PD.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextMCC_PD.append(np.mean(dataBin['context'])/8)

	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i]) & (data1['userid'].isin(uPD_MCC))
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsPD_MCC.append(model)
	crPD_MCC.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextPD_MCC.append(np.mean(dataBin['context'])/8)

#Control - I basically select user by exp1 and exp2 and track them here
# I also assume they experience the same mean field in CR and context
left = range(1,NC+1,drN)
right = range(1+drN,NC+2,drN)
centerC = [N1+(left[i]+right[i])*.5-.5 for i in range(len(left))]

lastCR =  float('nan')
for i in range(len(left)):
	print '\n',i+1
	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i]) & (dataC['userid'].isin(uMCC_PD))
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsMCC_PD.append(model)
	crMCC_PD.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))

	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i]) & (dataC['userid'].isin(uPD_MCC))
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsPD_MCC.append(model)
	crPD_MCC.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))

	contextMCC_PD.append(lastCR)
	contextPD_MCC.append(lastCR)

	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i])
	dataBin = dataC.loc[mask]
	lastCR = np.mean(dataBin['response'])

#Exp 2
left = range(1,N2+1,drN)
right = range(1+drN,N2+2,drN)
center2 = [N1+NC+(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i]) & (data2['userid'].isin(uMCC_PD))
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsMCC_PD.append(model)
	crMCC_PD.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextMCC_PD.append(np.mean(dataBin['context'])/8)

	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i]) & (data2['userid'].isin(uPD_MCC))
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsPD_MCC.append(model)
	crPD_MCC.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextPD_MCC.append(np.mean(dataBin['context'])/8)



"""SAVE"""

statsMCC_PD = [modelsMCC_PD[i].gen_stats() for i in range(len(modelsMCC_PD))]
dMCC_PD = {'a' : pd.Series([s['mean']['a'] for s in statsMCC_PD]),
	 'v' : pd.Series([s['mean']['v'] for s in statsMCC_PD]),
	 't' : pd.Series([s['mean']['t'] for s in statsMCC_PD]),
	 'z' : pd.Series([s['mean']['z'] for s in statsMCC_PD]),
	 'aE' : pd.Series([s['std']['a'] for s in statsMCC_PD]),
	 'vE' : pd.Series([s['std']['v'] for s in statsMCC_PD]),
	 'tE' : pd.Series([s['std']['t'] for s in statsMCC_PD]),
	 'zE' : pd.Series([s['std']['z'] for s in statsMCC_PD]),
	 'CR': crMCC_PD,
	 'context':contextMCC_PD}

dfMCC_PD = pd.DataFrame(dMCC_PD)
dfMCC_PD.to_csv('NW_rounds_MCC_PD.csv')

statsPD_MCC = [modelsPD_MCC[i].gen_stats() for i in range(len(modelsPD_MCC))]
dPD_MCC = {'a' : pd.Series([s['mean']['a'] for s in statsPD_MCC]),
	 'v' : pd.Series([s['mean']['v'] for s in statsPD_MCC]),
	 't' : pd.Series([s['mean']['t'] for s in statsPD_MCC]),
	 'z' : pd.Series([s['mean']['z'] for s in statsPD_MCC]),
	 'aE' : pd.Series([s['std']['a'] for s in statsPD_MCC]),
	 'vE' : pd.Series([s['std']['v'] for s in statsPD_MCC]),
	 'tE' : pd.Series([s['std']['t'] for s in statsPD_MCC]),
	 'zE' : pd.Series([s['std']['z'] for s in statsPD_MCC]),
	 'CR': crPD_MCC,
	 'context':contextPD_MCC}

dfPD_MCC = pd.DataFrame(dPD_MCC)
dfPD_MCC.to_csv('NW_rounds_PD_MCC.csv')






""" 2c - PC people"""

crPC = []

contextPC = []

modelsPC = []

#Exp1
left = range(1,N1+1,drN)
right = range(1+drN,N1+2,drN)
center1 = [(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i]) & (data1['userid'].isin(uPC))
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsPC.append(model)
	crPC.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextPC.append(np.mean(dataBin['context'])/8)


#Control - I basically select user by exp1 and exp2 and track them here
# I also assume they experience the same mean field in CR and context
left = range(1,NC+1,drN)
right = range(1+drN,NC+2,drN)
centerC = [N1+(left[i]+right[i])*.5-.5 for i in range(len(left))]

lastCR =  float('nan')
for i in range(len(left)):
	print '\n',i+1
	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i]) & (dataC['userid'].isin(uPC))
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsPC.append(model)
	crPC.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))

	contextPC.append(lastCR)

	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i])
	dataBin = dataC.loc[mask]
	lastCR = np.mean(dataBin['response'])

#Exp 2
left = range(1,N2+1,drN)
right = range(1+drN,N2+2,drN)
center2 = [N1+NC+(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i]) & (data2['userid'].isin(uPC))
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsPC.append(model)
	crPC.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextPC.append(np.mean(dataBin['context'])/8)



"""SAVE"""

statsPC = [modelsPC[i].gen_stats() for i in range(len(modelsPC))]
dPC = {'a' : pd.Series([s['mean']['a'] for s in statsPC]),
	 'v' : pd.Series([s['mean']['v'] for s in statsPC]),
	 't' : pd.Series([s['mean']['t'] for s in statsPC]),
	 'z' : pd.Series([s['mean']['z'] for s in statsPC]),
	 'aE' : pd.Series([s['std']['a'] for s in statsPC]),
	 'vE' : pd.Series([s['std']['v'] for s in statsPC]),
	 'tE' : pd.Series([s['std']['t'] for s in statsPC]),
	 'zE' : pd.Series([s['std']['z'] for s in statsPC]),
	 'CR': crPC,
	 'context':contextPC}

dfPC = pd.DataFrame(dPC)
dfPC.to_csv('NW_rounds_PC.csv')


""" --------------------------- """
"""	  AVERAGE CONTEXT ANALYSIS	"""
""" --------------------------- """

#What is the average context experienced by users

#a separate experiment 1-2

contU1 = [0]*169
contU2 = [0]*169

crMean1 = np.mean(data1['response'])
crMean2 = np.mean(data2['response'])
crMeanC = np.mean(dataC['response'])

for u  in range(1,170):
	contU1[u-1] = np.mean(data1['context'].loc[data1['userid'] == u])/8.
	contU2[u-1] = np.mean(data2['context'].loc[data2['userid'] == u])/8.



#b aggregate experiment

contU = [(c1*47+c2*58)/(47.+58) for c1,c2 in zip(contU1,contU2)]
crMean12 = (crMean1*47+crMean2*58)/(47.+58)
crMean1C2 = (crMean1*47+crMeanC*60+crMean2*58)/(165.)

y = [yy/169. for yy in range(1,170)]
plt.plot([0,0.51],[0.5,0.5],'--k')
plt.plot(sorted(contU1),y,'k.',[crMean1]*169,y,'k--')

plt.plot(sorted(contU2),y,'g.',[crMean2]*169,y,'g--')

plt.plot(sorted(contU),y,'b.',[crMean12]*169,y,'b--')
plt.plot([crMeanC]*169,y,'r--')
plt.plot([crMean1C2]*169,y,'k--')

plt.xlim(0,.51)
plt.show()

#ALL

usLow = [i for i in range(1,170) if contU[i-1] < 0.2215] #lower 30% 50 users, avg = 0.195 -> 1.56 neighbors
np.mean([contU[i-1] for i in usLow])
usHigh = [i for i in range(1,170) if contU[i-1] > 0.2843] #upper 30% 50 users, avg = 0.324 -> 2.59 neighbors
np.mean([contU[i-1] for i in usHigh])

#Exp1
usLow1 = [i for i in range(1,170) if contU1[i-1] < 0.246] #avg = 0.215 -> 1.72 neighbors
np.mean([contU1[i-1] for i in usLow1])
usHigh1 = [i for i in range(1,170) if contU1[i-1] > 0.316] # avg = 0.324 -> 2.94 neighbors
np.mean([contU1[i-1] for i in usHigh1])



""" 3- EXTREME CONTEXTS - NETWORK """

crLow = []
crHigh = []

contextLow = []
contextHigh = []

modelsLow = []
modelsHigh = []



#Exp1
left = range(1,N1+1,drN)
right = range(1+drN,N1+2,drN)
center1 = [(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i]) & (data1['userid'].isin(usLow))
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsLow.append(model)
	crLow.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextLow.append(np.mean(dataBin['context'])/8)

	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i]) & (data1['userid'].isin(usHigh))
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsHigh.append(model)
	crHigh.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextHigh.append(np.mean(dataBin['context'])/8)

#Control - I basically select user by exp1 and exp2 and track them here
# I also assume they experience the same mean field in CR and context
left = range(1,NC+1,drN)
right = range(1+drN,NC+2,drN)
centerC = [N1+(left[i]+right[i])*.5-.5 for i in range(len(left))]

lastCR =  float('nan')
for i in range(len(left)):
	print '\n',i+1
	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i]) & (dataC['userid'].isin(usLow))
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsLow.append(model)
	crLow.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))

	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i]) & (dataC['userid'].isin(usHigh))
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsHigh.append(model)
	crHigh.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))

	contextLow.append(lastCR)
	contextHigh.append(lastCR)

	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i])
	dataBin = dataC.loc[mask]
	lastCR = np.mean(dataBin['response'])

#Exp 2
left = range(1,N2+1,drN)
right = range(1+drN,N2+2,drN)
center2 = [N1+NC+(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i]) & (data2['userid'].isin(usLow))
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsLow.append(model)
	crLow.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextLow.append(np.mean(dataBin['context'])/8)

	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i]) & (data2['userid'].isin(usHigh))
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsHigh.append(model)
	crHigh.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextHigh.append(np.mean(dataBin['context'])/8)



"""SAVE"""

statsLow = [modelsLow[i].gen_stats() for i in range(len(modelsLow))]
dLow = {'a' : pd.Series([s['mean']['a'] for s in statsLow]),
	 'v' : pd.Series([s['mean']['v'] for s in statsLow]),
	 't' : pd.Series([s['mean']['t'] for s in statsLow]),
	 'z' : pd.Series([s['mean']['z'] for s in statsLow]),
	 'aE' : pd.Series([s['std']['a'] for s in statsLow]),
	 'vE' : pd.Series([s['std']['v'] for s in statsLow]),
	 'tE' : pd.Series([s['std']['t'] for s in statsLow]),
	 'zE' : pd.Series([s['std']['z'] for s in statsLow]),
	 'CR': crLow,
	 'context':contextLow}

dfLow = pd.DataFrame(dLow)
dfLow.to_csv('NW_rounds_Low.csv')

statsHigh = [modelsHigh[i].gen_stats() for i in range(len(modelsHigh))]
dHigh = {'a' : pd.Series([s['mean']['a'] for s in statsHigh]),
	 'v' : pd.Series([s['mean']['v'] for s in statsHigh]),
	 't' : pd.Series([s['mean']['t'] for s in statsHigh]),
	 'z' : pd.Series([s['mean']['z'] for s in statsHigh]),
	 'aE' : pd.Series([s['std']['a'] for s in statsHigh]),
	 'vE' : pd.Series([s['std']['v'] for s in statsHigh]),
	 'tE' : pd.Series([s['std']['t'] for s in statsHigh]),
	 'zE' : pd.Series([s['std']['z'] for s in statsHigh]),
	 'CR': crHigh,
	 'context':contextHigh}

dfHigh = pd.DataFrame(dHigh)
dfHigh.to_csv('NW_rounds_High.csv')






""" 3- EXTREME CONTEXTS (EXP1) - NETWORK """

crLow1 = []
crHigh1 = []

contextLow1 = []
contextHigh1 = []

modelsLow1 = []
modelsHigh1 = []



#Exp1
left = range(1,N1+1,drN)
right = range(1+drN,N1+2,drN)
center1 = [(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i]) & (data1['userid'].isin(usLow1))
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsLow1.append(model)
	crLow1.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextLow1.append(np.mean(dataBin['context'])/8)

	mask = (data1['round'] >= left[i]) & (data1['round'] < right[i]) & (data1['userid'].isin(usHigh1))
	dataBin = data1.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsHigh1.append(model)
	crHigh1.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextHigh1.append(np.mean(dataBin['context'])/8)

#Control - I basically select user by exp1 and exp2 and track them here
# I also assume they experience the same mean field in CR and context
left = range(1,NC+1,drN)
right = range(1+drN,NC+2,drN)
centerC = [N1+(left[i]+right[i])*.5-.5 for i in range(len(left))]

lastCR =  float('nan')
for i in range(len(left)):
	print '\n',i+1
	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i]) & (dataC['userid'].isin(usLow1))
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsLow1.append(model)
	crLow1.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))

	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i]) & (dataC['userid'].isin(usHigh1))
	dataBin = dataC.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsHigh1.append(model)
	crHigh1.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))

	contextLow1.append(lastCR)
	contextHigh1.append(lastCR)

	mask = (dataC['round'] >= left[i]) & (dataC['round'] < right[i])
	dataBin = dataC.loc[mask]
	lastCR = np.mean(dataBin['response'])

#Exp 2
left = range(1,N2+1,drN)
right = range(1+drN,N2+2,drN)
center2 = [N1+NC+(left[i]+right[i])*.5-.5 for i in range(len(left))]

for i in range(len(left)):
	print '\n',i+1
	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i]) & (data2['userid'].isin(usLow1))
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsLow1.append(model)
	crLow1.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextLow1.append(np.mean(dataBin['context'])/8)

	mask = (data2['round'] >= left[i]) & (data2['round'] < right[i]) & (data2['userid'].isin(usHigh1))
	dataBin = data2.loc[mask]
	model = hddm.HDDM(dataBin, include='z')
	model.sample(2000, burn=20)
	modelsHigh1.append(model)
	crHigh1.append(len(dataBin.loc[dataBin['response']==1])/float(len(dataBin)))
	contextHigh1.append(np.mean(dataBin['context'])/8)



"""SAVE"""

statsLow1 = [modelsLow1[i].gen_stats() for i in range(len(modelsLow1))]
dLow1 = {'a' : pd.Series([s['mean']['a'] for s in statsLow1]),
	 'v' : pd.Series([s['mean']['v'] for s in statsLow1]),
	 't' : pd.Series([s['mean']['t'] for s in statsLow1]),
	 'z' : pd.Series([s['mean']['z'] for s in statsLow1]),
	 'aE' : pd.Series([s['std']['a'] for s in statsLow1]),
	 'vE' : pd.Series([s['std']['v'] for s in statsLow1]),
	 'tE' : pd.Series([s['std']['t'] for s in statsLow1]),
	 'zE' : pd.Series([s['std']['z'] for s in statsLow1]),
	 'CR': crLow1,
	 'context':contextLow1}

dfLow1 = pd.DataFrame(dLow1)
dfLow1.to_csv('NW_rounds_Low1.csv')

statsHigh1 = [modelsHigh1[i].gen_stats() for i in range(len(modelsHigh1))]
dHigh1 = {'a' : pd.Series([s['mean']['a'] for s in statsHigh1]),
	 'v' : pd.Series([s['mean']['v'] for s in statsHigh1]),
	 't' : pd.Series([s['mean']['t'] for s in statsHigh1]),
	 'z' : pd.Series([s['mean']['z'] for s in statsHigh1]),
	 'aE' : pd.Series([s['std']['a'] for s in statsHigh1]),
	 'vE' : pd.Series([s['std']['v'] for s in statsHigh1]),
	 'tE' : pd.Series([s['std']['t'] for s in statsHigh1]),
	 'zE' : pd.Series([s['std']['z'] for s in statsHigh1]),
	 'CR': crHigh1,
	 'context':contextHigh1}

dfHigh1 = pd.DataFrame(dHigh1)
dfHigh1.to_csv('NW_rounds_High1.csv')
