from histogram_plotter import HistogramPlotter
from mann_whitney_utest import MannWhitneyUTest
from data_reader import DataReader
import scipy as sp

def main():
    data = DataReader().load()
    '''
    HistogramPlotter().plotHistogram(data, ['shmooing dist', 'lenght', 'time until shmooing'],
                                     series=['WT','Ste11(S243A)'], nbins=15,
                                     transformations=[(lambda x: x,''),
                                                     (lambda x: sp.log(x),'log'),
                                                     (lambda x: 1.0/x,'1/x'),
                                                     (lambda x: sp.sqrt(x),'sqrt')])
    '''
    MannWhitneyUTest().run(data,series=['shmooing dist','lenght','time until shmooing'],strains=['WT','Ste11(S243A)'])

if __name__ == "__main__":
    main()