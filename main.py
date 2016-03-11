from api_csv import CSV
from api_caffeine import get_caffeine_multi, get_latest_t_coffee
from api_utilities import average_sleep, average_activity
from api_clustering import get_cluster, euclidian_dist, best_day_cluster
from sklearn.cluster import AffinityPropagation
from time import time
from sys import argv
import json

DEBUG = False


def objectise_matrix(data_matrix):
    L = len(data_matrix)
    data_obj = []
    for i in range(L):
        obj = dict();
        obj["sleep_quality"] = int(data_matrix[i][0])
        obj["wake_up"] = int(data_matrix[i][1])
        obj["coffees"] = map(int, data_matrix[i][2].split('#')) #list of timestamps epoch
        obj["activity"] = int(data_matrix[i][3])
        obj["sleep"] = int(data_matrix[i][4])
        obj["cluster"] = None
        if i == 0: #for the first day
            obj["sleep_duration"] = 7 * 60 * 60 #7 hours of sleep default
        else:
            obj["sleep_duration"] = obj["wake_up"] - int(data_matrix[i-1][4])
        data_obj.append(obj)
    return data_obj

def objectise_json(data_json):
    L = len(data_json)
    data_obj = []
    for i in range(L):
        obj = dict();
        obj["sleep_quality"] = int(data_json[i].wakeup.quality)
        obj["wake_up"] = int(data_json[i].wakeup.time)
        obj["coffees"] = [int(x.time) for x in data_json.coffee] #map(int, data_json[i].coffee) #list of timestamps epoch
        obj["activity"] = int(data_json[i].activity[0].start)
        obj["sleep"] = int(data_json[i].sleep.time)
        obj["cluster"] = None
        if i == 0: #for the first day
            obj["sleep_duration"] = 7 * 60 * 60 #7 hours of sleep default
        else:
            obj["sleep_duration"] = obj["wake_up"] - int(data_json[i-1].wakeup.time)
        data_obj.append(obj)
    return data_obj


def read_data():
    if DEBUG:
        present = 1460639800
        command = "is_last_coffee"
        csv = CSV("data.csv")
        data_matrix = csv.read_data_rows()
        for row in data_matrix:
            x = len(row)
            if x != 5:
                raise ValueError("The input should contain 5 parameters per row but contains "+str(x)+".")
        data_obj = objectise_matrix(data_matrix)
    else:
        present = int(time())
        command = argv[1]
        data_json = json.loads(argv[2]) # [row.split(',') for row in argv[2].split(';')]
        data_obj = objectise_json(data_json)
    return present, command, data_obj

def clusterise_data(data_obj):
    dist_e = euclidian_dist(data_obj) #PROBLEM
    cluster_labels = AffinityPropagation().fit_predict(dist_e)
    for i in range(len(data_obj)):
        data_obj[i]["cluster"] = cluster_labels[i]
        
        
        



present, command, data_obj = read_data()
clusterise_data(data_obj) #Sets a cluster number to each day
cluster_now = get_cluster(data_obj)



t_sleep_expected = average_sleep(data_obj, cluster_now)
if DEBUG: print "DEBUG: Expected sleep time: " + str(t_sleep_expected)

best_day = best_day_cluster(data_obj, cluster_now)
if DEBUG: print "DEBUG: The day with the best sleep quality in the cluster: " + str(best_day)
suggested_sleep_caffeine = get_caffeine_multi(best_day["sleep"],
                                              best_day["coffees"])             
if DEBUG: print "DEBUG: Associated sleep caffeine level: " + str(suggested_sleep_caffeine)






# SHOULD BE ASKED WITH WAKE_UP EVENT ONLY
if command == "expected_activity": #epoch timestamp
    print average_activity(data_obj, cluster_now) #XXXX do something if NONE !!!
    # cluster_now should be determined without taking into account the activity of today
    # Repetition weekly XXXX to do Alexandra
    
    
    
elif command == "can_he_drink": # yes or no or last
    t_coffees_virtual = data_obj[-1]["coffees"] + [present]
    sleep_caffeine = get_caffeine_multi(t_sleep_expected, t_coffees_virtual)
    if DEBUG: print "DEBUG: sleep_caffeine = "+str(sleep_caffeine)
    if sleep_caffeine > suggested_sleep_caffeine:
        print "no"
    else:
        t_latest_coffee = get_latest_t_coffee(t_coffees_virtual,
                                              suggested_sleep_caffeine,
                                              t_sleep_expected)
        if t_latest_coffee < 0:
            print "no" #should never come here but who knows
        else:
            remaining_coffee_duration = t_latest_coffee - present
            if DEBUG: print "DEBUG: Minutes left before last possible api_caffeine: " + str(remaining_coffee_duration / 60)
            if remaining_coffee_duration < 6000: #6000 seconds
                print "last"
            else:
                print "yes"
            
            
            
elif command == "is_last_coffee": # yes or no
    #api_caffeine was already drunk and user checks if this one was his last one
    t_latest_coffee = get_latest_t_coffee(data_obj[-1]["coffees"],
                                          suggested_sleep_caffeine,
                                          t_sleep_expected)
    remaining_coffee_duration = t_latest_coffee - present
    if DEBUG: print "DEBUG: Hours left before last possible api_caffeine: " + str(float(remaining_coffee_duration)/3600)
    if remaining_coffee_duration < 6000: #6000 seconds
        print "yes"
    else:
        print "no"
else:
    print "undefined command"
        
        
        
# EOF