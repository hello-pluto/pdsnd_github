import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITIES = ['chicago', 'new york city', 'washington']

CITY_DATA = { CITIES[0]: 'chicago.csv',
              CITIES[1]: 'new_york_city.csv',
              CITIES[2]: 'washington.csv' }

MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']


def get_user_input(prompt, list_of_items):
    """
    Asks user to specify an item to analyze.

    Args:
        (str) prompt - type of item being filtered. i.e. city, month, day
        (list) list_of_items - list containing all possible options that can be filtered by
    Returns:
        (str) item - the user response containing the chosen option to filter by
    """

    item = ''
    options = ''
    for i, option in enumerate(list_of_items):
        if i:  
            # print a separator if this isn't the first element
            options += (', ')
        options += option.title()

    while item not in list_of_items:
        item =  input('\nWhich specific ' + prompt + ' would you like to view statistics on?\n' \
                'Your options are: ' + options + '.\n').lower()

        while item not in list_of_items:
            item = incorrect_input(options)

    return item


def incorrect_input(options):
    """
    Notifies user of incorrect input, and prompts for another response.

    Args:
        (list) options - list containing all possible options that can be filtered by
    Returns:
        (str) - the user response containing the chosen option to filter by
    """

    return input("\nOops. That's not one of the options.\n" \
            'Your options are: ' + options + '.\n')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello World! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = get_user_input('US city', CITIES)
    month = get_user_input('month', MONTHS)
    day = get_user_input('day', DAYS)
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int    
        month = MONTHS.index(month)

        # returns the dataframe where month is filtered by the entered month
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # returns the dataframe where day is filtered by the entered day
        df = df[df['day_of_week'] == day.title()]
    
    return df


def display_raw_data(df, num_rows):
    """
    Iterates through the the dataframe provided, and prints the data for the specified number of rows.

    Args:
        (frame) df - dataframe to iterate through
        (int) num_rows - number of rows to return the data for
    """

    i = 0
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break
        print(tabulate(df.iloc[np.arange(0+i,num_rows+i)], headers ="keys"))
        i+=5

    # for start_row in range(0, df.shape[0], num_rows):
    #     end_row = min(start_row + num_rows, df.shape[0])
    #     yield df.iloc[start_row:end_row, :].to_json(orient='index', indent=2)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating the most popular/frequent times of travel...\n")
    print("N.B. If you have specified a month or day, this will automatically be reflected as the most popular option!\n")
    
    # time of execution
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    popular_month_name = MONTHS[popular_month].title()
    print('\nMost popular month to travel: ', popular_month_name)

    # display the most common day of week
    df['day'] = df['Start Time'].dt.day_name()
    popular_day = df['day'].mode()[0]
    print('\nMost popular day to travel: ', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost popular time to travel: ', popular_hour)

    print("\nThis took %s seconds to compute." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost commonly used Start Station to travel from: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['Start Station'].mode()[0]
    print('\nMost commonly used End Station to arrive at: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_combination_station = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print("\nMost commonly used combination of stations: ", popular_combination_station)

    print("\nThis took %s seconds to compute." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()
    df['Duration Time'] = df['Trip Duration'].apply(pd.to_timedelta, unit='s')

    # display total travel time
    total_travel_duration = df['Duration Time'].sum()
    print("Total duration of travel: ", total_travel_duration)

    # display mean travel time
    mean_travel_duration = df['Duration Time'].mean()
    print("Average duration of travel: ", mean_travel_duration)

    print("\nThis took %s seconds to compute." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User statistics...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nType of bikeshare users and the total number of each:')
    print(user_types)

    if city != 'washington':
    # Display counts of gender
    
        gender_types = df['Gender'].value_counts()
        print('\nGender of bikeshare users and the total number of each:')
        print(gender_types)

        # Display earliest, most recent, and most common year of birth
        birth_year = df['Birth Year']
        # oldest user 
        earliest_year = int(birth_year.min())
        print('\nBirth year of eldest user:', earliest_year)
        # youngest user
        most_recent = int(birth_year.max())
        print('\nBirth year of youngest user:', earliest_year)
        # average user age
        most_common_year = int(birth_year.mode()[0])
        print('\nBirth year of most common users:', most_common_year)

    print("\nThis took %s seconds to compute." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df, 5)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
