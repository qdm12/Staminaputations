from api_csv import CSV
from time import time
from sys import argv
from json import loads as JsonLoads
from parameters import DEBUG

def read_data():
    if DEBUG:
        present = 1460639800
        command = "is_last_coffee"
        data_matrix = CSV("data.csv").read_data_rows()
        data_obj = objectise_matrix(data_matrix)
    else:
        present = int(time())
        command = argv[1]
        data_json = JsonLoads(argv[2])
        data_obj = objectise_json(data_json)
    return present, command, data_obj

def epoch2seconds(epoch):
    if epoch == 0:
        return 0
    x = epoch % 86400
    if x == 0:
        return 86400
    if x < 3600*4: #to do 
        return x + 86400
    return x

def objectise_matrix(data_matrix):
    """ This takes a 2D list and uses it as a source to create a list of 
        dictionaries as follows.
        @param data_matrix: list of list of strings
        @return: list of dict
        @raise TypeError 
    """
    if type(data_matrix) is not list:
        raise TypeError("data_matrix has to be a list.")
    L = len(data_matrix)
    if L == 0:
        raise TypeError("data_matrix can't be empty.")
    for d in data_matrix:
        if type(d) is not list:
            raise TypeError("data_matrix[i] have to be lists.")
        for e in d:
            if type(e) is not str:
                raise TypeError("data_matrix[i][j] have to be strings.")
    data_obj = []
    for i in range(L):
        obj = dict();
        obj["sleep_quality"] = int(data_matrix[i][0])
        obj["coffees"] = map(int, data_matrix[i][2].split('#')) #list of timestamps epoch
        obj["activity"] = epoch2seconds(int(data_matrix[i][3]))
        obj["cluster"] = None
        if i == 0: #for the first day
            obj["sleep_duration"] = 8 * 60 * 60 #8 hours of sleep default
        else:
            obj["sleep_duration"] = int(data_matrix[i][1]) - int(data_matrix[i-1][4])
        if i < L - 1:
            obj["sleep"] = epoch2seconds(int(data_matrix[i][4]))
        obj["wake_up"] = epoch2seconds(int(data_matrix[i][1]))
        data_obj.append(obj)
    return data_obj

           
def objectise_json(data_json):
    """ This takes a JSON data structure and uses it as a source to create a 
        list of dictionaries as follows.
        @param data_matrix: list of list of strings
        @return: list of dict
        @raise TypeError 
    """
    L = len(data_json)
    if L == 0:
        raise TypeError("data_json can't be empty.")
    data_obj = []
    for i in range(L):
        obj = dict();
        obj["sleep_quality"] = int(data_json[i]['wakeup']['quality'])
        obj["coffees"] = []
        for j in range(len(data_json[i]['coffee'])):
            obj["coffees"].append(int(data_json[i]['coffee'][j]['time']))
        obj["activity"] = epoch2seconds(int(data_json[i]['activity'][0]['start']))
        obj["cluster"] = None
        if i == 0: #for the first day
            obj["sleep_duration"] = 8 * 60 * 60 #8 hours of sleep default
        else:
            obj["sleep_duration"] = int(data_json[i]['wakeup']['time']) - int(data_json[i-1]["sleep"]["time"])        
        if i < L - 1:
            obj["sleep"] = epoch2seconds(int(data_json[i]['sleep']['time']))
        obj["wake_up"] = epoch2seconds(int(data_json[i]['wakeup']['time']))
        data_obj.append(obj)
    return data_obj