import scipy.stats as stats
import scipy as sp
from sklearn import mixture
import numpy as np

class Fitter(object):

    def __init__(self,data,descr,n_params):
        self._data = data
        self._fit(data)
        self._descr = descr
        self._n_params = n_params

    def _fit(self,data):
        pass

    def pdf(self,points):
        '''Computes a pdf for the given points.
        :param points: a list of points for which the pdf should be computed
        :return: a list of probabilities corresponding to each element in points. the sum of all elements in the returned list is 1
        '''

class NormalFitter(Fitter):
    '''
    Fits a normal distribution with mean mu_ and standard deviation std_.
    Uses stats.norm.fit
    '''

    def __init__(self,data):
        super(NormalFitter, self).__init__(data,'normal',2)

    def _fit(self,data):
        self._mu,self._std = stats.norm.fit(data)

    def pdf(self,points):
        p = stats.norm.pdf(points, self._mu, self._std)
        return p/sum(p)

class BiModalFitter(Fitter):
    '''
    Fits a bimodal distribution to the data.
    Uses mixture.GMM
    '''

    def __init__(self,data):
        super(BiModalFitter, self).__init__(data,'bi-modal',4)

    def _fit(self,data):
        self._g = mixture.GMM(n_components=2)
        self._g.fit(np.matrix([data],dtype='float32').T)

    def pdf(self,points):
        logprob,_  = self._g.score_samples(np.matrix([points],dtype='float32').T)
        p = sp.exp(logprob)
        p = p/sum(p)
        return p/sum(p)