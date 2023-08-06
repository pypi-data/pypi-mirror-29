import csv
# import sys
import glob
import os


class Parameters:

    """Standardized to hold all parameters in milliseconds:
    false_licks, pause_criterion are provided in milliseconds by user
    meal_criterion, session_duration, and bins are provided in seconds by user"""
    def __init__(self, folder, false_licks, pause_criterion, meal_criterion, session_duration, bins, on_column,
                 off_column):
        self.false_licks = float(false_licks)                   # Threshold for false licks
        self.pause_criterion = float(pause_criterion)           # Threshold for a burst
        self.meal_criterion = float(meal_criterion) * 1000      # Threshold for a meal
        self.session_duration = int(session_duration) * 1000    # Length of the session
        self.bins = int(bins) * 1000                            # Length of a bin
        self.on_column = on_column.strip()                      # The column name for the column of "on" values
        self.off_column = off_column.strip()                    # The column name for the column of "off" values

        if not os.path.exists(folder):
            raise OSError("Error: Folder {} not found".format(folder))

        self.files = []
        for filename in glob.glob(os.path.join(folder, '*.csv')):
            self.files.append(filename)

    def __str__(self):
        return "False Licks (ms)      : {false_licks}\n" \
               "Pause Criterion (ms)  : {pause_criterion}\n" \
               "Meal Criterion (ms)   : {meal_criterion}\n" \
               "Session Duration (ms) : {session_duration}\n" \
               "Number of bins        : {bins}\n" \
               "On Column             : {on_column}\n" \
               "Off Column            : {off_column}\n" \
               "Folder with files     : {files}\n" \
                .format(files=self.files, false_licks=self.false_licks, pause_criterion=self.pause_criterion,
                        meal_criterion=self.meal_criterion, session_duration=self.session_duration,
                        bins=self.bins, on_column=self.on_column, off_column=self.off_column)


def extract_params():
    """Get a parameter object containing all necessary user input"""
    filename = "param_file.csv"
    # if len(sys.argv) >= 2:
    #     filename = sys.argv[1]

    try:
        with open(filename) as csvDataFile:
            csv_reader = csv.reader(csvDataFile)
            csv_reader.next()
            p = csv_reader.next()
            return Parameters(*p)

    except IOError:
        print "Error: Parameter file {} does not appear to exist.".format(filename)
        exit()
    except ValueError:
        print "Error: One or more of your parameter values is of an incorrect type. \n" \
              "It is likely that it is one of the criteria \nthat are meant to be seconds, milliseconds, or an integer"
        exit()
    except OSError as e:
        print e
        exit()


# print extract_params()
