import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    error = True
    city = input('Please enter the name of the city for which you would like to analyze the data: chicago, new york city or washington:\n').lower()
    while error == True:
        if city in CITY_DATA.keys():
            error = False
        else:
            print('That\'s not a valid city name! You have to choose between chicago, new york city or washington:')
            city = input().lower()

    # ask the user is preference for the data filtering
    error_1 = True
    choice = input('Would you like to filter the data by Month, Day, Both or not at all. Type " None" for not at all:\n').title()
    while error_1 == True:
        if choice in ['Month', 'Day', 'Both', 'None']:
            error_1 = False
        else:
            print('That\'s not a valid choice! Please type Month, Day, Both or None:')
            choice = input().title()

    # get user input for month (all, january, february, ... , june)
    if choice == 'Month':
        day = 'all'
        error = True
        month = input('Which month? January, February, March, April, May or June?\n').title()
        while error == True:
            if month in ['January', 'February', 'March', 'April', 'May', 'June']:
                error = False
            else:
                print('That\'s not a valid month! Please select a valid month:')
                month = input().title()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif choice == 'Day':
        month = 'all'
        error = True
        day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n').title()
        while error == True:
            if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                error = False
            else:
                print('That\'s not a valid day! Please select a valid day:')
                day = input().title()

    # get user input for month and day
    elif choice == 'Both':
        error = True
        month = input('Which month? January, February, March, April, May or June?\n').title()
        while error == True:
            if month in ['January', 'February', 'March', 'April', 'May', 'June']:
                error = False
            else:
                print('That\'s not a valid month! Please select a valid month:')
                month = input().title()

        error_1 = True
        day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n').title()
        while error_1 == True:
            if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                error_1 = False
            else:
                print('That\'s not a valid day! Please select a valid day:')
                day = input().title()

    else:
        month = 'all'
        day = 'all'

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_number = df['month'].mode()[0]
    common_month = calendar.month_name[int(month_number)]
    print('Most common month:', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day:', common_day)

    # display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most common hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most common start station:', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most common end station:', common_end)

    # display most frequent combination of start station and end station trip
    common_comb = df.groupby(['Start Station','End Station']).size().agg(['idxmax'])
    common_comb_start = common_comb[0][0]
    common_comb_end = common_comb[0][1]
    print('Most frequent combination of start station and end station trip: {} with {}'.format(common_comb_start, common_comb_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = pd.Timedelta(df['Trip Duration'].sum(), unit='seconds')
    print('Total travel time:', total_time)

    # display mean travel time
    mean_time = pd.Timedelta(df['Trip Duration'].mean(), unit='seconds')
    print('Mean travel time:', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('Number of {}:'.format(user_types.keys()[0]), user_types[0])
    print('Number of {}:'.format(user_types.keys()[1]), user_types[1])

    # display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('Number of {}:'.format(gender.keys()[0]), gender[0])
        print('Number of {}:'.format(gender.keys()[1]), gender[1])

    else:
        print('No data available for Gender in Washington database')

    # display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        print('Earliest year of birth:', earliest)

        recent = int(df['Birth Year'].max())
        print('Most recent year of birth:', recent)

        common = int(df['Birth Year'].mode()[0])
        print('Most common year of birth:', common)

    else:
        print('No data available for Birth Year in Washington database')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays 5 lines of raw data if requested by user."""

    # update to show all columns
    pd.set_option('display.max_columns',200)

    i = 0
    while True:
        request = input('\nWould you like to display 5 lines of raw data? Enter yes or no.\n')
        if request.lower() == 'yes':
            print(df[i:i+5])
            i += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
