# Utils
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
from scipy.stats import t
import numpy as np

#------------------------------------------------------------------------------------------
# Mean, Standard Deviation, and Margin Error

def mean_std_error(X, data, stds=[]):
    '''
    Calculate the mean, standard deviation, and the margin error for a given dataset.

    Input:
    -                       X (int): Size
    - data (float, numpy.narray[?]): Data List
    - stds (float, numpy.narray[?]): Samples Standard Deviations List

    Output:
    -                  mean (float): Mean    
    -                   std (float): Standard Deviation        
    -                 error (float): Margin Error    
    '''  

    if (len(stds) == 0):
        m, n = 1, X                                 # t-Student Parameters
        std = np.std(data,ddof=1)                   # Standard Deviation
    else:
        m, n = len(stds), len(stds)                 # t-Student Parameters
        std  = np.sqrt(np.sum(np.array(stds)**2)/n) # Standard Deviation

    mean  = np.mean(data)                               # Mean
    error = t.ppf(0.9950,df=m*(X-1)) * (std/np.sqrt(n)) # Margin Error (99%)
        
    return mean,std,error 

#------------------------------------------------------------------------------------------

# Model
def model(T, ΔM):
    '''
    Fit the ZFC and FC magnetizations difference.

    Input:
    -       T (float, numpy.ndarray[X1]): Temperature List
    -      ΔM (float, numpy.ndarray[X1]): ZFC and FC Magnetizations Difference List

    Output:
    - ΔM_pred (float, numpy.ndarray[X1]): ZFC and FC Magnetizations Difference List (Fitted)                        
    '''  
    
    # Feature Scaling
    sc_x = MinMaxScaler()
    sc_y = MinMaxScaler()
    T    = sc_x.fit_transform(T.reshape(-1,1))
    ΔM   = sc_y.fit_transform(ΔM.ravel().reshape(-1,1))

    # Machine Learning Model
    model = SVR(kernel='rbf', C=100.0, epsilon=0.0001)
    model.fit(T,ΔM.ravel())

    # Prediction
    ΔM_pred = model.predict(T).reshape(-1,1)

    # Inverse Scaling
    T       = sc_x.inverse_transform(T).ravel()
    ΔM_pred = sc_y.inverse_transform(ΔM_pred).ravel()    
    
    return ΔM_pred 