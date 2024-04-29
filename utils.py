import matplotlib.pyplot as plt

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