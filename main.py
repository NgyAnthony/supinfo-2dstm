import os
import webbrowser
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas import option_context
from numpy import count_nonzero

# Read the dataset into a data table using Pandas

df = pd.read_csv("data/weather_madrid.csv")

# Webbrowser
def create_df_view():
    # Create a web page view of the data for easy viewing
    html = df[0:100].to_html()

    # Save the html to a temporary file
    with open("data/weather_madrid.html", "w") as f:
        f.write(html)

def show_df_view():
    # Open the web page in our web browser
    full_filename = os.path.abspath("data/weather_madrid.html")
    webbrowser.open("file://{}".format(full_filename))

# Explore
def get_df_head_numerical():
    head_numerical = df.select_dtypes('number').columns
    print("\n--- SHOWING NUMERICAL COLUMNS ---")
    for head in head_numerical:
        print(head)

def get_df_head_category():
    head_category = df.select_dtypes('object').columns
    print("\n--- SHOWING CATEGORY COLUMNS ---")
    for head in head_category:
        print(head)

def get_df_list_date():
    date_list = df['CET']
    print("\n--- SHOWING DATES ---")
    print(date_list)

def get_df_null_values():
    print("\n--- NULL VALUES IN DF ---")
    null_in_df = df.isnull().values.any()
    if null_in_df:
        print("Valeur nulle dans le dataframe.")
    else:
        print("Pas de valeur nulle dans le dataframe.")
    return null_in_df

class Analyzer:
    def __init__(self, raw_df):
        self.df: pd.DataFrame = raw_df

    def select_df_attributes(self):
        self.df = self.df[["CET", "Mean TemperatureC", "Min TemperatureC", "Max TemperatureC", "Mean Humidity", "Max Humidity", "Min Humidity", "MeanDew PointC", "Min DewpointC", "Dew PointC", "CloudCover", "Events"]]

    def rename_df_columns(self):
        self.df.columns = ["date", "MeanTemp", "MinTemp", "MaxTemp", "MeanHum", "MaxHum", "MinHum", "MeanDew", "MinDew", "Dew", "CloudCover", "Events"]

    def describe_df(self):
        # Showing all columns to check everything
        with option_context('display.max_rows', 100, 'display.max_columns', 10):
            print("\n--- DESCRIBING COLUMNS ---")
            # Max temperature shows 80°C, max recorded in madrid is 42.2°C
            print(self.df.describe())

    def show_incorrect_numerical(self, column_name, incorrect_limit):
        print("\n--- SHOW INCORRECT " + column_name + " DATA ---")
        # Show "column_name" element higher than "incorrect_limit"
        print(self.df[self.df[column_name] > incorrect_limit])

    def draw_boxplot(self, column_name):
        # Init figure
        sns.set_theme(style="whitegrid")
        bp = sns.boxplot(x=self.df[column_name])
        fig = bp.get_figure()
        fig.savefig("data/graphs/" + column_name + "_boxplot.png")

    def flush_incorrect_numerical(self, column_name, flush_limit):
        # Getting a warning even though I'm using .loc, welp.
        self.df.loc[self.df[column_name] > flush_limit, column_name] = None

    def count_rows_with_nan(self):
        count = count_nonzero(self.df.isnull().values)
        print("--- SHOW COUNT OF ROWS WITH NAN ---")
        print(count)

    def remove_rows_with_nan(self):
        temp = self.df.dropna()
        print("--- SHOW ROWS COUNT AFTER DROPNA ---")
        print(temp.count())

    def count_nan_in_col(self, column_name):
        count_nan = len(self.df[column_name]) - self.df[column_name].count()
        print("--- SHOW COUNT OF NAN IN " + column_name + " ---")
        print(count_nan)

    def replace_nan_by_value_in_col(self, column_name, value):
        # This spits out a .loc error but it works.
        # Couldn't make it work with a .loc, needs to be fixed
        print("--- REPLACING NAN IN " + column_name + " BY " + value + " ---")
        self.df[column_name] = self.df[column_name].fillna(value)


def start_analysis():
    analyzer = Analyzer(df)
    # Question 4.1
    analyzer.select_df_attributes()
    # Question 4.2
    analyzer.rename_df_columns()
    # Question 4.3
    analyzer.describe_df()
    # Question 4.4
    analyzer.show_incorrect_numerical("MaxTemp", 42.2)
    # Question 4.5
    analyzer.draw_boxplot("MaxTemp")
    # Question 5.1
    analyzer.flush_incorrect_numerical("MaxTemp", 42.2)
    # Question 5.2
    analyzer.count_rows_with_nan()
    # Question 5.3
    analyzer.remove_rows_with_nan()
    # Question 5.5
    analyzer.count_nan_in_col("Events")
    # Question 5.6
    analyzer.replace_nan_by_value_in_col("Events", "NoEvent")
    # Need to choose a strategy to fill missing data on Dew/Temp/CloudCover
    # Question 6.1


if __name__ == '__main__':
    # Question 2.1
    # create_df_view()
    # Question 2.2
    # show_df_view()
    # Question 3.1
    # get_df_head_numerical()
    # Question 3.2
    # get_df_head_category()
    # Question 3.3
    # get_df_list_date()
    # Question 3.4
    # get_df_null_values()
    start_analysis()
