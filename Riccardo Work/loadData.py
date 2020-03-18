import pandas as pd
import hddm
import csv

reDict = {'D':0.,'C':1.}

def loadData():

	"""EXP1""" #with context
	#Load original file
	data = []
	with open('../times_exp1_rand.dat', 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			data.append((row[0],row[1],row[3],row[5],row[6].strip(),row[2]))
	#Create a file formatted for hddm
	with open('times_exp1_rand_hddm.csv', 'w') as outFile:
		outFile.write('userid,rt,response,round,context,strategy\n')
		for i in range(len(data)):
			d = data[i]
			action = reDict[d[1].strip()]
			roundN = int(d[2])
			if roundN > 1:
				context = contextNext #context is that of the previous round
			else:
				context = float('nan');
			contextNext = float(d[3])
			rt = float(d[0])/1000 #seconds
			if rt > 0 and rt< 30:
				outFile.write('%3d,%5.2f,%2.0f,%2d,%2.0f,%s\n'%(int(d[5]),rt,action,roundN,context,d[4]))
	#Load hddm format
	data1 = hddm.load_csv('times_exp1_rand_hddm.csv')
	data1 = hddm.utils.flip_errors(data1)

	"""CONTROL"""
	#Load original file
	data = []
	with open('../times_control_users.dat', 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			data.append((row[0],row[1],row[3],row[2]))
	#Create a file formatted for hddm
	with open('times_expC_rand_hddm.csv', 'w') as outFile:
		outFile.write('userid,rt,response,round\n')
		for d in data:
			rt = float(d[0])/1000; #seconds
			if rt > 0 and rt< 30:
				outFile.write('%3d,%8.6f,%5.3f,%2d\n'%(int(d[3]),rt,reDict[d[1].strip()],int(d[2])))
	#Load hddm format
	dataC = hddm.load_csv('times_expC_rand_hddm.csv')
	dataC = hddm.utils.flip_errors(dataC)

	"""EXP 2""" #with context
	#Load original file
	data = []
	with open('../times_exp2_rand.dat', 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			data.append((row[0],row[1],row[3],row[5],row[6].strip(),row[2]))
	#Create a file formatted for hddm
	with open('times_exp2_rand_hddm.csv', 'w') as outFile:
		outFile.write('userid,rt,response,round,context,strategy\n')
		for i in range(len(data)):
			d = data[i]
			action = reDict[d[1].strip()]
			roundN = int(d[2])
			if roundN > 1:
				context = contextNext #context is that of the previous round
			else:
				context = float('nan');
			contextNext = float(d[3])
			rt = float(d[0])/1000; #seconds
			if rt > 0 and rt< 30:
				outFile.write('%3d,%5.2f,%2.0f,%2d,%2.0f,%s\n'%(int(d[5]),rt,action,roundN,context,d[4]))
	#Load hddm format
	data2 = hddm.load_csv('times_exp2_rand_hddm.csv')
	data2 = hddm.utils.flip_errors(data2)

	"""PAIRWISE RECIPROCITY"""
	#Load original file
	data = []
	with open('../weakPD.dat', 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=' ')
		for row in csvreader:
			data.append((row[0],row[1],row[3],row[2]))
	#Create a file formatted for hddm
	with open('times_expW_rand_hddm.csv', 'w') as outFile:
		outFile.write('userid,rt,response,round\n')
		for d in data:
			rt = float(d[0])/1000; #seconds
			if rt > 0 and rt< 30:
				outFile.write('%2d,%8.6f,%5.3f,%2d\n'%(int(d[3]),rt,reDict[d[1].strip()],int(d[2])))
	#Load hddm format
	dataW = hddm.load_csv('times_expW_rand_hddm.csv')
	dataW = hddm.utils.flip_errors(dataW)

	return (data1,dataC,data2,dataW)
