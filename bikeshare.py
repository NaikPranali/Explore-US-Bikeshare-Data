# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 08:19:40 2018

@author: pranali naik
"""

# import all required packages 
import time
import numpy as np
import pandas as pd

# files
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

# ProjSummary:
# calculated descriptive statistics data of cities in USA with the help of user interface
# for selecting city and others filters in the data such as month & day.

def city_info():
    ''' Asks the user to select city and returns filename for respective bike share data
    Args:
        none
    returns:
        filename for bikeshare data of selected city
    '''
    city = input('\n Hello! let\'s explore some US Bikeshare Data !\n'
                 '\n Would you like to see data for Chicago(CH), New York (NY),Washington (WA)?\n' )
    city = city.lower()
    while True:
        if city == "ny" or city == "new york":
            print('\n Looks like you want to hear about New York City !\n'
                  '\n Let\'s explore its bikeshare data !\n')
            return new_york_city
        elif city == "ch" or city == "chicago":
            print('\n Looks like you want to hear about Chicago !\n'
                  '\n Let\'s explore its bikeshare data !\n')
            return chicago
        elif city == "wa" or city == "washington":
            print('\n Looks like you want to hear about Washington !\n'
                  '\n Let\'s explore its bikeshare data !\n')
            return washington
        city = input("Please choose between Chicago (CH), New York (NY), or Washington (WA)")
        city = city.lower()
        
def time_period_info():
    ''' Asks user for time period and returns respective information
    Args:
        none
    returns:
        time period information
    '''
    time_period = input('\nWould you like to filter the data by month (m) and day of the month, day of the week (d), or not at all? Type "none" for no time filter.\n')
    
    time_period = time_period.lower()
    while True:
        if time_period == 'm' or time_period == 'month':
            while True:
                filterByDayofMonth = input("\n Would you like to filter by day of the month too ? Type 'YES' or 'NO' \n").lower()
                if filterByDayofMonth == "no":
                    print(" We are now filterning data by month..... \n")
                    return 'month'
                elif filterByDayofMonth == "yes":
                    print(" We are now filterning data by month and day of the month.... \n")
                    return 'day_of_month'
        if time_period == "d" or time_period == "day":
            print("we are now filtering data by day of the week.....\n")
            return 'day_of_week'
        elif time_period == "n" or time_period == "none":
            print('\n We are not applying any time filter to the data\n')
            return 'none'
        time_period == input("\n Please choose a time filter option between month (m), day of the week (d), or none (n) \n").lower()
        
def month_info(month_):
    '''Asks user to select month and returns the same
    Args:
        none
    returns:
        month information
    '''
    if month_ == 'month':
        month = input('\n Which month?' '\n January, February, March, April, May, or June?''\n Please type the full month name.\n')
        while month.strip().lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease choose between January, February, March, April, May, or June?' '\n Please type the full month name.\n')
        return month.strip().lower()
    else:
        return 'none'
    
def day_of_month_info(df, dayofmonth_):
    ''' Asks user for day of the month and month and returns information realted to both
    Args:
        dayofmonth_  - output of time_period_info()
        df           - dataframe with all bikeshare data
    returns:
        MonthAndDay list - list with all month and day information
    '''
    
    MonthAndDay = []
    
    
    if dayofmonth_ == "day_of_month":
        month = month_info("month")
        MonthAndDay.append(month)
        
        num_of_days_month = get_max_day_of_month(df, month)
        
        while True: 
            
            promptstr = """\n Which day of the month? \n Please type your response as an integer between 1 and """
            
            promptstr = promptstr + str(num_of_days_month) + "\n"
            
            dayofmonth = input(promptstr)
            
            try:
                dayofmonth = int(dayofmonth)
                
                if 1 <= dayofmonth <= num_of_days_month:
                    MonthAndDay.append(dayofmonth)
                    return MonthAndDay
            except ValueError:
                print("That's not an integer, please enter valid input")
    else:
        return 'none'
    
def day_info(day_):
    '''Asks user for day and returns the same
    Args:
        day_  - string of data to be filtered by day
    Returns:
        Day information
    '''
    if day_ == "day_of_week":
        day = input("\n which day of the week?""\n Please type a day M, Tu, We, Th, F, Sa, Su.\n")
        while day.strip().lower() not in ['m', 'tu', 'we', 'th', 'f', 'sa', 'su']:
            day = input('\nPlease type a day as a choice from M, Tu, W, Th, F, Sa, Su. \n')
        return day.strip().lower()
    else:
        'none'

def load_data(city):
    ''' It reads city data and load it into dafaframe
    Input:
        city- path to the file
    Output:
        df - data frame to be used for all statistic calculations
    '''
    print('\n Loading the data...''\n.......')
    df = pd.read_csv(city)
    
    # In the given data, we have "Start Time" column from which we can get datetime.
    # We can easily filter the data with these steps
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['day_of_month'] = df['Start Time'].dt.day
    
    return df

def get_filters(df, time_period, month, dayOfWeek, MonthAndDay):
    ''' This function filters the data as per input given by User
    Input:
        df           -- city datafrane
        time_period  -- specified time period , month , day_of_month or day_of _week
        month        -- month used to filter the data. type string
        dayOfWeek    -- week day used to filter the data. tyoe-string
        MonthAndDay  -- month used to filter the data . Tyoe- List
    Output:
        df - dataframe -to be used to calculate according to the selected filters
    '''
    print('Data loaded. Now computing stats... \n')
    print('-'*50)
    
    if time_period == 'month':
        months = [ 'january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
        
    if time_period == 'day_of_week':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days :
            if dayOfWeek.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week'] == day_of_week]
        
    if time_period == 'day_of_month':
        months = [ 'january', 'february', 'march', 'april', 'may', 'june']
        month = MonthAndDay[0]
        month = months.index(month)+1
        df = df[df['month'] == month]
        day = MonthAndDay[1]
        df = df[df['day_of_month'] == day]
        
    return df


def common_month(df):
    ''' Returns most common month for Bikesharing
    Input:
        df - dataframe returned from get_filters
    Output:
        most_common_month - most frequent month.type-string
    ''' 
    print('-'*50)
    print('\nCalculation of the Most Frequent Times of Travel...\n')
    print('-'*50)
    print('\n The is most common month for traveling:')
    mth = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month = months[mth - 1].capitalize()
    return most_common_month 

def common_day(df):
    ''' Returns most common day of week
    Input:
        df - dataframe returned from get_filters
    Output:
        common_day - day with most rides. type-string
    '''
    print( '\n the most popular day of the week (Monday to Sunday) for bike traveling :')
    return df['day_of_week'].value_counts().reset_index()['index'][0]

def common_hour(df):
    '''Returns most common day for travel
    Input:
        df - dataframe returned from get_filters
    Output:
        Most common hour
    '''
    print('\n Most common hour of the day for traveing :')
    df['hour'] = df['Start Time'].dt.hour
    return df.hour.mode()[0]




def common_station(df):
    ''' Returns most common Start and end stations
    Input:
        df - dataframe returned from get_filters
    Output:
        Information about most common Start and end stations
    '''
    print('-'*50)
    print('\nCalculation of the Most Common Station...\n')
    print('-'*50)    
    print('\n the most common start station is: \n')
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print(start_station)
    
    print('\n the most common end station is: \n')
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print(end_station)
    return start_station, end_station


def common_trip(df):
    '''returns common trip
    INPUT:
        df - dataframe returned from get_filters
    OUTPUT:
        most common trip information
    '''
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\n Most common trip from start to end:')
    
    return result


def trip_duration(df):
    '''Returns total trip duration
    INPUT:
        df - dataframe returned from get_filters
    OUTPUT:
        total trip duration, average trip duration
    '''
    print('-'*50)
    print('\n * What was the total traveling done for 2017 through June, and what was the average time spent on each trip?')
    
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum for total trip time, mean for avg trip time
 
    total_travel_time = np.sum(df['Travel Time'])

    totalDays = str(total_travel_time).split()[0]

    print ("\nThe total travel time " + totalDays + " days \n")

    average_travel_time = np.mean(df['Travel Time'])

    averageDays = str(average_travel_time).split()[0]

    print("The average travel time " + averageDays + " days \n")

    return total_travel_time, average_travel_time

def users(df):
    '''returns the count of each User type
    INPUT:
        df - dataframe returned from get_filters
    OUTPUT:
        User type
    '''
    print('-'*50)
    print('\n User Details: \n')
    
    return df['User Type'].value_counts()

def gender(df):
    '''Returns the counts of gender
    INPUT:
        df - dataframe returned from get_filters
    OUTPUT:
        returns counts for each gender
    '''
    print('-'*50)
    try:
        print('\n* Gender Count: \n')

        return df['Gender'].value_counts()
    except:
        print('There is no gender data in the source file.')


def birth_years(df):
    '''Returns earliest, latest, and most frequent birth year
    INPUT:
        df - dataframe returned from get_filters
    OUTPUT:
        earliest, latest, and most frequent year of birth
    '''
    print('-'*50)
    try:
        print('\n the earliest, latest, and most frequent year of birth, respectively :')
        earliest = np.min(df['Birth Year'])
        print ("\nThe earliest year of birth is " + str(earliest) + "\n")
        latest = np.max(df['Birth Year'])
        print ("The latest year of birth is " + str(latest) + "\n")
        most_frequent= df['Birth Year'].mode()[0]
        print ("The most frequent year of birth is " + str(most_frequent) + "\n")
        return earliest, latest, most_frequent
    except:
        print('No available birth date data for this period.')

def time_stat(f, df):
    '''Calculates the time it takes to commpute a stat
    INPUT:
      f  - the applied stats function
      df - the dataframe with all the data
    OUTPUT:
        doesn't return a value
    '''
    
    start_time = time.time()
    statToCompute = f(df)
    print(statToCompute)
    print("Computing this stat took %s seconds." % (time.time() - start_time))
    


def get_max_day_of_month(df, month):
    """
    Gets the max day of the month
    INPUT:
      df - the city dataframe
      month - string of the selected month
    OUTPUT:
       the max day of the month. type-integer
    """
    months = {"january": 1, "february": 2, "march": 3, "april":4, "may": 5, "june":6}
    df = df[df["month"] == months[month]]
    
    maxDay = max(df["day_of_month"])
    return maxDay

def display_raw_data(df):
    """
    Displays the data used to compute the stats
    Input:
      df-  the dataframe with all the bikeshare data
    Returns: 
       none
    """
    
    df = df.drop(['month', 'day_of_month'], axis = 1)
    
    rowIndex = 0

    seeData = input("\n Would you like to see rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()

    while True:

        if seeData == 'no':
            return

        if seeData == 'yes':
            print(df[rowIndex: rowIndex + 5])
            rowIndex = rowIndex + 5

        
        seeData = input("\n Would you like to see five more rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()
    
def stats():
    
    '''Calculates and prints out the descriptive statistics about a city
    and time period specified by the user through raw input.
    Args:
        none.
    Returns:
        none.
    '''
    
    city = city_info()
    df = load_data(city)
    time_period = time_period_info()
    month = month_info(time_period)
    day = day_info(time_period)
    MonthAndDay = day_of_month_info(df, time_period)
    df = get_filters(df, time_period, month, day, MonthAndDay)
    display_raw_data(df)
    stat_function_list = [common_month,
                         common_day, common_hour,
                         common_station,
                         common_trip,
                         trip_duration,
                         users, gender, birth_years
                         ]  
   
    for fun in stat_function_list:
        time_stat(fun, df)
        
    restart = input("\n * Would you like to restart and perform another analysis? Type \'yes\' or \'no\'.\n")
    if restart.upper() == 'YES' or restart.upper() == "Y":
        stats()
        

if __name__ == '__main__':
    stats()
    
    
    
        
    
    
    
    
    

            
    
                
            
            
            
    
    
    


