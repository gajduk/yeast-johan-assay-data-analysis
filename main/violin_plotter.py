import os
import matplotlib.pyplot as plt
import utils
import numpy as np
import matplotlib

class ViolinPlotter:

    _default_figure_folder = os.path.join(utils.PROJECT_DIR,'figures','violin plots')
    _nice_labels= {'shmooing dist':'Shmooing distance [$\mu$m]','actual time until shmooing':'Time until shmooing [min]'};
    _nice_series= {'WT':'WT','Ste11(S243A)':'Ste11\n(S243A)'};
    _series_colors = {'WT':'gray','Ste11(S243A)':'#8E3A59'}
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
            plt.figure(figsize=(3,3.4))
            ax=plt.subplot()
            data_to_plot = []
            for transformation_fun,transformation_label in transformations:
                for serie_name in series:
                    series_data = data[serie_name]
                    if label_to_plot not in series_data:
                        raise ValueError('Label "{0}" not in series "{1}"'.format(label_to_plot,serie_name))
                    raw_data = np.array([val for val in series_data[label_to_plot] if val is not None])
                    transformed_data = transformation_fun(raw_data)
                    data_to_plot.append(transformed_data)
            plt.ylabel(self._nice_labels[label_to_plot])
            #plt.title(label_to_plot)
            violin_parts = plt.violinplot(data_to_plot,showmedians=True)
            pc_idx = 0
            for idx,pc in enumerate(violin_parts['bodies']):
                pc_idx += 1
                pc.set_facecolor(self._series_colors[series[idx]])
                pc.set_edgecolor('black')
                pc.set_linewidth(1)
            plt.xticks( range(1,1+len(series)), [self._nice_series[serie] for serie in series])
            labels_font = matplotlib.font_manager.FontProperties(family='arial', style='normal', size=9, weight='normal', stretch='normal')
            plt.ylim([min([qwe for asd in data_to_plot for qwe in asd])-3,max([qwe for asd in data_to_plot for qwe in asd])+3])
            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                     ax.get_xticklabels() + ax.get_yticklabels()):
                item.set_fontproperties(labels_font)
            plt.tight_layout()
            if save:
                plt.savefig(os.path.join(figure_folder,self.getDescr(label_to_plot))+'.png')
            else:
                plt.show()

    def getDescr(self,label_to_plot):
        return label_to_plot
