
from datetime import datetime, time

#Check if the current time is between supplied start and end times
#https://stackoverflow.com/questions/10048249/how-do-i-determine-if-current-time-is-within-a-specified-range-using-pythons-da

def is_time_between(begin_time, end_time):
    # If check time is not given, default to current time
    check_time = datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time