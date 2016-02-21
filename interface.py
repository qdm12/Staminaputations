import json
from coffee import get_caffeine_multi_all, get_ReadyToSleep_time

def caffeine_day_data(present, coffee_list, step=15):
    data_python = get_caffeine_multi_all(present, coffee_list, step)
    data = json.dumps(data_python)
    with open("json.js","wb") as f:
        f.write(data)
        
def sleep_day_time(coffee_list):
    data_python = get_ReadyToSleep_time(coffee_list)
    data = json.dumps(data_python)
    with open("json.js","wb") as f:
        f.write(data)