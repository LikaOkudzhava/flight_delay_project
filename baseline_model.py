
###############################
# ------ Basline model ------ #
###############################

import numpy as np
import pandas as pd

def baseline_model(X,logdur="DURATION_LOG",value=49.11):
    '''
    X: Must include the column defined in 'logdur'
    logdur: Must be a column in X which includes the logarithmic duration
    value: Must be the value which is used as predicted target (49.11 is the mean value of the train data in the mid delay range)
    '''

    y_predict = np.zeros(len(X))

    y_predict[(X[logdur] >= 2.9) & (X[logdur] <= 6.4)] = value

    return y_predict

##############################################################

def baseline_model2(X,value=49.11):
    '''
    X: Must include the column STATUS
    value: Must be the value which is used as predicted target (49.11 is the mean value of the train data for STATUS not in (SCH,DEL))
    '''

    y_predict = np.zeros(len(X))

    y_predict[(X["STATUS"] != "SCH") & (X["STATUS"] != "DEL")] = value

    return y_predict

##############################################################

def get_accuracy(y_true,y_predict,plusminus=10):
    
    inrange = np.zeros(len(y_true))
    inrange[((y_true-plusminus) <= y_predict) & (y_predict <= (y_true+plusminus))] = 1

    return (sum(inrange)/len(y_true))