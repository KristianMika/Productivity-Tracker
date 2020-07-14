from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np


class Grapher:
    """ The grapher class takes care of plotting charts"""

    def plot_time_dist(self, data, name, time_from, time_to, date):
        """
        Creates a pie plot with labels and a description

        :param data: a map of activities
        :param name: the name of this chart
        :param time_from: time of the first activity as a string
        :param time_to: time of the last activity as a string
        :param date: the date of the activities
        """
        labels = []
        sizes = []

        # Transforms data dictionary into two arrays - labels and sizes
        for key in data.keys():
            val = data[key]
            # label = name of an app (window) and the duration of the activity
            label = key + '\n({})'.format(str(timedelta(seconds=val)))
            labels.append(label)
            sizes.append(val)

        # Creates gaps in the plot
        explode = [0.1 for _ in range(len(labels))]

        fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"), figsize=(20, 10))
        wedges, _, autotexts = ax.pie(sizes, explode=explode, autopct='%1.1f%%', shadow=True, startangle=50,
                                      wedgeprops=dict(width=1))

        # Sets the label size and thickness
        plt.setp(autotexts, size=10, weight="bold")

        ax.set_title(name, fontweight='bold', size=15)

        # Inserts the "info" frame with information about this activity set
        ax.text(1, -1.3, 'Date:  ' + date +
                '\nFrom: ' + time_from +
                '\nTo:      ' + time_to, size=14)

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")

        self.__pie_chart_create_labels(wedges, kw, ax, labels)

        plt.show()
        plt.savefig('./plot.png')

    @staticmethod
    def __pie_chart_create_labels(wedges, kw, ax, labels):
        """
        Creates labels for a pie chart

        A piece of an example code from the matplotlib documentation
        Source: (https://matplotlib.org/3.1.0/gallery/pie_and_polar_charts/pie_and_donut_labels.html)
        """
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(labels[i], xy=(x, y), xytext=(1.35 * np.sign(x), 1.4 * y),
                        horizontalalignment=horizontalalignment, **kw)
