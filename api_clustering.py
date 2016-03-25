from api_utilities import closest, most_common, remove_duplicates
from math import pow, sqrt
from parameters import DEBUG
    
def get_accuracy(clusters, target, closest_found):
    
    #Calculates factor based on clusters found.
    mc_clusters = most_common(clusters)
    
    M = clusters.count(mc_clusters[0]) #same for all mc_cluster
    N = len(clusters)
    
    P = len(mc_clusters)
    Q = len(remove_duplicates(clusters))
    
    MN = pow(float(N - M + 1) / N, 2)
    PQ = float(P) / Q
    factor = PQ * MN

    #Adds up to the target - closest_found difference    
    accuracy = 100*factor*(1 - abs( float((target - closest_found)) / target ))
    return accuracy


#Returns cluster indices that contain same wake up time in day_t 
def get_cluster_wakeup(data_obj, wake_up):
    clusters = []
    closest_wake_up = closest([obj["wake_up"] for obj in data_obj[:-1]],
                              wake_up)
    for obj in data_obj[:-1]: #-1 not to include present day
        if obj["wake_up"] == closest_wake_up:
            clusters.append(obj["cluster"])
    accuracy = get_accuracy(clusters, wake_up, closest_wake_up)
    return clusters, accuracy



#Returns cluster indices that contain same sleep duration in day_t
def get_cluster_duration(data_obj, sleep_duration):
    clusters = []
    closest_sleep_duration = closest([obj["sleep_duration"] for obj in data_obj[:-1]],
                                     sleep_duration)
    for obj in data_obj[:-1]: #-1 not to include present day
        if obj["sleep_duration"] == closest_sleep_duration:
            clusters.append(obj["cluster"])      
    accuracy = get_accuracy(clusters, sleep_duration, closest_sleep_duration)
    return clusters, accuracy

#Returns clusters that contain elements with same wake up time and same sleep duration
def get_cluster(data_obj):
    """ Finds the right cluster for the current (latest) day given. 
        This takes into account the wake_up and sleep_duration of the current
        day, as this one is not finished yet.
        @param data_obj: List of dictionnaries
        @return: string, most common and suited cluster
    """ 
    L = len(data_obj)
    clusters_wakeup, accuracy1 = get_cluster_wakeup(data_obj, data_obj[L-1]["wake_up"])
    clusters_sleepduration, accuracy2 = get_cluster_duration(data_obj, data_obj[L-1]["sleep_duration"])
    if DEBUG: print "DEBUG: cluster containing same wake up: " + str(clusters_wakeup)
    if DEBUG: print "DEBUG: cluster containing same sleep duration: " + str(clusters_sleepduration)
    accuracy = 0.5*(accuracy1+accuracy2)
    if DEBUG: print "DEBUG: Overall accuracy: " + str(int(accuracy)) + "%"
    if clusters_sleepduration is None and clusters_wakeup is None:
        return None
    if clusters_sleepduration is None:
        return most_common(clusters_wakeup)[0]
    if clusters_wakeup is None:
        return most_common(clusters_sleepduration)[0]
    clusters=[]
    for i in range(len(clusters_wakeup)):
        for j in range(len(clusters_sleepduration)):
            if clusters_wakeup[i] == clusters_sleepduration[j]:   
                clusters.append(clusters_wakeup[i])        
    if len(clusters) == 0:
        return most_common(clusters_wakeup+clusters_sleepduration)[0]
    return most_common(clusters)[0]


def euclidian_dist(data_obj):
    """ Calculates the N(N-1) Euclidian distances for N days. 
        This takes into account the wake_up, sleep_duration, sleep
        and activity times. 
        @param data_obj: List of dictionnaries
        @return: dist_e: 2D Matrix (list) of euclidian distances.
    """ 
    L = len(data_obj)
    points = [[] for _ in range(L)]
    for i in range(L):      
        points[i] = [data_obj[i]["wake_up"],
                     data_obj[i]["sleep_duration"],
                     data_obj[i-1]["sleep"],
                     data_obj[i]["activity"]]
    coeff = [3, 3, 2, 1.5] #different weights for each parameter
    dist_e = [[None for _ in range(L)] for _ in range(L)]
    for i in range(L):
        for j in range(L):
            acc = 0
            for k in range(len(coeff)):
                acc += coeff[k] * pow(points[i][k] - points[j][k], 2)
            dist_e[i][j] = - sqrt( acc ) / 10000
    return dist_e

#Finds day with best sleep quality within the cluster
def best_day_cluster(data_obj, cluster_now):
    maxi = -1
    for i in range(len(data_obj)):
        if data_obj[i]["cluster"] == cluster_now:
            if data_obj[i]["sleep_quality"] > maxi:
                maxi = data_obj[i]["sleep_quality"] 
                best_day = data_obj[i]
    return best_day

