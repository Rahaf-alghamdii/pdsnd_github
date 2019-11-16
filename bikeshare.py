import pandas as pd
from datetime import datetime,timedelta #we need timedelta here as zone
import time


def select_city():
    #Ask the user for a city and return the CSV File name of it
    state = '' #Init empty value for while loop
    all_states = ['new york', 'chicago', 'washington'] #list of states we have
    while state.lower() not in all_states: #set the value user type as lowercase in city variable
        state = input('Let\'s explore some data from United States!\n' 'Would you like to see '
                      'data for  New York, Chicago, or' ' Washington?\n')
        if state.lower() == 'new york':
            return 'new_york_city.csv'
        elif state.lower() == 'chicago':
            return 'chicago.csv'
        elif state.lower() == 'washington':
            return 'washington.csv'
        else:
            print('Sorry we cant find that, make sure you select one state from the list [Chicago, '
                  'New York, or Washington].')


def ask_period():
    #Ask for the period 'Month,Day or none' so we can filter the data into one of them
    period = '' #Init empty value for while loop
    available_period = ['month', 'day', 'none'] #List for available periods
    while period.lower() not in available_period:
        period = input('\nWould you like the see data by month, day,'' or not at all? Select "none" '
                       'for no filter.\n')
        if period.lower() not in ['month', 'day', 'none']:
            print('Sorry, Double check you select one from the list "month , day , none".')
    return period


def ask_month():
    #If the user selected period as month so he have to select which month
    month_i = '' #Init empty value for while loop
    m_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4,
                   'may': 5, 'june': 6} #Dictionary for months as Key with a number as Value
    while month_i.lower() not in m_dict.keys(): #make dict keys as list and then search on them
        month_i = input('\nWhich month? January, February, March, April,'
                            ' May, or June?\n')
        if month_i.lower() not in m_dict.keys(): #If unlisted month
            print('Please Selects a '
                  'month between January and June')
    month = m_dict[month_i.lower()]
    return ('2017-{}'.format(month), '2017-{}'.format(month + 1)) #return Date of this month and the upcoming month


def ask_day():
    #If the user selected period as day so he have to select which Month then which Day
    this_month = ask_month()[0] #Ask for month and get current month
    month = int(this_month[5:]) #Extract the month only from the date ex.ask_month()[0] will be '2017-4' so this_month[5:] will be 4
    valid = False #Assume date isn't correct at first
    while valid == False:    
        is_int = False #Assume the day is not int
        day = input('\nWhich day? Integer Only.\n')
        while is_int == False:
            try:
                day = int(day)
                is_int = True
            except ValueError: #if we got something other than int so ask again
                print('Sorry, Make sure you type integer only.')
                day = input('\nWhich day? Integer Only.\n')
        try:
            start_date = datetime(2017, month, day) #Make a DateTime value
            valid = True #Set the date to True so we know Date is correct
        except ValueError as e:
            print(str(e).capitalize())
    end_date = start_date + timedelta(days=1)
    return (str(start_date), str(end_date))


def popular_month(df):
    #Find the most popular month then print it
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['start_time'].dt.month.mode()) #get the index of the post popular month using datetime lib
    pop = months[index - 1] #Get the month name from the list
    print('The most popular month is {}.'.format(pop))


def popular_day(df):
    #Find the most popular day and return it as str
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday']
    index = int(df['start_time'].dt.dayofweek.mode()) #get the index of the post popular day using datetime lib
    pop = days[index] #Get the day name from the list
    print('The most popular day is {}.'.format(pop))


def popular_hour(df):
    #Find the most popular day
    pop = int(df['start_time'].dt.hour.mode()) #get the most popular hour
    if pop == 0:
        am_pm = 'am'
        pop_hour = 12
    elif 1 <= pop < 13:
        am_pm = 'am'
        pop_hour = most_pop_hour
    elif 13 <= pop < 24:
        am_pm = 'pm'
        pop_hour = pop - 12
    print('The most popular hour is {}{}.'.format(pop_hour, am_pm))

    


def popular_stations(df):
    #Get 'start_staion' and 'end_station' and print the most popular one
    start = df['start_station'].mode().to_string(index = False) #Get most popular date in 'start_station' column
    end = df['end_station'].mode().to_string(index = False) #Get most popular date in 'end_station' column
    print('The most popular start station is {}.'.format(start))
    print('The most popular end station is {}.'.format(end))

def popular_journy(df):
    #Get all the 'journy' column info and then print the most popular journey
    pop = df['journey'].mode().to_string(index = False)
    # The 'journey' column is created in the program() function.
    print('The most popular journey is {}.'.format(pop))


def trip_duration(df):
    #Get the trip_duration column info and find the average trip duration
    total_duration = df['trip_duration'].sum() #sum all duration values
    minute, second = divmod(total_duration, 60) #make division store in minute and the reminder at second
    hour, minute = divmod(minute, 60) #make division store in hour and the reminder at minute
    print('The total trip duration is {} hours, {} minutes and {}' ' seconds.'.format(hour, minute, second))
    average_duration = round(df['trip_duration'].mean()) #Get the Mean value 'AVG'
    m, s = divmod(average_duration, 60)
    if m > 60: #if the duration is larger than one hour
        h, m = divmod(m, 60)
        print('The average trip duration is {} hours, {} minutes and {}' ' seconds.'.format(h, m, s))
    else:
        print('The average trip duration {} minutes and {} seconds.'.format(m, s))

        
def users(df):
    #Find out how many Subscriber and customer
    subscriber = df.query('user_type == "Subscriber"').user_type.count() #Get all Subscriber and count them
    customer = df.query('user_type == "Customer"').user_type.count() #Get all customer and count them
    print('There are {} Subscribers and {} Customers.'.format(subscriber, customer))


def birth_years(df):
    #Get all 'birth_year' column info and find the minumum value as 'earliest' and max as 'latest' and mode as the most popular
    earliest = int(df['birth_year'].min())
    latest = int(df['birth_year'].max())
    pop = int(df['birth_year'].mode()) #Find most popular
    print('The oldest users are born in {}.\nThe youngest users are born in {}.' '\nThe most popular birth year is {}.'.format(earliest, latest, pop))


def gender(df):
    #Find how many Male and female
    male = df.query('gender == "Male"').gender.count() #Access 'Gender' column in the file and count how many 'Male'
    female = df.query('gender == "Female"').gender.count() #Access 'Gender' column in the file and count how many 'Female'
    print('There are {} male users and {} female users.'.format(male, female))


def birth_years(df):
    #Get all 'birth_year' column info and find the minumum value as 'earliest' and max as 'latest' and mode as the most popular
    earliest = int(df['birth_year'].min())
    latest = int(df['birth_year'].max())
    pop = int(df['birth_year'].mode()) #Find most popular
    print('The oldest users are born in {}.\nThe youngest users are born in {}.' '\nThe most popular birth year is {}.'.format(earliest, latest, pop))

def display_data(df):
    #Ask if user want to see 5 rows of data in tables or no and if yes ask him if he want to show another 5 rows or no etc...
    def is_valid(display):
        if display.lower() in ['yes', 'no']:
            return True
        else:
            return False
    head = 0 #first
    tail = 5 #end
    valid_input = False #Make sure user type 'yes'&'no' Only
    while valid_input == False: #keep asking as much as the user type yes or no
        display = input('\nWould you like to view some data in table? '
                        'Type \'yes\' or \'no\'.\n')
        valid_input = is_valid(display) #Check the user typed 'yes' or 'no' only
        if valid_input == True:
            break
        else:
            print("Please type 'yes' or"
                  " 'no'.")
    if display.lower() == 'yes':
        print(df[df.columns[0:-1]].iloc[head:tail]) #Print 5 rows of data
        display_more = ''
        while display_more.lower() != 'no':
            valid_input_2 = False
            while valid_input_2 == False: #Ask if he wants more
                display_more = input('\nWould you like to view more individual'
                                     ' trip data? Type \'yes\' or \'no\'.\n')
                valid_input_2 = is_valid(display_more)
                if valid_input_2 == True:
                    break
                else:
                    print("Sorry, I do not understand your input. Please type "
                          "'yes' or 'no'.")
            if display_more.lower() == 'yes':
                head += 5 #Add new 5 rows of data
                tail += 5 #add new 5 rows of data
                print(df[df.columns[0:-1]].iloc[head:tail]) #Print the new 5 rows of data
            elif display_more.lower() == 'no': #if the user says 'no' then break the while loop and get out
                break


def program(): #The Main funtion that holds all operations
    #Get some quick info about the city and period he selected
    # Filter by city (Chicago, New York, Washington)
    city = select_city()
    print('Please Wait ...')
    df = pd.read_csv(city, parse_dates = ['Start Time', 'End Time']) #Open the file of city user selected
    new_labels = []
    for col in df.columns: #go through all columns
        new_labels.append(col.replace(' ', '_').lower()) #make all rows in lowercase and all spaces with underscore for easy access the data
    df.columns = new_labels #new columns name in a list called new_lables    
    # increases the column width so that the long strings in the 'journey'
    # column can be displayed fully
    pd.set_option('max_colwidth', 100)
    #To get most popular journy we will add journey column that takes data from start_station and end_station
    df['journey'] = df['start_station'].str.cat(df['end_station'], sep=' to ')
    time_period = ask_period() #Ask for Period
    if time_period == 'none': #if no filter
        df_filtered = df
    elif time_period == 'month' or time_period == 'day':
        if time_period == 'month':
            filter_lower, filter_upper = ask_month()
        elif time_period == 'day':
            filter_lower, filter_upper = ask_day()
        print('Filtering data...')
        df_filtered = df[(df['start_time'] >= filter_lower) & (df['start_time'] < filter_upper)]
    print('\nCalculating ...')
    if time_period == 'none':
        start_time = time.time() #Save current time before execution        
        # get the most popular month
        popular_month(df_filtered)
        print("That took %s seconds." % (time.time() - start_time)) #print the current time - time before execution then we get time it took
        print("\nCalculating ...")    
    if time_period == 'none' or time_period == 'month':
        start_time = time.time() #Save current time before execution        
        # get the most popular day
        popular_day(df_filtered)
        print("That took %s seconds." % (time.time() - start_time)) #print the current time - time before execution then we get time it took
        print("\nCalculating ...")    
        start_time = time.time() #Save current time before execution
    # get the most popular hour
    popular_hour(df_filtered)
    print("That took %s seconds." % (time.time() - start_time)) #print the current time - time before execution then we get time it took
    print("\nCalculating ...")
    start_time = time.time() #Save current time before execution
    # get the total journy duration and average journy duration
    trip_duration(df_filtered)
    print("That took %s seconds." % (time.time() - start_time)) #print the current time - time before execution then we get time it took
    print("\nCalculatin ...")
    start_time = time.time() #Save current time before execution
    # get the most popular start station and most popular end station
    popular_stations(df_filtered)
    print("That took %s seconds." % (time.time() - start_time)) #print the current time - time before execution then we get time it took
    print("\nCalculating ...")
    start_time = time.time() #Save current time before execution
    # get the most popular journy
    popular_journy(df_filtered) 
    print("That took %s seconds." % (time.time() - start_time)) #print the current time - time before execution then we get time it took
    print("\nCalculating ...")
    start_time = time.time() #Save current time before execution
    # get the counts of user type
    users(df_filtered)
    print("That took %s seconds." % (time.time() - start_time)) #print the current time - time before execution then we get time it took    
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        print("\nCalculating statistic...")
        start_time = time.time() #Save current time before execution        
        # get the counts of gender
        gender(df_filtered)
        print("That took %s seconds." % (time.time() - start_time)) #print the current time - time before execution then we get time it took
        print("\nCalculating ...")
        start_time = time.time() #Save current time before execution
        # get tge birth years info "min,max,most popular"
        birth_years(df_filtered)
        print("That took %s seconds." % (time.time() - start_time)) #print the current time - time before execution then we get time it took
    # if the user selected that he want to see data in table then view 5 rows
    display_data(df_filtered)
    # If the user wants to select new Data filters
    restart = input('\nWould you like to restart? [yes , no]')
    while restart.lower() not in ['yes', 'no']: # if user tyed another value than yes and no
        print("Invalid input. Please type 'yes' or 'no'.")
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes': #if user typed yes then run the program again
        program()



if __name__ == "__main__":
	program() #start the program with this function to let the user choose city and other filters
