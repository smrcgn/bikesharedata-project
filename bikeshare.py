import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Args:
        None.
    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #filter by city
    city = ''

    while city not in CITY_DATA.keys():
        print("\nwhich city you will choose to analyze?: ")
        print("\n Chicago, New York City, or Washington?")

        #converting into lower to standardize them
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\n Oops! you can select only the city specified in CITY_DATA or please check your spelling.")

    #filter by month
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nWhich month you select for analysing the data, january, february,...,june, all: ")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\n Oops! You can only select month specified in MONTH_DATA or please check your spelling.")

    #filter by day
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nWhich day you select for analysing the data; monday, tuesday,...sunday, all: ")
        day = input().lower()

        if day not in DAY_LIST:
            print("\n Oops! You can only select day specified in DAY_LIST or please check your spelling")

    print("\nYou have chosen to view data for city: {city.upper()}, month: {month.upper()} and day: {day.upper()}")
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    #Converting the "Start Time" column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Creating new column by extracting month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    #Filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    print("\nMost Common Month (1 = january,...,6 = june): {most_common_month}")

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]

    print("\nMost Common Day: {common_day_of_week}")

    # display the most common start hour
    # creating hour column
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print("\nMost Popular Start Hour: {most_common_start_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station: {common_start_station}")

    # display most commonly used end station

    common_end_station = df['End Station'].mode()[0]
    print("\nThe most commonly used end station: {common_end_station}")

    # display most frequent combination of start station and end station trip

    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep =' to ')
    combined = df['Start To End'].mode()[0]
    print("\nThe most frequent combination of trips are from {combined}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_type = df['User Type'].value_counts()
    print("The types of users counted as below:\n{user_type}")

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("\nThe types of users by gender are given below:\n{gender}")
    except:
        print("\nThere is no 'Gender' column.")

    # Display earliest, most recent, and most common year of birth

    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):

    #Display contents as requested by the user.

    start_row = 0
    end_row = 5

    see_data = input("\nIf you want to see the raw data, please type 'yes' or 'no': ").lower()

    if see_data == 'yes':
        while end_row <= df.shape[0] - 1:

            print(df.iloc[start_row:end_row,:])
            start_row += 5
            end_row += 5

            end_display = input("\nIf you want to see more rows, please type 'yes' or 'no': ").lower()
            if end_display == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
