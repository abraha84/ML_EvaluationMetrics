# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:18:10 2013

@author: abraha84
"""

from ROC import ROC
import random

TrueLabel=[]
PredictedLabel=[]

# open file to read
for i in range(0,100):
        TrueLabel.append(random.uniform(0,1))
        PredictedLabel.append(random.uniform(-0.2,1))
        
for i in range(0,100):
        TrueLabel.append(random.uniform(-1,0))
        PredictedLabel.append(random.uniform(-1,0.2))
ROC_Obj = ROC(TrueLabel, PredictedLabel,'Log1.csv')
print("ROC AUC: %s" % (str(ROC_Obj.auc()),)	)
ROC_Obj.plot(True, True,PlotFileName='Plots/ROCPlot.png')
