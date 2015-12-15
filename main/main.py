from histogram_plotter import HistogramPloter
from data_reader import DataReader
import scipy as sp

def main():
    data = DataReader().load()
    HistogramPloter().plotHistogram(data,['shmooing dist','lenght','time until shmooing'],
                                    series=['WT','Ste11(S243A)'],nbins=15,
                                    transformations=[(lambda x: x,''),
                                                     (lambda x: sp.log(x),'log'),
                                                     (lambda x: 1.0/x,'1/x'),
                                                     (lambda x: sp.sqrt(x),'sqrt')])


if __name__ == "__main__":
    main()