import numpy as np
import pandas as pd
from matplotlib import  cm
import matplotlib.pyplot as plt
import seaborn as sns


class PlottingData(object):
    def __init__(self, name, history, series_styles=('b','r')):
        self.Name = name
        self.History = history
        self.SeriesStyles = series_styles


class PlotData:
    def __init__(self):
        self._legend = True


class SeriesData:
    def __init__(self):
        self._x_label = None


class Visualizer(object):
    def __init__(self):
        self.Style = None#'ggplot'
        self.figure_num = 0
        plt.figure(self.figure_num)

    def increment_figure(self):
        plt.figure(self.figure_num + 1)

    def plot(self, x, y):
        plt.plot(x, y)

    def save(self, name):
        plt.savefig(name)

    def show(self):
        if self.Style:
            plt.style.use(self.Style)
        plt.show()

    def display_plot(self, alpha_space, cv_scores, cv_scores_std):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(alpha_space, cv_scores)

        std_error = cv_scores_std / np.sqrt(10)

        ax.fill_between(alpha_space, cv_scores + std_error, cv_scores - std_error, alpha=0.2)
        ax.set_ylabel('CV Score +/- Std Error')
        ax.set_xlabel('Alpha')
        ax.axhline(np.max(cv_scores), linestyle='--', color='.5')
        ax.set_xlim([alpha_space[0], alpha_space[-1]])
        ax.set_xscale('log')

    def boxplot(data_frame, x_column_name, y_column_name, rot):
        data_frame.boxplot(x_column_name, y_column_name, rot=rot)

    def plot_bar(self, xlabel, ylabel, data):
        sns.barplot(xlabel, ylabel, data)
        #sns.barplot(x='Age', y='Survived', data=average_age)

    #train[[u'Survived', u'Pclass', u'Sex', u'Age', u'Parch', u'Fare', u'Embarked', u'FamilySize', u'Title']]
    def plot_pairplot(self, features):
        g = sns.pairplot(features, hue='Survived', palette='seismic', size=1.2, diag_kind='kde',
                         diag_kws=dict(shade=True), plot_kws=dict(s=10))
        g.set(xticklabels=[])

    def plot_distributions(self, df, y):
        pd.scatter_matrix(df, c=y, figsize=[8, 8], s=150, marker='D')
        self.increment_figure()

    def plot_correlations(self, correlations, size=11):
        fig, ax = plt.subplots(figsize=(size, size))
        ax.matshow(correlations)
        plt.xticks(range(len(correlations.columns)), correlations.columns)
        plt.yticks(range(len(correlations.columns)), correlations.columns)
        plt.legend()
        self.increment_figure()

    #train.astype(float).corr()
    def plot_heatmap(self, correlations):
        colormap = plt.cm.RdBu
        plt.figure(figsize=(14, 12))
        plt.title('Pearson Correlation of Features', y=1.05, size=15)
        sns.heatmap(correlations, linewidths=0.1, vmax=1.0,
                    square=True, cmap=colormap, linecolor='white', annot=True)
        self.increment_figure()

    def plot_model_complexity(neighbors, train_accuracy, test_accuracy):
            # Generate plot
            plt.title('k-NN: Varying Number of Neighbors')
            plt.plot(neighbors, test_accuracy, label='Testing Score')
            plt.plot(neighbors, train_accuracy, label='Training Score')
            plt.legend()
            plt.xlabel('Number of Neighbors')
            plt.ylabel('Score')

    def heatmap(corr, square=True, cmap='RdYlGn'):
        sns.heatmap(corr, square=True, cmap='RdYlGn')

    def plot_scatter(self, X, y, xlabel=None, ylabel=None, color=None):
        plt.scatter(X, y, color=color)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    def plot_image(self, data):
        image = data.reshape(28, 28)
        plt.imshow(image, cmap=cm.binary,
                   interpolation="nearest")
        plt.axis("off")

    def plot_images(self, instances, images_per_row=10, **options):
        size = 28
        images_per_row = min(len(instances), images_per_row)
        images = [instance.reshape(size, size) for instance in instances]
        n_rows = (len(instances) - 1) // images_per_row + 1
        row_images = []
        n_empty = n_rows * images_per_row - len(instances)
        images.append(np.zeros((size, size * n_empty)))
        for row in range(n_rows):
            rimages = images[row * images_per_row: (row + 1) * images_per_row]
            row_images.append(np.concatenate(rimages, axis=1))
        image = np.concatenate(row_images, axis=0)
        plt.imshow(image, cmap=cm.binary, **options)
        plt.axis("off")

    def plot_facetgrid(self, df):
        FacetGrid = sns.FacetGrid(df, row='Embarked', size=4.5, aspect=1.6)
        FacetGrid.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette=None, order=None, hue_order=None)
        FacetGrid.add_legend()

    def plot_histogram(self, df):
        survived = 'survived'
        not_survived = 'not survived'
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
        women = df[df['Sex'] == 'female']
        men = df[df['Sex'] == 'male']
        ax = sns.distplot(women[women['Survived'] == 1].Age.dropna(), bins=18, label=survived, ax=axes[0], kde=False)
        ax = sns.distplot(women[women['Survived'] == 0].Age.dropna(), bins=40, label=not_survived, ax=axes[0],
                          kde=False)
        ax.legend()
        ax.set_title('Female')
        ax = sns.distplot(men[men['Survived'] == 1].Age.dropna(), bins=18, label=survived, ax=axes[1], kde=False)
        ax = sns.distplot(men[men['Survived'] == 0].Age.dropna(), bins=40, label=not_survived, ax=axes[1], kde=False)
        ax.legend()
        _ = ax.set_title('Male')

    def plot_precision_and_recall(precision, recall, threshold):
        plt.plot(threshold, precision[:-1], "r-", label="precision", linewidth=5)
        plt.plot(threshold, recall[:-1], "b", label="recall", linewidth=5)
        plt.xlabel("threshold", fontsize=19)
        plt.legend(loc="upper right", fontsize=19)
        plt.ylim([0, 1])

    def plot_precision_vs_recall(precision, recall):
        plt.plot(recall, precision, "g--", linewidth=2.5)
        plt.ylabel("recall", fontsize=19)
        plt.xlabel("precision", fontsize=19)
        plt.axis([0, 1.5, 0, 1.5])

    def plot_roc_curve(self, false_positive_rate, true_positive_rate, auc = None, label=None):
        if auc:
            if label:
                label = f'{label} AUC = %0.2f' % auc
            else:
                label = 'AUC = %0.2f' % auc
        plt.plot(false_positive_rate, true_positive_rate, linewidth=2, label=label)
        plt.plot([0, 1], [0, 1], 'r', linewidth=4)
        plt.axis([0, 1, 0, 1])
        plt.xlabel('False Positive Rate (FPR)', fontsize=16)
        plt.ylabel('True Positive Rate (TPR)', fontsize=16)
        plt.legend(loc='lower right')
        '''
        plt.title('ROC Curve')
        plt.plot(fpr, tpr, 'b',
                 label='AUC = %0.2f' % roc_auc)
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], 'r--')
        #plt.xlim([0, 1])
        #plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.show()
        '''


    def make_meshgrid(self, x, y, h=.02):
        """Create a mesh of points to plot in

        Parameters
        ----------
        x: data to base x-axis meshgrid on
        y: data to base y-axis meshgrid on
        h: stepsize for meshgrid, optional

        Returns
        -------
        xx, yy : ndarray
        """
        x_min, x_max = x.min() - 1, x.max() + 1
        y_min, y_max = y.min() - 1, y.max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        return xx, yy

    def plot_contours(self, ax, clf, xx, yy, **params):
        """Plot the decision boundaries for a classifier.

        Parameters
        ----------
        ax: matplotlib axes object
        clf: a classifier
        xx: meshgrid ndarray
        yy: meshgrid ndarray
        params: dictionary of params to pass to contourf, optional
        """
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.values.reshape(xx.shape)
        out = ax.contourf(xx, yy, Z, **params)
        return out

    def plot_contour(self, context):
        """
        Draws a contour plot with the classifier's decision boundaries
        :param context: An RMLContext object with a trained model.
        :return:
        """
        import matplotlib.pyplot as plt
        X0 = context.model.data_container.X_test[:, 0]
        X1 = context.model.data_container.X_test[:, 1]
        xx, yy = self.make_meshgrid(X0, X1)
        y = context.model.data_container.y_test
        fig, ax = plt.subplots(1,1)
        self.plot_contours(ax, context, xx, yy,cmap=plt.cm.coolwarm, alpha=0.8)
        ax.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xlabel(context.model.data_container.X_columns[0])
        ax.set_ylabel(context.model.data_container.X_columns[1])
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_title(f'{context.model.data_container.config.dataset_name} {context.model.model_config.name}')


    def plot(self, X, y, color = 'blue', linewidth=2):
        plt.plot(X, y, color=color, linewidth=linewidth)

    def clear(self):
        plt.clf()

class MetricsVisualizer(Visualizer):
    def __init__(self):
        self.Style = 'ggplot'

    def build_series(self, epochs, data, style, label):
        series_data = SeriesData()
        series_data.x_data = epochs
        series_data.y_data = data
        series_data.series_style = style
        series_data.series_label = label
        return series_data

    def plot_histories(self, histories, figures):
        for history in histories:
            self.plot_metrics(history, figures)

    def plot_metrics(self, metrics, figures):
        history = metrics.History.history
        # change to metrics['loss']
        for layout in figures:
            plt.figure(layout[0])
            for i, series_name in enumerate(layout[1]):
                series_data = history[series_name]
                epochs = range(1, len(series_data) + 1)
                series = self.build_series(epochs, series_data, metrics.SeriesStyles[i], f'{metrics.Name} {series_name}')
                self.add_series(series)

        plt.title('Training & Validation Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()


    def add_series(self, series_data):
        plt.plot(series_data.x_data, series_data.y_data, series_data.series_style, label=series_data.series_label)

    def show_plot(self, x, y, xlabel, ylabel, legend=False):
        plt.plot(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if (legend == True):
            plt.legend()
        plt.show()
