import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york city', 'washington']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DOW = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def confirm_choice(city_filter, month_filter, day_filter):
    """
    Asks user to confirm choice of filters and requests for new filters if mistake was made

    Args:
        (str) city - name of chosen city to filter by
        (str) month - name of chosen month to filter by
        (str) day - name of chosen day of the week to filter by
    """
    if month_filter != 'all':
        month_filter = MONTHS[int(month_filter) - 1]
    if day_filter != 'all':
        day_filter = DOW[int(day_filter) - 1]
    
    message = "\nYou will be exploring {}'s data by month: {} and day: {}".format(city_filter, month_filter, day_filter)
    
    print(message)
    while True:
        try:
            choice = input('Would you like to make changes to your filters? Enter yes or no\n').lower()
            if not choice.isalpha():
                raise ValueError
            if choice not in ['yes', 'no']:
                raise ValueError
            
            print('-'*40)
            break
        except:
            print('Enter yes or no')
    
    return choice

def get_day():
    """
    Asks user to specify particular day to analyze

    Returns:
        (int) day - day of the week to be analyzed
    """

     # get user input for day of week (monday, tuesday, ... sunday)
    while True:
        try:
            day = int(input('What day of the week would you like to look into? Input day of week - Sun = 1, Mon = 2... '))
            # check if day is a number
            if day not in range(1, 8):
                raise KeyError
            break
        except ValueError:
            print("Oh No! Input should be a NUMBER representing the day of the week")
        except AttributeError:
            print("Oh No! Input should be a NUMBER representing the day of the week")
        except KeyError:
            print("Ooops! Try that again. It's just Sunday to Saturday")
    return day

def get_month():
    """
    Asks user to specify particular month to analyze

    Returns:
        (int) month - month to be analyzed
    """

     # get user input for month (january, february, ... , june)
    while True:
        try:
            month = int(input('What month would you like to explore (Jan to Jun)? Input month number - Jan = 1, Feb = 2... '))
            # check if month only is a number
            if month not in range(1, 7):
                raise KeyError
            break
        except ValueError:
            print("Oh No! Input should be a NUMBER representing the day of the week")
        except AttributeError:
            print('Nope! Input should be a NUMBER representing the month')
        except KeyError:
            print('Nahh! Month should be between January to June')
    return month            

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) filterby - the filter applied: "month", "day" or "both"
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        month = 'all' 
        day = 'all'
        while True:
            try:
                city = input('\nWhat city\'s data would you like to explore - "chicago"," new york city", "washington": ').lower()
                # check if city only has alphabets
                if not city.replace(' ', 'a').isalpha():
                    raise ValueError
                if city not in CITIES:
                    raise KeyError
                print("We are about to explore {}'s bikeshare data. This will be interesting\n".format(city))
                break
            except:
                print('Ooops! You typed a wrong city name. City should be "chicago", "new york city" or "washington"')
                
        while True:
            try:
                filterby = input("How would you like to filter the data? 'Month', 'Day', 'Both' or 'None' ").lower()
                if filterby not in ['month', 'day', 'both', 'none']:
                    raise KeyError
                break
            except:
                print("Enter 'Month', 'Day', 'Both', or 'None'. 'None' applies no filter at all")
        
        if filterby == "both":
            # get user input for month (january, february, ... , june)
            month = get_month()

            # get user input for day of week (monday, tuesday, ... sunday)
            day = get_day()
            
        if filterby == "month":
            # get user input for month (january, february, ... , june)
            month = get_month()
                    
        if filterby == 'day':
            # get user input for day of week (monday, tuesday, ... sunday)
            day = get_day()
                    
        choice = confirm_choice(city, month, day)
        if choice == 'no':
            print("\nAlright explorer, let the adventure begin!!!")
            print('-'*40)
            return city, month, day, filterby
            break

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load city data into dataframe df
    df = pd.read_csv(CITY_DATA[city])

    # change start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day and hour of the week from start time column
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if filter is inputted
    if month != "all":
        # get a new df based on the month input
        df = df[(df['Month'] == month)]

    # filter by day if filter is inputted
    if day != "all":
        day = DOW[day - 1]

        # filter by day of the week to create df
        df = df[(df['Day_of_week'] == day.title())]

    return df

def print_common_month(df):
    """Display most common month of travel"""

    common_month = df['Month'].mode()[0]
    common_month = MONTHS[common_month - 1].title()
    month_count = df['Month'].value_counts().max()
    print('Well, {} has the most travels.\t Count: {}\n'.format(common_month, month_count))

def print_common_dow(df):
    """Display most common day of week of travel"""

    common_dow = df['Day_of_week'].mode()[0]
    dow_count = df['Day_of_week'].value_counts().max()
    print('Most popular day is {}\t Count: {}\n'.format(common_dow, dow_count))

def print_common_hour(df):
    """Display most coomon hour of travel"""

    common_hour = df['Start Time'].dt.hour.mode()[0]
    hour_count = df['Hour'].value_counts().max()
    print('The most common hour is {} hr(s)\t Count: {}\n'.format(common_hour, hour_count))

def time_stats(df, filterby):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('')
    start_time = time.time()

    # if there are no filters applied to month and day - all months and days included
    if filterby == 'none':
        # display the most common month
        print_common_month(df)

        # display the most common day of week
        print_common_dow(df)

        # display the most common start hour
        print_common_hour(df)

    # if the filter is applied to the month - all days included
    elif filterby == 'month':
        # display the most common dow
        print_common_dow(df)

        # display the most common start hour
        print_common_hour(df)

    # if the filter is applied to the day - all months included
    elif filterby == 'day':
        # display the most common month
        print_common_month(df)

        # display the most common start hour
        print_common_hour(df)

    # if filters are applied to both month and day - data is for only a particular month and day
    else:
        # display the most common start hour
        print_common_hour(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].value_counts().index[0]
    common_start_freq = df['Start Station'].value_counts().max()
    print('{} is the most popular start station\t Count: {}\n'.format(common_start, common_start_freq))

    # display most commonly used end station
    common_end = df['End Station'].value_counts().index[0]
    common_end_freq = df['End Station'].value_counts().max()
    print('{} is the most popular end station\t Count: {}\n'.format(common_end, common_end_freq))

    # display most frequent combination of start station and end station trip
    start_end_combo = df.groupby([df['Start Station'], df['End Station']]).size().sort_values(ascending=False)
    start_end_station = start_end_combo.index[0]
    start_end_max = start_end_combo.max()
    print('{} to {} is the most popular route\t Count: {}\n'.format(start_end_station[0], start_end_station[1], start_end_max))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def calc_time(seconds):
    """
    Calculates time in days, hours, minutes and seconds.

    Args:
        (int) seconds: time in seconds

    Returns:
        (str) time_str: string of time in days, hours, minutes and seconds
    """
    days = 0
    hours = 0
    minutes = seconds // 60
    secs = seconds % 60
    if minutes > 60:
        hours = minutes // 60
        minutes = minutes % 60
    if hours > 24:
        days = hours // 24
        hours = hours % 24

    time_str = ''

    if days == 0 and hours == 0:
        time_str = '{} minutes and {:.1f} seconds'.format(minutes, secs)
    elif days == 0:
        time_str = '{} hours, {} minutes and {:.1f} seconds'.format(hours, minutes, secs)
    else:
        time_str = '{} days, {} hours, {} minutes and {:.1f} seconds'.format(days, hours, minutes, secs)
    
    return time_str

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    time_str = calc_time(total_travel_time)
    print('The total travel time is: {}'.format(time_str))
    

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    time_str = calc_time(mean_travel_time)
    print('The mean travel time is: {} per travel'.format(time_str))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(df['User Type'])['User Type'].count()
    user_type_names = list(user_types.index)
    user_type_count = user_types.values
    print("The users are categorized as: ")
    for user_type, count in zip(user_type_names, user_type_count):
        print(user_type, count)

    if city != 'washington':
        # Display counts of gender
        genders = df.groupby(df['Gender'])['Gender'].count()
        genders_list = list(genders.index)
        gender_count = genders.values
        print("\nThe users' gender stats are: ")
        for gender, count in zip(genders_list, gender_count):
            print(gender, count)
        print('\n')

        # Display earliest, most recent, and most common year of birth
        birth_years = df['Birth Year'].fillna(method='ffill', axis=0)
        print('The earliest/oldest birth year is ' + str(birth_years.min()))
        print('The most recent/youngest birth year is ' + str(birth_years.max()))
        print('The most common birth year is {}\t Count: {}'.format(birth_years.mode()[0], birth_years.value_counts().iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def disp_raw_data(df):
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    row_no = len(df.index) + 1
    df.index = range(1, row_no + 1)
    pd.set_option('display.max_columns',200)
    i = 0
    show_data = 'yes'
    
    while i < len(df.index):
        if show_data == "no":
            break
            
        print(df[i:i + 5])
        i += 5
        
        while True:
            try:
                show_data = input('\nWould you still like see more raw data? yes or no.\n').lower()
                if not show_data.isalpha():
                    raise ValueError
                if show_data in ['yes', 'no']:
                    break
            except:
                print('Enter yes or no')

def main():
    while True:
        city, month, day, filterby = get_filters()
        df = load_data(city, month, day)

        time_stats(df, filterby)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        while True:
            try:
                raw_data = input('\nWould you like to see raw data? yes or no.\n').lower()
                if not raw_data.isalpha():
                    raise ValueError
                if raw_data == "yes":
                    disp_raw_data(df)
                    break
                else:
                    break
            except:
                print('Enter yes or no')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
