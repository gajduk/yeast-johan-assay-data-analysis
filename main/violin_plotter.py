import os
import matplotlib.pyplot as plt
import utils
import numpy as np

class ViolinPlotter:

    _default_figure_folder = os.path.join(utils.PROJECT_DIR,'figures','violin plots')

    def __init__(self):
        pass

    def plotViolin(self,data,labels_to_plot='all',series='all',transformations=None,save=True):
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

        for label_to_plot in labels_to_plot:
            plt.figure(figsize=(10,15))
            data_to_plot = []
            for transformation_fun,transformation_label in transformations:
                for serie_name in series:
                    series_data = data[serie_name]
                    if label_to_plot not in series_data:
                        raise ValueError('Label "{0}" not in series "{1}"'.format(label_to_plot,serie_name))
                    raw_data = np.array([val for val in series_data[label_to_plot] if val is not None])
                    transformed_data = transformation_fun(raw_data)
                    data_to_plot.append(transformed_data)
            plt.ylabel(label_to_plot)
            plt.title(label_to_plot)
            plt.violinplot(data_to_plot,showmedians=True)
            plt.xticks( range(1,1+len(series)), series )
            plt.ylim([min([qwe for asd in data_to_plot for qwe in asd])-3,max([qwe for asd in data_to_plot for qwe in asd])+3])
            if save:
                plt.savefig(os.path.join(figure_folder,self.getDescr(label_to_plot))+'.png')
            else:
                plt.show()

    def getDescr(self,label_to_plot):
        return label_to_plot
