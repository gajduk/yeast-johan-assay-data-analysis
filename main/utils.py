import datetime
import os
import scipy as sp

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')

def removeNoneValues(x):
    return [val for val in x if val is not None]

def s_timestamp():
    return datetime.datetime.now().strftime("%H_%M_%S %d_%m_%y")

def getCommonTransformations():
    return [(lambda x: x,''),
         (lambda x: sp.log(x),'log'),
         (lambda x: 1.0/x,'1/x'),
         (lambda x: sp.sqrt(x),'sqrt')]