import os
import matplotlib.pyplot as plt
import datetime
import numpy as np
import scipy.stats as stats
import scipy as sp
from sklearn import mixture

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')

class HistogramPloter:

    _default_figure_folder = os.path.join(PROJECT_DIR,'figures','histograms')

    def __init__(self):
        pass

    def plotHistogram(self,data,labels_to_plot='all',series='all',nbins=10,transformations=None,save=True,draw_normal=True,draw_bimodal=True):
        if transformations is None:
            transformations = [(lambda x: x,'')]
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
            plt.figure(figsize=(10,15))
            i = 1
            for transformation_fun,transformation_label in transformations:
                for serie_name in series:
                    plt.subplot(len(transformations),len(series),i)
                    i += 1
                    series_data = data[serie_name]
                    if label_to_plot not in series_data:
                        raise ValueError('Label "{0}" not in series "{1}"'.format(label_to_plot,serie_name))
                    raw_data = np.array([val for val in series_data[label_to_plot] if val is not None])
                    transformed_data = transformation_fun(raw_data)

                    title = serie_name+' '+transformation_label
                    n, bins, patches = plt.hist(transformed_data, bins=nbins, normed=False)
                    data_pdf = n/sum(n)
                    bin_centers = [(bins[i_]+bins[i_+1])/2.0 for i_ in range(len(bins)-1)]
                    plt.xlabel(transformation_label+' '+label_to_plot)
                    plt.ylabel('Count')
                    k = len(raw_data)
                    if draw_normal:
                        mu, std = stats.norm.fit(transformed_data)
                        p = stats.norm.pdf(bin_centers, mu, std)
                        p = p/sum(p)
                        plt.plot(bin_centers, p*sum(n), 'k', linewidth=2)
                        chi_squared,p = stats.normaltest(transformed_data)
                        mse = (np.array(data_pdf-p)**2).mean()*100
                        title += ' p:{0:.2f} mse:{1:.2f}'.format(p,mse)

                    if draw_bimodal:
                        g = mixture.GMM(n_components=2)
                        g.fit(np.matrix([transformed_data],dtype='float32').T)
                        logprob,responsibilities  = g.score_samples(np.matrix([bin_centers],dtype='float32').T)
                        prob = sp.exp(logprob)
                        prob = prob/sum(prob)
                        plt.plot(bin_centers,prob*sum(n), 'r',linewidth=2)
                        mse = (np.array(data_pdf-prob)**2).mean()*100
                        title += ' mse-bi:{0:.2f}'.format(mse)
                    plt.title(title)
                plt.tight_layout()
            if save:
                plt.savefig(os.path.join(figure_folder,self.getDescr(label_to_plot,transformation_label))+'.png')
            else:
                plt.show()

    def getDescr(self,label_to_plot,transformation_label):
        return label_to_plot+' '+transformation_label


