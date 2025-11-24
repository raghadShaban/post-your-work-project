import time
import pandas as pd
import numpy as np
import calendar as cal
# array with keys
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Ask user which city, month and day they want to explore.
    Returns the chosen filters for data analysis.
    """
    print('Hello!Im Raghad. Let\'s explore some US bikeshare data Together!!')
    # Ask user for  the city choice
    while True:
        city = input("Which city would you like to explore?\nChicago, New York City, or Washington:\n")
        city = city.lower().strip()  #Lowercase and remove spaces on edges
        if city in CITY_DATA:
            break
        else:
            print("that's not a valid city. It's either: Chicago, New York City, or Washington.\n")
    # same logic as the cities but for months
    while True:
        print(f"\nNow let's choose a month for {city.title()}.")
        month = input(" January, February, March, April, May, June, or type 'all' for all months: ")
        month = month.lower().strip()
        #ARRAY of months
        valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        if month in valid_months:
            break
        else:
            print("Not valid choose from: January, February, March, April, May, June, or type 'all' for all months:\n")
    while True:
        print(f"\n  choose a day of the week for {city.title()}.")
        day = input("(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.) or type 'all' for all days: ")
        day = day.lower().strip()
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        if day in valid_days:
            break
        else:
            print("that's not a valid day. Please enter a day or 'all'.\n")
    print('-' * 40)
    print(f"Great! You've chosen :")
    print(f"City: {city.title()}")
    print(f"Month: {month.title()}")
    print(f"Day: {day.title()}")
    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Load the data file for chosen city and filter by month/day if needed.
    Returns the filtered dataframe ready for analysis.
    """
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_number = months.index(month) + 1
        df = df[df['Month'] == month_number]
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_number = days.index(day)
        df = df[df['Weekday'] == day_number]
    return df

def display_raw_data(df):
    """
    Show raw data 5 rows at a time if user wants to see it.
    Keeps showing more data until user says 'no' or runs out.
    """
    try:
        if not isinstance(df, pd.DataFrame):
            print("Error: Invalid data format.")
            return
        if df.empty:
            print("\nNo data available for the selected filters.")
            return
        i = 0
        total_rows = len(df)
        print(f"\nDataset contains {total_rows} rows of data.")
        while True:
            raw = input("\nDo you want to see the first 5 rows of raw data? Enter yes or no: ").lower().strip()
            if raw in ['yes', 'no']:
                break
            else:
                print("Please enter only 'yes' or 'no'.")
        pd.set_option('display.max_columns', 200)
        while raw == 'yes':
            end_index = min(i + 5, total_rows)
            print(f"\nRows {i + 1} to {end_index} of {total_rows}:")
            print('=' * 80)
            print(df.iloc[i:end_index])
            print('=' * 80)
            i = end_index
            if i >= total_rows:
                print("\nAll data has been displayed.")
                break
            while True:
                raw = input("\nDo you want to see the next 5 rows? Enter yes or no: ").lower().strip()
                if raw in ['yes', 'no']:
                    break
                else:
                    print("Please enter only 'yes' or 'no'.")
    except Exception as e:
        print(f"\nAn error occurred while displaying raw data: {e}")
    finally:
        pd.reset_option('display.max_columns')

def time_stats(df, city, month, day):
    """
    Show stats about popular travel times - most common month, day, and hour.
    """
    print('\nCalculating The Most Frequent Times of Travel.\n')
    start_time = time.time()
    common_month_number = df['Month'].mode()[0]
    common_month_name = cal.month_name[common_month_number]
    if month != 'all':
        print(f'you selected {month.title()}, we are only looking at data from {common_month_name}.')
    else:
        print(f'The most popular month for biking in {city.title()} is {common_month_name}.')
    common_day_number = df['Weekday'].mode()[0]
    common_day_name = cal.day_name[common_day_number]
    if day != 'all':
        print(f' you selected {day.title()}, we are only looking at data from {common_day_name}s.')
    else:
        print(f'The most popular day for biking in {city.title()} is {common_day_name}.')
    df['Start Hour'] = df['Start Time'].dt.hour
    common_hour = df['Start Hour'].mode()[0]
    print(f'The most common hour to start biking is {common_hour}:00.')
    end_time = time.time()
    print(f"\nThis analysis took {round(end_time - start_time, 2)} seconds.")
    print('-' * 40)

def station_stats(df):
    """
    Show stats about popular stations and most common trip routes.
    """
    print('\nCalculating The Most Popular Stations and Trip.\n')
    start_time = time.time()
    common_start_station = df['Start Station'].mode()[0]
    print(f'The most popular station to start a trip is: {common_start_station}')
    common_end_station = df['End Station'].mode()[0]
    print(f'The most popular station to end a trip is: {common_end_station}')
    df['Trip Combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Trip Combination'].mode()[0]
    print(f'The most popular trip route is: {common_trip}')
    end_time = time.time()
    print(f"\nThis analysis took {round(end_time - start_time, 2)} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """
    Show stats about trip durations - total and average travel time.
    """
    print('\nCalculating Trip Duration.\n')
    start_time = time.time()
    total_seconds = df['Trip Duration'].sum()
    total_hours = round(total_seconds / 3600, 1)
    print(f' total travel time for all trips is {total_hours} hours.')
    average_seconds = df['Trip Duration'].mean()
    average_minutes = round(average_seconds / 60, 1)
    print(f' average trip duration is {average_minutes} minutes.')
    end_time = time.time()
    print(f"\nThis analysis took {round(end_time - start_time, 2)} seconds.")
    print('-' * 40)

def user_stats(df, city):
    """
    Show stats about users - types, gender, and birth years when available.
    Washington doesn't have gender or birth year data.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    print('User Type Information:')
    for user_type, count in user_types.items():
        print(f'  - {user_type}s: {count}')
    if city.lower() != 'washington':
        print('\nGender Information:')
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            print(f'  - {gender}: {count}')
        print('\nBirth Year Information:')
        youngest = df['Birth Year'].max()
        print(f'  - Most recent birth year: {int(youngest)}')
        oldest = df['Birth Year'].min()
        print(f'  - Earliest birth year: {int(oldest)}')
        most_common = df['Birth Year'].mode()[0]
        print(f'  - Most common birth year: {int(most_common)}')
    else:
        print('\nNote: Gender and birth year information is not available for Washington.')
    end_time = time.time()
    print(f"\nThis analysis took {round(end_time - start_time, 2)} seconds.")
    print('-' * 40)

def main():
    """
    Run the main bikeshare analysis program.
    Welcome users, show stats, and let them restart or exit.
    """
    print('=' * 50)
    print('WELCOME TO THE US BIKESHARE DATA ANALYSIS PROGRAM HOPE YOU FIND IT USEFUL :)!')
    print('=' * 50)
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)
        while True:
            restart = input('\nWould you like to explore more data? Enter yes or no: ')
            restart = restart.lower().strip()
            if restart in ['yes', 'no']:
                break
            else:
                print("Please enter 'yes' or 'no'.")
        if restart == 'no':
            print('\nThank you for using the Bikeshare Data Analysis Program!')
            print('Goodbye!')
            break
        else:
            print('\n' + '=' * 50)
            print('RESTARTING PROGRAM...')
            print('=' * 50)

if __name__ == "__main__":
    main()