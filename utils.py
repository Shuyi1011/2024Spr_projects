import matplotlib.pyplot as plt
import pandas as pd
import os

# Data process tools
def get_all_file_paths(directory):
    all_files = os.listdir(directory)
    all_csv_files = [file for file in all_files if file.endswith(".csv")]
    all_csv_file_paths = [os.path.join(directory, file) for file in all_csv_files]
    return all_csv_file_paths

def check_columns(file_path, required_columns):
    df = pd.read_csv(file_path, nrows=1)
    if set(required_columns).issubset(df.columns):
        return file_path

# Data visualization tools
def plot_immigration_over_time(data, regions, mutiple=True):

    plt.figure(figsize=(10, 6))
    if mutiple:
        for region in regions:
            plt.plot(data.columns.astype(str), data.loc[region], label=region)
    else:
        plt.plot(data.columns.astype(str), data.loc[regions], label=regions)

    plt.title('Immigration Over Time')
    plt.xlabel('Time Period')
    plt.ylabel('Number of Immigrants')
    plt.legend()

    # Rotate x-labels
    plt.xticks(rotation=45)

    # Display the plot
    plt.show()


def plot_states_bar(data, regions):
    df = data.loc[regions].drop('Total').sort_values()

    # Create a bar chart
    plt.figure(figsize=(6, 10))
    plt.barh(df.index, df)

    plt.title(f"States that receive immigrants from {regions} (2013-2022)")
    plt.xlabel('Number of Immigrants')
    plt.ylabel('States')

def plot_percentage_pie(data, regions, type):
    df = data[type]
    df = df.loc[regions]

    # Create a pie chart
    plt.figure(figsize=(10, 6))
    plt.pie(df, labels=df.index, autopct='%1.1f%%')

    # Optionally, you can add a title
    plt.title(type)

    # Display the plot
    plt.show()