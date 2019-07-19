"""
Dictionary that contains all the info of the subsciber of the service
"""

import datetime

subscriber = {
            'name' : 'user_iot',
            'start_day_time' : datetime.time(9,0,0,0),  # the hour after the script can run
            'end_day_time' : datetime.time(17,0,0,0)    # the hour before the script can run
            }

if __name__ == "__main__":
    current_time = datetime.time(14,0,0,0)

    if current_time > subscriber['start_day_time'] and current_time < subscriber['end_day_time']:
        print("working")
    else:
        print("resting")