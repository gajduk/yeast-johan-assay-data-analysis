import os
import numpy as np
from numpy import asarray
import utils
from scipy.stats._rank import rankdata,tiecorrect
from scipy.stats.distributions import norm

class MannWhitneyUTest:

    _default_res_folder = os.path.join(utils.PROJECT_DIR,'results','mann-whitney-test')

    def __init__(self):
        pass

    def run(self,data,series,strains):
        all_pairs = [(i1,i2) for i1,_ in enumerate(strains) for i2,_ in enumerate(strains) if i1 < i2]
        with open(os.path.join(self._default_res_folder,utils.s_timestamp()+'.txt'),'w') as pout:
            for series_name in series:
                for i1,i2 in all_pairs:
                    strain1,strain2 = strains[i1],strains[i2]
                    data1,data2 =  utils.removeNoneValues(data[strain1][series_name]),utils.removeNoneValues(data[strain2][series_name])
                    smallu,bigu,z,p = self.mannwhitneyu(data1,data2)
                    pout.write('Strain1: {0: <13} Strain2: {1: <13} Series: {2: <20} p: {3:8.5f}\n'
                               .format(strain1,strain2,series_name,p))

    def mannwhitneyu(self,x,y,use_continuity=True):
        x = asarray(x)
        y = asarray(y)
        n1 = len(x)
        n2 = len(y)
        ranked = rankdata(np.concatenate((x, y)))
        rankx = ranked[0:n1]  # get the x-ranks
        u1 = n1*n2 + (n1*(n1+1))/2.0 - np.sum(rankx, axis=0)  # calc U for x
        u2 = n1*n2 - u1  # remainder is U for y
        bigu = max(u1, u2)
        smallu = min(u1, u2)

        T = tiecorrect(ranked)
        sd = np.sqrt(T * n1 * n2 * (n1+n2+1) / 12.0)
        if use_continuity:
            # normal approximation for prob calc with continuity correction
            z = abs((bigu - 0.5 - n1*n2/2.0) / sd)
        else:
            z = abs((bigu - n1*n2/2.0) / sd)  # normal approximation for prob calc
        p =  norm.sf(z)
        return smallu, bigu, z, p
