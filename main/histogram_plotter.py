import os
import matplotlib.pyplot as plt
import utils
import numpy as np
import scipy.stats as stats
import fitters

class HistogramPlotter:

    _default_figure_folder = os.path.join(utils.PROJECT_DIR,'figures','histograms')

    def __init__(self):
        pass

    def plotHistogram(self,data,labels_to_plot='all',series='all',nbins=10,transformations=None,save=True,draw_normal=True,draw_bimodal=True):
        if transformations is None:
            transformations = [(lambda x: x,'')]
        timestamp = utils.s_timestamp()
        figure_folder = os.path.join(self._default_figure_folder,timestamp)
        if save:
            #create a separate_folder
            if not os.path.exists(figure_folder):
                os.makedirs(figure_folder)
        if series == 'all':
            series = data.keys()
        if labels_to_plot == 'all':
            labels_to_plot = data[series[0]].keys()
        fitters_ = []
        if draw_normal:
            fitters_.append(fitters.NormalFitter)
        if draw_bimodal:
            fitters_.append(fitters.BiModalFitter)

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

                    title = transformation_label+' '+serie_name+' '
                    n, bins, patches = plt.hist(transformed_data, bins=nbins, normed=False)
                    data_pdf = n/sum(n)
                    bin_centers = [(bins[i_]+bins[i_+1])/2.0 for i_ in range(len(bins)-1)]
                    #plt.xlabel(transformation_label+' '+label_to_plot)
                    plt.ylabel('Count')
                    fitted = []
                    for fitter in fitters_:
                        temp = fitter(transformed_data)
                        fitted.append(temp)
                        p = temp.pdf(bin_centers)
                        plt.plot(bin_centers, p*sum(n), 'k', linewidth=2)
                        mse = (np.array(data_pdf-p)**2).mean()*100
                        #title += '\nmse {0}:{1:.2f}'.format(temp._descr,mse)
                    fitter_combinations = [(f1i,f2i) for f1i,f1 in enumerate(fitters_) for f2i,f2 in enumerate(fitters_) if f1i < f2i]
                    for f1i,f2i in fitter_combinations:
                        f1,f2 = fitted[f1i],fitted[f2i]
                        title += ' {0}vs{1}:{2:.2f}'.format(f1._descr,f2._descr,self.f_test(n/sum(n),f1.pdf(bin_centers),f2.pdf(bin_centers),f1._n_params,f2._n_params,len(transformed_data)))
                    plt.title(title)
            if save:
                plt.savefig(os.path.join(figure_folder,self.getDescr(label_to_plot))+'.png')
            else:
                plt.show()

    def getDescr(self,label_to_plot):
        return label_to_plot

    @staticmethod
    def f_test(y_true,y1,y2,p1,p2,n):
        rss1 = sum(np.array(y_true-y1)**2)
        rss2 = sum(np.array(y_true-y2)**2)
        if rss1 < rss2:
            return 0
        return ((rss1-rss2)/(p2-p1))/(rss2/(n-p2+1))

