import time
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

    # get user input for city (chicago, new york city, washington).
    while True: # loop to handle errors: asks the user to enter one of the available cities (case insensitive)
        try:
            city = input('What city would you like data for?\n').lower()
        except:
            print('\nPlease enter one of the available cities: Chicago, New York City, Washington\n')            
        else:
            if city in CITY_DATA.keys():
                break
            else:
                print('\nPlease enter one of the available cities: Chicago, New York City, Washington\n')            


    # get user input for month (all, january, february, ... , june)
    while True: # loop to handle errors - requires month name in full (case insensitive) or 'all
        try:
            month = input('What month would you like data for? (Type "all" if all months are required.)\n').lower()
        except:
            print('\nPlease enter the name of a month, eg. "January"\n')            
        else:
            if month in ['all','january','february','march','april','may','june',\
                         'july','august','september','october','november','december']:
                break
            else:
                print('\nPlease enter the name of a month, eg. "January"\n')            


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True: # loop to handle errors - requires day of the week name in full (case insensitive) or 'all'
        try:
            day = input('What day would you like data for? (Type "all" if all days are required.)\n').lower()
        except:
            print('\nPlease enter the name of a day of the week, eg. "Monday"\n')            
        else:
            if day in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
                break
            else:
                print('\nPlease enter the name of a day of the week, eg. "Monday"\n')   

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
    city = city.replace(" ", "_",) # replaces spaces with underscores to read city filename
    df = pd.DataFrame(pd.read_csv(f'{city}.csv'))

    # conversion to datetime and addition of 'month' and 'day of week' columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.day_of_week

    # set of if statements to apply filters for month/day (if 'all' not input)
    if month != 'all':
        all_months = ['january','february','march','april','may','june',\
                      'july','august','september','october','november','december']
        month = all_months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    all_months = ['january','february','march','april','may','june',\
                  'july','august','september','october','november','december']
    print(f"Most common month : {all_months[ df['month'].mode().item()-1 ].capitalize()}") # output is capitalised

    # display the most common day of week
    all_days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    print(f"Most common day of the week : {all_days[ df['day of week'].mode().item()-1 ].capitalize()}") # output is capitalised

    # display the most common start hour
    print(f"Most common start hour : {df['Start Time'].dt.hour.mode().item()}:00") # output is formatted as 24hr clock

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(f"Most common start station : {df['Start Station'].mode().item()}") # .item() takes the element in the single-element series output by .mode()

    # display most commonly used end station
    print(f"Most common end station : {df['End Station'].mode().item()}")

    # display most frequent combination of start station and end station trip
    print(f"Most common route : " + f"{df[['Start Station','End Station']].mode().values.tolist()}"[2:-2]) # remove square brackets before and after

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time']) # convert end time to datetime
    print(f"Total travel time : {df['End Time'].sub(df['Start Time']).sum()}") # subtract end time from start time to get travel time and sum for total

    # display mean travel time
    print(f"Mean travel time : {df['End Time'].sub(df['Start Time']).mean()}") # subtract end time from start time to get travel time and average

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"Numbers of different user types : \n" + f"{df['User Type'].value_counts()}\n"[10:-26]) # remove column header & datatype footer

    # Display counts of gender
    print(f"Gender counts : " + f"{df['Gender'].value_counts()}\n"[6:-26]) # remove column header & datatype footer

    # Display earliest, most recent, and most common year of birth
    print(f"Earliest birth year : " + f"{int(df['Birth Year'].min().item())}") # int( ... .item()) prints as an integer
    print(f"Most recent birth year : " + f"{int(df['Birth Year'].max().item())}")
    print(f"Most common birth year : " + f"{int(df['Birth Year'].mode().item())}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def present_raw(df):
    """Asks the user if they would like to see the raw dataset and returns 5 lines at a time"""
    
    counter = 299993;

    # ask user whether they want detailed statistics
    while True: # loop to handle errors: asks the user to enter one of the available cities (case insensitive)
        try:
            user_in = input('Would you like to see 5 lines of raw data? (Type yes or no)\n').lower()
        except:
            print('\nPlease enter yes or no\n')            
        else:
            if user_in.lower() == 'yes':
                if counter+5 > df.shape[0]:
                    print(df.iloc[counter:df.shape[0]])
                    print("\nEnd of dataset reached")
                    break
                else:
                    print(df.iloc[counter:counter+5])
                    counter += 5
            elif user_in.lower() == 'no':
                break
            else:
                print('\nPlease enter yes or no\n')  

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        present_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
