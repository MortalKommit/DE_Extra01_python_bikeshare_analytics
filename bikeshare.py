import time
import calendar
import warnings
from pprint import pprint
import pandas as pd
import numpy as np
import plotext as plt

# Mute plotext warnings - numpy warning of None comparison being shown
warnings.filterwarnings("ignore", module='plotext')

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# Populate month and day names, with the first element being "all"
month_names, day_names = list(map(lambda month: month.lower(
), calendar.month_name)), list(map(lambda day: day.lower(), calendar.day_name))
month_names[0] = "all"
day_names = ["all"] + day_names


def get_filters() -> tuple:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        Tuple of (city, month, day)
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city, month, day = None, None, None

    # get user input for city (chicago, new york city, washington).
    while city is None or city not in CITY_DATA.keys():
        city = input(
            "Enter city name to filter by (chicago/new york city/washington):")
        city = city.lower()
        if not city or city not in CITY_DATA.keys():
            print("Enter a valid city name as input ({}).".format(
                ", ".join(CITY_DATA.keys())))

    # get user input for month (all, january, february, ... , june)
    while month is None or month not in month_names:
        month = input("Enter month name to filter by (all for no filter): ")
        month = month.lower()
        if not month or month not in month_names:
            print("Enter a valid month name as input ({}).".format(
                ", ".join(month_names)))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day is None or day not in day_names:
        day = input("Enter a day to filter by (all for no filter): ")
        day = day.lower()
        if not day or day not in day_names:
            print("Enter a valid day as input ({}).".format(", ".join(day_names)))

    print('-'*40)
    return city, month, day


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    city_file = CITY_DATA[city]
    df = pd.read_csv(city_file)
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].apply(lambda x: x.strftime("%I %p"))

    df.rename(columns={list(df)[0]: 'ride_id'}, inplace=True)
    month_filter = month_names.index(month)

    if month != 'all':
        month_filter = month_names.index(month)
        df = df[df['month'] == month_filter]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df: pd.DataFrame):
    """
    Displays statistics on the most frequent times of travel.

    [Args]
        df - pandas DataFrame created from filtered csv data.
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month - Add 1 to index since month_names[0] is all
    print("The most common rental month: {}".format(
        month_names[df['month'].mode()[0]]))

    prompt_start_time = time.time()
    graph_prompt = input(
        "Generate graph of rentals by month? (y[es]/s[ave]/n[o]): ")
    prompt_end_time = time.time()
    if graph_prompt.lower() in ['y', 'yes', 's', 'save']:

        month_index = set(df['month'].values)

        months = [month_names[i].title() for i in month_index]

        create_data_graph(df, ['month'], ['month'], graph_title="Rides by month",
                          graph_type='bar', xticks=month_index, xtick_labels=months, yticks=None,
                          xlabel='Month', ylabel='Rides Booked', saveplot=graph_prompt.lower())
        prompt_start_time += time.time()
        input("\nPress any key to continue...")
        prompt_end_time += time.time()

    # display the most common day of week
    print("The most common rental day of the week: {}".format(
        df['day_of_week'].mode()[0]))

    prompt_start_time += time.time()
    graph_prompt = input(
        "Generate graph of rentals by day of week? (y[es]/s[ave]/n[o]): ")
    prompt_end_time += time.time()
    if graph_prompt.lower() in ['y', 'yes', 's', 'save']:
        days = set(df['day_of_week'].values)

        create_data_graph(df, ['day_of_week'], ['day_of_week'], graph_title="Rides by Day of Week",
                          graph_type='bar', xticks=None, xtick_labels=None, yticks=None, ytick_labels=None,
                          xlabel='Day', ylabel='Rides Booked', color_theme='pro', saveplot=graph_prompt.lower())
        prompt_start_time += time.time()
        input("\nPress any key to continue...")
        prompt_end_time += time.time()

    # display the most common start hour
    mode_start_hour = df['hour'].mode()[0]

    print("The most common rental start hour: {}".format(mode_start_hour))

    prompt_start_time += time.time()
    graph_prompt = input(
        "Generate graph of rentals by hour [warning - messy]? (y[es]/s[ave]/n[o]): ")
    prompt_end_time += time.time()
    if graph_prompt in ['y', 'yes', 's', 'save']:

        create_data_graph(df, ['hour'], ['hour'], graph_title="Rides by Hour",
                          graph_type='bar', xticks=None, xtick_labels=None, yticks=None, ytick_labels=None,
                          xlabel='Rides Booked', ylabel='Hour', color_theme='matrix', horizontal=True, 
                          saveplot=graph_prompt)
        prompt_start_time += time.time()
        input("\nPress any key to continue...")
        prompt_end_time += time.time()

    print("\nThis took %s seconds." %
          (time.time() - start_time - (prompt_end_time - prompt_start_time)))
    print('-'*40)


def station_stats(df: pd.DataFrame):
    """
    Displays statistics on the most popular stations and trip.

    [Args]
        df - pandas DataFrame created from filtered csv data.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most common start station
    print("\n The most common start station:{}".format(
        df["Start Station"].mode()[0]))

    # display    most common end station
    print("\n The most common end station:{}".format(
        df["End Station"].mode()[0]))

    # display most frequent combination of start station and end station trip
    print("\n The most common start-end station combinations:{}".format(
        (df["Start Station"] + "-" + df["End Station"]).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df: pd.DataFrame):
    """
    Displays statistics on the total and average trip duration.

    [Args]
        df - pandas DataFrame created from filtered csv data. 
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time it took for all of these trips is:", end=' ')
    print("{} seconds".format(df['Trip Duration'].sum()))

    # display mean travel time
    print("The mean travel time for a trip is {} seconds.".format(
        df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df: pd.DataFrame, city: str):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The users grouped by subscription are:")
    print(df['User Type'].value_counts().to_string())
    if city == 'washington':
        print(
            "\nWashington bike share data doesn't have the Gender and Birth Year columns!")
    else:
        print("\nThe users grouped by gender are:")
        # Display counts of gender
        print(df['Gender'].value_counts().to_string())

        # Display earliest, most recent, and most common year of birth

        print("\nThe earliest birth year of a user is: {:.0f}".format(
            df['Birth Year'].dropna().sort_values(ascending=True).head(1).item()))
        print("The most recent birth year of a user is: {:.0f}".format(
            df['Birth Year'].dropna().sort_values(ascending=False).head(1).item()))
        print("The most common birth year of a user is: {:.0f}".format(
            df['Birth Year'].mode()[0]))

    # Display the average trip time, by subscription type
    print("\nThe average trip duration (HH:MM:SS), by customer type is:")
    print(pd.to_timedelta(df.groupby(["User Type"])[
          "Trip Duration"].mean().round(), unit='s').to_string())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def create_data_graph(df: pd.DataFrame, select_columns: list, grouping_columns: str = None, stat: list = ["count"],
                      graph_title: str = None, graph_type=None, xticks: list = None, xtick_labels: list = None,
                      yticks: list = None, ytick_labels: list = None, xlabel=None, ylabel=None, color_theme='default',
                      horizontal=False, saveplot='n'):
    """
    Generates graph from a dataframe, grouping by the relevant columns, and with 
    the provided title, xticks, ticks, xlabel, ylabel 

    [Args]
        df: pandas DataFrame to select values from
        select_columns: list of str, columns to plot
        grouping_columns:  str, columns to groupBy
        stat: str statistic to compute from grouped columns, default count
        graph_title: str, Title of the generated graph
        xticks: list, List of tick values for x-axis
        yticks: list, List of tick values for y-axis
        xlabel: str, label for x-axis
        ylabel: str, label for y-axis
    """

    selected_columns = ",".join(select_columns)
    grouped_df = df.groupby(grouping_columns)[selected_columns].agg(stat)

    # Set graph theme color
    plt.theme(color_theme)
    # Assume most graphs start from 0

    min_range = 0
    max_range = max(grouped_df.loc[:, ','.join(stat)])
    if yticks is None:
        yticks = np.linspace(min_range, max_range, num=len(
            grouped_df.loc[:, ','.join(stat)].values)).astype(int)

    plt.yticks(yticks, ytick_labels)
    if xticks is not None:
        plt.xticks(xticks, xtick_labels)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(graph_title)
    if not horizontal:
        plt.bar(grouped_df.index.values.tolist(),
                grouped_df.loc[:, ','.join(stat)].values)
    else:
        plt.bar(grouped_df.index.values.tolist(), grouped_df.loc[:, ','.join(stat)].values,
                orientation='h', width=0.3, marker='fhd')

    plt.show()
    if saveplot[0] == 's':
        plt.savefig("./{}.html".format(graph_title))
    plt.clear_color()
    plt.clf()


def display_raw_data(df: pd.DataFrame, start_pos: int, batch_size: int = 5):
    """
    Displays raw data in batches of 5
    [Args]
        df - Dataframe containing city data filtered by month, day
    """

    json_data = df.iloc[start_pos:start_pos +
                        batch_size, :].to_dict(orient='records')
    pprint(json_data)


def main():
    while True:
        city, month, day = get_filters()
        start_pos = 0
        df = load_data(city, month, day)

        # Calculate stats by passing dataframe to each function call
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data_prompt = input(
            "Would you like to view the raw data (yes/no)? ")

        while raw_data_prompt == "yes":
            if raw_data_prompt == "yes":
                display_raw_data(df, start_pos)
                raw_data_prompt = input("Continue (yes/no)? ")
                if raw_data_prompt == "yes":
                    start_pos += 5
                    continue
                break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
