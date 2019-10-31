# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 14:54:33 2013

@author: abraha84
"""

from __future__ import division
try:    
    import pylab as pl
    import argparse
    from decimal import Decimal
except:
    print("Error:\tUnable to import one or more module.")

#Need to update the plot method to be scalable run fast with large data
#-An possible solution is to use only Equidistant sample values for the true and false positive lists
#Need to add fn to check whether the size of the input lists match and class labels are valid
#Need to incorparate trapezoidal area estimatation for more accurate AUC.
#Need to add more options to customize the plot properties
#Need to add option to plot multiple ROC curves on the same plot.
#-t 'TrueLabel.csv' -p 'PredictedValue.csv' -o 'True'
    
class ROC(object):
    """ A class that plots an ROC Curve and returns AUC.
        Input data is two list TrueClass and PredictedValue
        where:
            TrueClass = 1 for positive class and TrueClass = -1 for negative class
            PredictedValue is the real valued-list of size equal to TrueClass
            AUC= Area under the curve;
                AUC was computed by using TotalArea=PositiveClassSize*NegativeClassSize.
                (To match previous matlab version of this code)
    """

    def __init__(self,TrueClass,PredictedValue, OutputFileName='RocOuput.csv'):
        """ Constructor takes two input lists for plotting the ROC Curve.
            Parameters:
                TrueClass = 1 for positive class and TrueClass = -1 for negative class
                PredictedValue is the real valued-list of size equal to TrueClass
        """
        #Initialization of variables
        self.TrueClass = TrueClass        
        self.PredictedValue=PredictedValue
        self.OutputFileName=OutputFileName
        self.TotalPositiveClass=0
        self.TotalNegativeClass=0        
        self.FalsePositiveRate=[]
        self.TruePositiveRate=[]            
        self.CumulativePositive=0
        self.CumulativeNegative=0
        self.AUC=0
        self.auc()
        self.computeTrueAndFalsePositiveRate()
        #self.saveToFile(self.OutputFileName)        
        #self.plot()
    
    def computeTrueAndFalsePositiveRate(self):
        """     Compute TruePositiveRate and FalsePositive Rate Sorts predicted values in descending order and use the indices to sort True class
             labels to compuate 
            Parameters:
                None
            Return:
                None
        """
        
        #Computing the Total of Positive and Negative class data points
        for n,i in enumerate(self.TrueClass):
            if (i>0):
                self.TrueClass[n]=1
                self.TotalPositiveClass=self.TotalPositiveClass+1;
            if (i<=0):
                self.TrueClass[n]=-1
                self.TotalNegativeClass=self.TotalNegativeClass+1;
        #Reordering TrueClass labels to map to sorted order of Predicted Values
        self.SortedPredictedValueIndx=[i[0] for i in sorted(enumerate(self.PredictedValue), key=lambda x:x[1], reverse=True)]
        self.ReorderedTrueClass=[ self.TrueClass[i] for i in self.SortedPredictedValueIndx]
        
        for i in range(0, len(self.ReorderedTrueClass)):
            if (self.ReorderedTrueClass[i]==1):
                self.CumulativePositive=self.CumulativePositive+1.0;
                self.TruePositiveRate.append(float(self.CumulativePositive/self.TotalPositiveClass))
                self.FalsePositiveRate.append(float(self.CumulativeNegative/self.TotalNegativeClass))                
                self.AUC=self.AUC+ ((1-(self.CumulativeNegative/self.TotalNegativeClass))/self.TotalPositiveClass)
            if (self.ReorderedTrueClass[i]==-1):
                self.CumulativeNegative=self.CumulativeNegative+1.0;
                self.TruePositiveRate.append(float(self.CumulativePositive/self.TotalPositiveClass))
                self.FalsePositiveRate.append(float(self.CumulativeNegative/self.TotalNegativeClass))
            
        
    def auc(self):
        """ Computes the area under the curve            
            Parameters:
                None
            Return:
                Area under ROC curve (AUC) (float)
        """
        return self.AUC
    def saveToFile(self,OutputFileName='RocOuput.csv'):
        """ Save the results to a file            
            Parameters:
                OutputFileName
        """        
        outputFile = open(OutputFileName, "w")
        for i in range(len(self.TruePositiveRate)):                
            print >>outputFile, self.TruePositiveRate[i], ',',self.FalsePositiveRate[i]


    def plot(self,ViewPlot,SavePlot,PlotTitle='Receiver operating characteristic (ROC)', PlotFileName='ROCPlot.png'):
        """ Generates a plot of the ROC curve 
            Parameters:
                PlotTitle: Title of the ROC plot
        """
        
        pl.clf()    
        pl.ylim((0,1))
        pl.xlim((0,1))
        pl.xticks(pl.arange(0,1.1,.1))
        pl.yticks(pl.arange(0,1.1,.1))
        pl.grid(True)
        pl.plot([0, 1], [0, 1], 'k--')
        pl.plot(self.FalsePositiveRate, self.TruePositiveRate, 'r-')
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title(PlotTitle)
        pl.text(0.7,0.15,"AUC: %0.2f" %(self.auc()))
        if SavePlot:
            pl.savefig(PlotFileName)
        if ViewPlot:
            pl.show()
            
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot ROC and compute AUC")     
    #potential argument
    parser.add_argument("-t", action="store", type=str,
                 dest="TrueLabelsFile",
                 help="The name of the input file containing true labels. The two classes of the true labels are (\'1\' or \'-1\'). " +\
            "Alternatively, the two classes can be represented by real value ranges (\'>0\' or \'<=0\')")
    parser.add_argument("-p", action="store", type=str,
                 dest="PredictedValueFile",
                 help="The name of the input file containing the predicted probabilities. Required if providing TrueLabelsFile. " +\
            "Value of the predicted label can be any real number. The length of this file must match the length of TrueLabelsFile")
    parser.add_argument("-i", action="store", type=str,
                 dest="InputFile",
                 help="The name of the input file containing both true labels and predicted labels in two columns.")
    parser.add_argument("-o", action="store", type=str,
                 dest="OutputFileName",
                 default="ROCOutput.csv",
                 help="The name of the output file. The output file returns the tuple of TruePositiveRate and FalsePositiveRate at each quantile.")    
    parser.add_argument("-s", action="store_true",
                 dest="SavePlot",
                 default=False,
                 help="Set flag to save plot. The default option is to not save the plot.")
    parser.add_argument("-v", action="store_false",
                 dest="ViewPlot",
                 default=True,
                 help="Set flag to view the plot. The default option is to view the plot.")
    parser.add_argument("-w", action="store_true",
                 dest="SaveText",
                 default=False,
                 help="Set flag to save the csv file containing the tuple of TruePositiveRate and FalsePositiveRate at each quantile. "+\
                     "The default file name is \'ROCOutput.csv\' .")
    parser.add_argument("-title", action="store", type=str,
                 dest="PlotTitle",
                 default="Receiver operating characteristic (ROC)",
                 help="Title of plot")
    parser.add_argument("-f", action="store", type=str,
                 dest="PlotFileName",
                 default="ROCOutput.png",
                 help="The file name of the .png plot. The output file returns the tuple of TruePositiveRate and FalsePositiveRate at each quantile.")
    # parse command line
    Args = parser.parse_args()
    Opts = dict(vars(Args))
    Separator=','
    TrueLabel=[]
    PredictedValue=[]
    if (Opts['InputFile'] is not None):
        File = open(Args.InputFile, 'r')
        for Line in File:
            # split the line into a list of column values
            Columns = Line.split(Separator)
            # clean any whitespace off the items
            Columns = [Col.strip() for Col in Columns]    
            # ensure the column has at least one value before printing
            if Columns:
                TrueLabel.append(Decimal(Columns[0]))  
                PredictedValue.append(Decimal(Columns[-1]))# Columns[-1] # print the last column
        File.close()
        ROCObj = ROC(TrueLabel, PredictedValue)
        print("AUC of the ROC plot: %s" % (str(ROCObj.auc()),))
        ROCObj.plot(Args.ViewPlot,Args.SavePlot,Args.PlotTitle, Args.PlotFileName)
        if (Opts['SaveText']==True):
            if Opts.has_key('OutputFileName'):
                ROCObj.saveToFile(Args.OutputFileName)
            
    else:
        if (Opts['TrueLabelsFile'] is not None):
            if (Opts['PredictedValueFile'] is None):
                print('If an input file is not provided, both TrueLabel and PredictedValue files need to be provided.')
            else:
                File = open(Args.TrueLabelsFile, 'r')
                for Line in File:
                    Columns = Line.split(Separator)
                    Columns = [Col.strip() for Col in Columns]
                    if Columns:
                        TrueLabel.append(Decimal(Columns[0]))  
                File.close()
                File = open(Args.PredictedValueFile, 'r')
                for Line in File:
                    Columns = Line.split(Separator)
                    Columns = [Col.strip() for Col in Columns]
                    if Columns:
                        PredictedValue.append(Decimal(Columns[0]))  
                File.close()
                if len(PredictedValue)==len(TrueLabel):                
                    ROCObj = ROC(TrueLabel, PredictedValue)
                    print("AUC of the ROC plot: %s" % (str(ROCObj.auc()),))
                    ROCObj.plot(Args.ViewPlot,Args.SavePlot,Args.PlotTitle, Args.PlotFileName)
                    if (Opts['SaveText']==True):
                        if Opts.has_key('OutputFileName'):
                            ROCObj.saveToFile(Args.OutputFileName)
                else:
                    print('The two input files are not of the same length.')
    
    
    
    

          
          
          
          




