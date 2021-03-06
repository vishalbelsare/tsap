import numpy as np
import math
from basemodel import base
import matplotlib.pyplot as plt
from gradient_check import eval_numerical_gradient, eval_numerical_gradient_array
import sys




class AR(base):  
    """class AR implements the AR model which has __init__ , loss and predict as functions"""  

    def __init__(self, lag, phi, sigma, intercept):
        """__init__: initialize the model with lag phi sigma and intercept
           Input: 
                 lag: the number of lag in AR model, dimension 1
                 phi: the coefficients for each lag, dimension lag, column vector
                 sigma: the standard deviation of the error term, dimension 1
                 intercept: the constant component in the AR model, dimension 1
           Output:
                 _lag: the number of lag in the AR model
                 params: hash table of phi, sigma and intercept"""

        self._lag = lag
        self.params = {}
        self.params['phi'] = phi 
        self.params['sigma'] = sigma
        self.params['intercept'] = intercept

    ###################################################################


    def loss(self, X, lag=None, phi=None, sigma=None, intercept=None):
        """loss: return the loglikelihood and its gradient with respect to phi, sigma and intercept
           Input: 
                 X: the input time series, each row is about one stock. For one stock, X is a row vector. Note phi is a column vector
           Output:
                  loglikelihood: the loglikelihood that calculated from the input time series
                  grads: hash table that records the gradient of phi sigma and intercept"""


        """the number of samples, usually it's about how many stocks we have """
        num_data = X.shape[0]
        """the length of time"""
        input_dim = X.shape[1] 

        """parameters""" 
        if lag is None:  
            lag = self._lag  
        if phi is None:  
            phi = self.params['phi']
        if sigma is None:
            sigma = self.params['sigma']
        if intercept is None:
            intercept = self.params['intercept']
        
        """initialization"""
        loglikelihood = 0.0
        grad_phi = np.zeros((lag,1))
        grad_intercept = 0.0
        grad_sigma = 0.0

        """get the expression of loglikelihood and its gradient with respect to phi, sigma and intercept"""
        for i in range(input_dim - lag):
            """np.flipud can flip the vector"""
            temp = intercept + np.dot(X[0,i:(i+lag+1)], np.vstack((np.flipud(phi),-1.0)))
            
            loglikelihood -= temp**2
            
            grad_phi -= float(temp) * (np.fliplr(np.matrix(X[0,i:(i+lag)]))).T
            
            grad_intercept -= temp
            grad_sigma += temp**2

        loglikelihood = loglikelihood / (2 * sigma**2)
        loglikelihood += (lag - input_dim) / 2.0 * math.log(sigma**2)

        loglikelihood -= (input_dim-lag)/2.0 * math.log(2*math.pi)
        grad_phi = grad_phi / (sigma**2)
        grad_intercept = grad_intercept / (sigma**2)
        grad_sigma = grad_sigma / (sigma**3)
        grad_sigma += (lag - input_dim) / sigma

        """grad_phi is a column vector"""
        grads = {} 
        grads['phi'] = -grad_phi   
        grads['intercept'] = -grad_intercept 
        grads['sigma'] = -grad_sigma

        return -loglikelihood, grads

    ###################################################################

    
    def predict(self, X, nstep, lag=None, phi=None, sigma=None, intercept=None):
        """predict: return the predicted series based on the samples given
           Input: 
                 X: the input time series, each row is about one stock. For one stock, X is a row vector. Note phi is a column vector
                 nstep: the number of steps to predict
           Output:
                  pred_state: the predicted series based on AR model, which is a row vector"""

        """parameters"""
        if lag is None:  
            lag = self._lag  
        if phi is None:  
            phi = self.params['phi']
        if sigma is None:
            sigma = self.params['sigma']
        if intercept is None:
            intercept = self.params['intercept']


        """the length of time"""
        input_dim = X.shape[1] 
        """check whether there's enough input"""
        if input_dim < lag:
            print "The data is not enough"
            exit(0)

        """pred_state stores the predicted series, it is a row vector """
        pred_state = []
        for i in range(nstep):
            pred_state.append(0.0)

        """define the training set"""
        train = np.hstack((X[0,(input_dim-lag):input_dim], pred_state))

        """make the pred_state as numpy array"""
        pred_state = np.array([pred_state])
        for i in range(nstep):
            """prediction"""
            pred_state[0,i] = np.dot(train[i:(i+lag)],np.flipud(phi)) + intercept
            """update training set"""
            train[lag+i] = pred_state[0,i]

        return pred_state


###################################################################


"""class MA implements the MA model which has __init__ , loss and predict"""
"""__init__: initialize the model with lag phi sigma and intercept"""
"""loss: calculate the loglikelihood"""
"""predict: does the prediction. Given the sample, it predicts future prices """
class MA(base):
    def __init__(self, lag, phi, sigma, intercept):
        """lag, phi, sigma, intercept is the parameter of AR"""
        self._lag = lag
        self.params = {}
        self.params['phi'] = phi 
        self.params['sigma'] = sigma
        self.params['intercept'] = intercept

    ###################################################################

    def loss(self, X, lag=None, phi=None, sigma=None, intercept=None):
        if lag is None:  
            lag = self._lag  
        if phi is None:  
            phi = self.params['phi']
        if sigma is None:
            sigma = self.params['sigma']
        if intercept is None:
            intercept = self.params['intercept']
        loglikelihood = self.get_loglikelihood(X, lag=lag, phi=phi, sigma=sigma, intercept=intercept)
        """grad_phi is a column vector"""
        grads = {} 
        grads['phi'] = eval_numerical_gradient_array(lambda phi: self.get_loglikelihood(X, lag,phi,sigma,intercept), phi, 1)   
        grads['intercept'] = eval_numerical_gradient_array(lambda intercept: self.get_loglikelihood(X, lag,phi,sigma,intercept), intercept, 1)
        grads['sigma'] = eval_numerical_gradient_array(lambda sigma: self.get_loglikelihood(X, lag,phi,sigma,intercept), sigma, 1)
        return loglikelihood, grads

    def get_loglikelihood(self, X, lag=None, phi=None, sigma=None, intercept=None):
        """X is dataset, right now X is a row vector"""
        """phi is a column vector, and we need to make it into matrix form"""

        input_dim = X.shape[1]    
        if lag is None:  
            lag = self._lag  
        if phi is None:  
            phi = self.params['phi']
        if sigma is None:
            sigma = self.params['sigma']
        if intercept is None:
            intercept = self.params['intercept']

        
        """initialization"""
        loglikelihood = 0

        loglikelihood =- float(input_dim) / 2 * math.log(2*math.pi*sigma**2)

        """Derive autocorrelation for likelihood function"""
        autocov = np.zeros((lag+1,1))
        temp = sigma**2+ phi.T.dot(phi) * sigma**2

        autocov[0]=temp
        if lag>1.0:
            for i in range(lag-1):
                temp = np.dot(phi[0:lag-i-1].T,phi[i+1:lag])*sigma**2
                autocov[i+1]=temp-phi[i]*sigma**2
        autocov[lag]=-phi[lag-1]*sigma**2

        """Derive the covariance matrix for likelihood function"""
        covmat=np.zeros((input_dim,input_dim))
        for i in range(input_dim):
            for j in range(i+1):
                if abs(i-j)<=lag:
                    covmat[i,j]=autocov[abs(i-j)]
                    covmat[j,i]=autocov[abs(i-j)]
        
        loglikelihood -= 0.5*np.linalg.slogdet(covmat)[1]+ 1.0/(2 * sigma**2) * np.dot(np.dot(X,np.linalg.inv(covmat)),X.T)[0,0]
        return -loglikelihood

    ###################################################################
        
    """predict: does the prediction. Given the sample, it predicts future prices. nstep: how many future prices you wanna predict """
    def predict(self, X, nstep):
        """X is a row vector"""
        lag = self._lag    
        phi = self.params['phi']
        sigma = self.params['sigma']
        intercept = self.params['intercept']
        input_dim = X.shape[1]

        """pred_state stores the predicted prices, it is a row vector """
        pred_state = []
        for i in range(nstep):
            pred_state.append(0)

        train = np.hstack((X[0,(input_dim-lag):input_dim], pred_state))
        for i in range(nstep):
            pred_state[i] = np.dot(train[i:(i+2)],phi) + intercept

        return pred_state

###################################################################




def plot_price(X):
    plt.plot(X)
    plt.ylabel('stock prices')
    plt.show()

def plot_price_pred_vs_true (X, Y):
    plt.plot(X,'b')
    plt.plot(Y,'r')
    plt.ylabel('stock prices')
    plt.show()

