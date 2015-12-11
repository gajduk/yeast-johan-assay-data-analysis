import os
import matplotlib.pyplot as plt
import datetime

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')

class HistogramPloter:

    _default_figure_folder = os.path.join(PROJECT_DIR,'figures','histograms')

    def __init__(self):
        pass

    def plotHistogram(self,data,labels_to_plot='all',series='all',nbins=10,normed=True,save=True):

        timestamp = datetime.datetime.now().strftime("%H_%M_%S %d_%m_%y")
        figure_folder = os.path.join(self._default_figure_folder,timestamp)
        if save:
            #create a separate_folder
            if not os.path.exists(figure_folder):
                os.makedirs(figure_folder)
        if series == 'all':
            series = data.keys()
        if labels_to_plot == 'all':
            labels_to_plot = data[series[0]].keys()
        for label_to_plot in labels_to_plot:
            plt.figure()
            for i,serie_name in enumerate(series):
                if len(series) > 1:
                    if len(series) > 2:
                        plt.subplot(2,2,i+1)
                    else:
                        plt.subplot(1,2,i+1)
                series_data = data[serie_name]
                if label_to_plot not in series_data:
                    raise ValueError('Label "{0}" not in series "{1}"'.format(label_to_plot,serie_name))
                plt.hist([val for val in series_data[label_to_plot] if val is not None], bins=nbins, normed=normed)
                plt.xlabel(label_to_plot)
                plt.ylabel('Fraction' if normed else 'Count')
                plt.title(serie_name)
            plt.tight_layout()
            if save:
                plt.savefig(os.path.join(figure_folder,self.getDescr(label_to_plot))+'.png')
            else:
                plt.show()

    def getDescr(self,label_to_plot):
        return label_to_plot


