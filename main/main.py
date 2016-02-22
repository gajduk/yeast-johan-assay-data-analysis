from violin_plotter import ViolinPlotter
from data_reader import DataReader
import scipy as sp

def main():
    data = DataReader().load()
    '''
    HistogramPlotter().plotHistogram(data, ['shmooing dist', 'lenght', 'time until shmooing'],
                                     series=['WT','Ste11(S243A)'], nbins=15,
                                     transformations=)
    '''
    ViolinPlotter().plotViolin(data,labels_to_plot=['shmooing dist','actual time until shmooing'],series=['WT','Ste11(S243A)'])

if __name__ == "__main__":
    main()