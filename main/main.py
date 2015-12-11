from histogram_plotter import HistogramPloter
from data_reader import DataReader


def main():
    data = DataReader().load()
    HistogramPloter().plotHistogram(data,['shmooing dist','lenght','time until shmooing'],
                                    series=['WT','Ste11(S243A)'],nbins=15,normed=False)


if __name__ == "__main__":
    main()