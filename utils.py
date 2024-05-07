import matplotlib.pyplot as plt
import pandas as pd
import os
import re
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import geopandas as gpd

# Data process tools
def get_all_file_paths(directory):
    """Get all file paths in a directory.
    :param directory: The directory to search for files."""
    all_files = os.listdir(directory)
    all_csv_files = [file for file in all_files if file.endswith(".csv")]
    all_csv_file_paths = [os.path.join(directory, file) for file in all_csv_files]
    return all_csv_file_paths

def check_columns(file_path, required_columns):
    """Check if a file contains the required columns.
    :param file_path: The file path to check.
    :param required_columns: A list of required columns."""
    df = pd.read_csv(file_path, nrows=1)
    df.columns = [column.lower().replace("_", " ") for column in df.columns]
    required_columns = [column.lower().replace("_", " ") for column in required_columns]
    if set(required_columns).issubset(df.columns):
        return file_path
    
def get_perm_data_path(file_paths, required_columns):
    """Get the file paths that contain the required columns.
    :param file_paths: A list of file paths to check.
    :param required_columns: A list of required columns."""
    qualified_files = []
    for file in file_paths:
        qualified_file = check_columns(file, required_columns)
        if qualified_file:
            qualified_files.extend(qualified_file) # To avoid nested list
    print(sorted(qualified_files))
    return sorted(qualified_files)

def read_perm_data(qualified_files, required_columns, new_columns = {}):
    """Read the PERM data from the qualified files.
    :param qualified_files: A list of qualified file paths.
    :param required_columns: A list of required columns.
    :param new_columns: A dictionary of new column names."""
    df_perm = pd.DataFrame()
    for file in qualified_files:
        try:
            df = pd.read_csv(file)
            df.columns = [column.lower().replace("_", " ") for column in df.columns] # Convert actual columns to lower case
            required_columns = [column.lower().replace("_", " ") for column in required_columns]  # Convert required columns to lower case
            df = df[required_columns]
            df["Year"] = file.split("_")[-1].split(".")[0]  # Extract the year from the file name
            if new_columns:
                df = df.rename(columns= new_columns)
            df_perm = pd.concat([df_perm, df], axis=0)
        except ValueError:
            # Handle the exception
            print(f"ValueError occurred while processing file: {file}")
    return df_perm

# Data visualization tools
def plot_immigration_over_time(data, regions, mutiple=True):
    """ Plot the immigration number over time for the given regions.
    :param data: The data frame of immigration numbers.
    :param regions: The list of regions to plot.
    :param mutiple: A boolean flag to indicate whether to plot multiple regions. Default is True."""

    plt.figure(figsize=(12, 8))
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
    """ Plot the number of immigrants for the given regions.
    :param data: The data of immigration numbers.
    :param regions: The list of regions to plot."""
    df = data.loc[regions].drop('Total').sort_values()

    # Create a bar chart
    plt.figure(figsize=(6, 10))
    plt.barh(df.index, df)

    plt.title(f"States that receive immigrants from {regions} (2013-2022)")
    plt.xlabel('Number of Immigrants')
    plt.ylabel('States')

def plot_percentage_pie(data, regions, type):
    """ Plot the percentage of the given green card type for the given regions.
    :param data: The data frame of the green card types.
    :param regions: The list of regions to plot.
    :param type: The type of green card.
    """
    df = data[type]
    df = df.loc[regions]

    plt.figure(figsize=(10, 6))
    plt.pie(df, labels=df.index, autopct='%1.1f%%')
    plt.title(type)

    plt.show()

def plot_stacked_bar(df, title, xlabel, ylabel):
    """ Plot a stacked bar plot for the given data frame.
    :param df: The data frame to plot.
    :param title: The title of the figure.
    :param xlabel: The label for the x-axis.
    :param ylabel: The label for the y-axis.
    """
    # Set the figure size
    plt.figure(figsize=(10, 6))

    # Create a cross table
    cross_tab = pd.crosstab(index=df[xlabel], columns=df[ylabel])

    # Calculate the percentage for each group in each year
    percentage_tab = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100

    # Create a stacked bar plot for the percentages
    ax = percentage_tab.plot(kind='bar', stacked=True)

    # Add percentages on the figure
    for i, (idx, row) in enumerate(percentage_tab.iterrows()):
        for j, item in enumerate(row):
            if item > 0:
                ax.text(i, row.iloc[:j+1].sum() - item / 2, f'{item:.1f}%', ha='center', va='center')

    # Set the title and labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Move the legend outside of the plot
    ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

    # Show the figure
    plt.show()

def vectorize_TFIDF_cluster(data, n_clusters=16):
    """Vectorize the text data using TF-IDF and cluster the data using KMeans.
    :param data: The text data to vectorize.
    :param n_clusters: The number of clusters to use in KMeans. Default is 16."""
    # TF-IDF
    # it assigns a weight to each word that signifies the word's importance in the text. 
    # Words that are common across all documents have lower weights, while words that are rare have higher weights.
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data)
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    labels = kmeans.labels_
    return labels

def plot_map(df, region):
    """ Plot the map of the US with the color representing the number
    :param df: The data frame of the number
    :param region: The region to plot."""
    df_receiving_states = df.set_index('Region and country of birth')

    us_states = gpd.read_file('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json')

    # convert df to geodf
    us_states = us_states.set_index('name')
    df_receiving_states = df_receiving_states.transpose()
    us_states = us_states.join(df_receiving_states)

    # plot the map
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    us_states.plot(column=region, ax=ax, legend=True, missing_kwds={"color": "lightgrey"}, legend_kwds={'shrink': 0.5})

    # put names on the map
    us_states['center'] = us_states['geometry'].centroid
    us_states_points = us_states.copy()
    us_states_points.set_geometry('center', inplace = True)

    for x, y, label in zip(us_states_points.geometry.x, us_states_points.geometry.y, us_states_points.index):
        ax.text(x, y, label, fontsize=7)

    plt.title(f"Immigrants from {region} in the US by State (2013-2022)")

    plt.show()

def receiving_states_job_title(df, state_short, state, regions, title):
    """ Plot the top 10 job titles for the given birth place in the given state.
    :param df: The data frame of the job titles.
    :param state_short: The short name of the state.
    :param state: The full name of the state.
    :param regions: The list of regions to plot.
    :param title: The title of the plot."""
    df[((df["worksite state"] == state_short) | (df["worksite state"] == state)) & (df["birth country"].isin(regions))].groupby("job title").size().sort_values(ascending=False).head(10).plot(kind="barh", title=f"Top 10 Job Titles for {title} Immigrants in {state}")
    plt.show()