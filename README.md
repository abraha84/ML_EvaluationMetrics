# ML_EvaluationMetrics
Repository of a few popular evaluation metrics and plots (ROC, AUC, etc.)


class ROC(builtins.object)
 |  A class that plots an ROC Curve and returns AUC.
 |  Input data is two list TrueClass and PredictedValue
 |  where:
 |      TrueClass = 1 for positive class and TrueClass = -1 for negative class
 |      PredictedValue is the real valued-list of size equal to TrueClass
 |      AUC= Area under the curve;
 |          AUC was computed by using TotalArea=PositiveClassSize*NegativeClassSize.
 |          (To match previous matlab version of this code)
 |  
 |  Methods defined here:
 |  
 |  __init__(self, TrueClass, PredictedValue, OutputFileName='RocOuput.csv')
 |      Constructor takes two input lists for plotting the ROC Curve.
 |      Parameters:
 |          TrueClass = 1 for positive class and TrueClass = -1 for negative class
 |          PredictedValue is the real valued-list of size equal to TrueClass
 |  
 |  auc(self)
 |      Computes the area under the curve            
 |      Parameters:
 |          None
 |      Return:
 |          Area under ROC curve (AUC) (float)
 |  
 |  computeTrueAndFalsePositiveRate(self)
 |      Compute TruePositiveRate and FalsePositive Rate Sorts predicted values in descending order and use the indices to sort True class
 |       labels to compuate 
 |      Parameters:
 |          None
 |      Return:
 |          None
 |  
 |  plot(self, ViewPlot, SavePlot, PlotTitle='Receiver operating characteristic (ROC)', PlotFileName='ROCPlot.png')
 |      Generates a plot of the ROC curve 
 |      Parameters:
 |          PlotTitle: Title of the ROC plot
 |  
 |  saveToFile(self, OutputFileName='RocOuput.csv')
 |      Save the results to a file            
 |      Parameters:
 |          OutputFileName
 |  
 |  ----------------------------------------------------------------------
