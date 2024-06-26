import matplotlib.pyplot as plt
import seaborn as sns

class Visualizations:

    @staticmethod
    def histogram(data, title, color, bins):
        """
        Funtion that more easily allows user to produce a histogram for any given data array.

        Args:
            data (array): the array of data the histogram will plot the distribution for
            title (string): title of the histogram
            color (string): color used for the histogram plots
            bins (int): number of bins used for plotting distribution
        """
        plt.hist(data, color=color, edgecolor='black', bins=bins)
        plt.title(f"{title}")
        plt.show()

    @staticmethod
    def box_plot(data, title, title_size,color):
        """
        Funtion that more easily allows user to produce a boxplot/box & whiskers plot for any given data array.

        Args:
            data (array): the array of data the boxplot will show the different quartiles and graphical outliers
            title (string): title of the graph
            title_size (int): graph title size
            color (string): main color of the boxplot
        """

        plt.boxplot([data],
                        notch=True,
                        patch_artist=True,
                        widths=.1,
                        medianprops= dict(linestyle='-', linewidth=2, color='Yellow'),
                        boxprops = dict(linestyle='--', linewidth=2, color='Black', facecolor =color, alpha = .5)
                        );


   
        plt.xticks(fontsize = 16);
        plt.yticks(fontsize = 16);
        plt.title(f'{title}', fontdict={'fontsize': title_size})
        plt.show()
    

    @staticmethod
    def hist_loop(dataframe, features, color):
        """
        This function loops through a dataframe using the names of the numeric data columns in the dataframe
        in order to generate a histogram for each

        Args:
            dataframe (dataframe): Dataframe being used to generate multiple histogram plots
            features (list): List of all the columns in the desired dataframe
            color (string): color of the main histogram plots
        """
        for feature in features:
            plt.hist(dataframe[feature], color=color, edgecolor='black')
            plt.title(f"{feature} Histogram")
            plt.show()
