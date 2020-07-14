import sys

from Analyzer.activities import Activities
from Analyzer.grapher import Grapher

# GMT + 2
TIME_DIFFERENCE = 60 * 60 * 2
CURR_DATE_STR = ''
SUBS_DICT = {'jetbrains-pycharm-ce': 'Pycharm', 'Navigator': 'Firefox'}
LOG_DELIMITER = ';'
PLOT_DIR = '../'


def load_act_logs(log_file):
    """
    Loads activity logs from the :param log_file:
    :param log_file: name of the log file
    :return: a list of lists (parsed logs)
    """
    with open(log_file, 'r') as file:
        return [x.split(LOG_DELIMITER) for x in file.read().splitlines()]


class ActivityStats:
    """
    The ActivityStats class represents a statistics about a specific list of activities
    """

    def __init__(self, activities):
        self.activities = activities
        self.from_time = activities[0].start_time_str()
        self.to_time = activities[-1].start_time_str()

        self.__make_time_dist_map__()
        self.grapher = Grapher()

    def app_dist(self, app, min_percentage=1):
        """
        Plots the time distribution of :param app:

        :param app: Name of the app
        :param min_percentage: records that make up less than :param min_percentage:
            per cents will be filtered out
        :return: None
        """

        windows = list(filter(lambda x: x.app_name == app, self.activities))

        app_map = {}

        for act in windows:
            if not act.window_name in app_map:
                app_map[act.window_name] = 0
            app_map[act.window_name] += act.duration

        app_map = self.__filter_short_activities__(app_map, min_percentage)
        self.grapher.plot_time_dist(app_map,
                                    'Time spent in ' + app, self.from_time, self.to_time, CURR_DATE_STR)

    def overall_dist(self, min_percentage=1):
        """
        Plots the overall time distribution
        :return: None
        """
        dist_map = self.__filter_short_activities__(self.time_dist_map, min_percentage)
        self.grapher.plot_time_dist(dist_map,
                                    'The overall time distribution', self.from_time, self.to_time, CURR_DATE_STR)

    @staticmethod
    def __filter_short_activities__(app_map, min_percentage=1):
        """
        Removes activities that make up less than :param min_percentage: per cents.

        :param app_map: maps with activities and times
        :param min_percentage: the bound in percents
        :return: a filtered map
        """

        time_thresh = sum(app_map.values()) / 100 * min_percentage
        app_map_filtered = {}
        for key in app_map.keys():
            if app_map[key] >= time_thresh:
                app_map_filtered[key] = app_map[key]

        return app_map_filtered

    def __make_time_dist_map__(self):
        """
        Creates a map of {<app> name : the total time spent in <app>}

        :return: None
        """
        self.time_dist_map = {}
        for activity in self.activities:
            if not activity.app_name in self.time_dist_map:
                self.time_dist_map[activity.app_name] = 0

            self.time_dist_map[activity.app_name] += activity.duration


if __name__ == '__main__':
    """
    Brief demo that loads a file with activity logs and plots
    the overall time distribution and the time distribution spent in Chromium
    """

    if len(sys.argv) != 2:
        print('Incorrect use!\nUse: "analyze [file]"')
        exit(1)

    file_name = sys.argv[1].split('/')[-1]
    CURR_DATE_STR = file_name[:file_name.index('.')]

    samples = load_act_logs(sys.argv[1])

    activities = Activities(samples)

    stats = ActivityStats(activities)

    stats.overall_dist()

    stats.app_dist("Chromium", 5)
