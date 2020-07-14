import sys
import time


class Activity:
    """
    The Activity class represents a single activity,
    that is defined by a name, window name and a start time
    """
    MAX_NAME_LEN = 25

    def __init__(self, application, window_name, start_time, duration):
        # TODO: Remove the local import bellow
        from Analyzer.analyzer import TIME_DIFFERENCE

        self.app_name = application
        self.window_name = self.__tweak_window_name__(window_name)
        self.app_name = self.__tweak_app_name__(application)
        self.start_time = start_time + TIME_DIFFERENCE
        self.duration = duration

    def __str__(self):
        return "{}: {} - from {}, lasted {}".format(self.app_name,
                                                    self.window_name,
                                                    self.start_time_str(),
                                                    self.duration)

    def start_time_str(self):
        """Returns the start time of this activity in format HH:MM:SS as a string"""
        t = time.gmtime(self.start_time)
        return "{:02d}:{:02d}:{:02d}".format(t.tm_hour, t.tm_min, t.tm_sec)

    @staticmethod
    def __tweak_window_name__(win_name):
        """
        TODO: remove trailing app names from window names, e.g. 'New Tab - Chromium' to 'New Tab'
        :param win_name: the window name
        :return: the modified window name
        """
        return win_name[:Activity.MAX_NAME_LEN]

    @staticmethod
    def __tweak_app_name__(app_name):
        """
        Modifies the name of an application.

        :param app_name: the application name
        :return: the modified application name
        """
        # TODO: some apps tend to put lots of information into the app name, cut the useless data off
        app_name = app_name[:20]

        # TODO: Remove the local import bellow
        from Analyzer.analyzer import SUBS_DICT

        # Substitutes the app name with a custom name, e.g. 'jetbrains-pycharm-ce' -> 'Pycharm'
        if app_name in SUBS_DICT:
            app_name = SUBS_DICT[app_name]

        app_name = app_name.title()

        return app_name


class Activities:
    """
    The Activities class represents a list of activities
    """

    def __init__(self, logs):
        """
        Parses and fills the activities list
        :param logs: a list of activity logs
        """
        self.act_list = []

        for i in range(len(logs)):
            activity = logs[i]

            if len(activity) != 3:
                sys.stderr.write('Invalid log format: {}\n'.format(activity))
                continue

            beg_time = int(activity[0])
            window_name = activity[1]
            application = activity[2]
            duration = 0

            # Gets the start time of the next activity and computes it's duration
            if i < len(logs) - 1:
                duration = int(logs[i + 1][0]) - beg_time

            self.act_list.append(Activity(application, window_name, beg_time, duration))

    def __getitem__(self, index):
        return self.act_list[index]

    def remove_short(self, s):
        """
        Removes activities that lasted less than :param s: seconds.

        :param s: a number of seconds
        :return: None
        """
        self.act_list = list(filter(lambda x: x.duration >= s, self.act_list))

    def size(self):
        return len(self.act_list)
