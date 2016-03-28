from api_utilities import closest, most_common, debug_print, remove_duplicates
from math import pow, sqrt
from parameters import ALGO
from numpy import array as NumpyArray
from sklearn.cluster import AffinityPropagation, MeanShift, estimate_bandwidth, KMeans
from sklearn import metrics

def get_accuracy(clusters, target, closest_found):
    #Calculates factor based on clusters found.
    mc_clusters = most_common(clusters)
    factor= float(clusters.count(mc_clusters)) / len(clusters)
    #Adds up to the target - closest_found difference    
    accuracy = 100*factor*(1 - abs( float((target - closest_found)) / target ))
    return accuracy

def get_cluster_wakeup(data_obj, wake_up):
    """ Returns the clusters where the wakeup time is the closest wake up 
        time to the wake up time of the current day. It also returns an 
        accuracy depending on various factors such as the gap between 
        the wake up time of today and the closest one found in the data.
    """
    clusters = []
    closest_wake_up = closest([obj["wake_up"] for obj in data_obj[:-1]],
                              wake_up)
    for obj in data_obj[:-1]: #-1 not to include present day
        if obj["wake_up"] == closest_wake_up:
            clusters.append(obj["cluster"])
    accuracy = get_accuracy(clusters, wake_up, closest_wake_up)
    return clusters, accuracy

def get_cluster_duration(data_obj, sleep_duration):
    """ Returns the clusters where the sleep duration is the closest sleep 
        duration to the sleep duration of the current day. It also returns an 
        accuracy depending on various factors such as the gap between 
        the sleep duration of today and the closest one found in the data.
    """
    clusters = []
    closest_sleep_duration = closest([obj["sleep_duration"] for obj in data_obj[:-1]],
                                     sleep_duration)
    for obj in data_obj[:-1]: #-1 not to include present day
        if obj["sleep_duration"] == closest_sleep_duration:
            clusters.append(obj["cluster"])      
    accuracy = get_accuracy(clusters, sleep_duration, closest_sleep_duration)
    return clusters, accuracy

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
    debug_print("Cluster containing same wake up: " + str(clusters_wakeup))
    debug_print("Wake up accuracy: " + str(accuracy1))
    debug_print("Cluster containing same sleep duration: " + str(clusters_sleepduration))
    debug_print("Sleep duration accuracy: " + str(accuracy2))
    accuracy = 0.5*(accuracy1+accuracy2)
    debug_print("Overall accuracy: " + str(int(accuracy)) + "%")
    if clusters_sleepduration == [] and clusters_wakeup == []:
        return None
    if clusters_sleepduration == []:
        return most_common(clusters_wakeup)[0]
    if clusters_wakeup == []:
        return most_common(clusters_sleepduration)[0]
    clusters = []
    for i in range(len(clusters_wakeup)):
        for j in range(len(clusters_sleepduration)):
            if clusters_wakeup[i] == clusters_sleepduration[j]:   
                clusters.append(clusters_wakeup[i])        
    if len(clusters) == 0:
        return most_common(clusters_wakeup + clusters_sleepduration)[0]
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
    points[0] = [data_obj[0]["wake_up"],
                 data_obj[0]["sleep_duration"],
                 86400 - data_obj[0]["sleep_duration"] + data_obj[0]["wake_up"], #wake up minus 7 hours of sleep for first day
                 data_obj[0]["activity"]]
    for i in range(1,L):
        points[i] = [data_obj[i]["wake_up"],
                     data_obj[i]["sleep_duration"],
                     data_obj[i-1]["sleep"],
                     data_obj[i]["activity"]]
    coeff =[3, 3, 3, 0.25]#different weights for each parameter
    dist_e = [[None for _ in range(L)] for _ in range(L)]
    for i in range(L):
        for j in range(L):
            acc = 0
            for k in range(len(coeff)):
                acc += coeff[k] * pow(points[i][k] - points[j][k], 2)
            dist_e[i][j] = - sqrt( acc ) / 10000
    return dist_e

def best_day_cluster(data_obj, cluster_now):
    #Finds day with best sleep quality within the cluster
    maxi = -1
    for i in range(len(data_obj)):
        if data_obj[i]["cluster"] == cluster_now:
            if data_obj[i]["sleep_quality"] > maxi:
                maxi = data_obj[i]["sleep_quality"] 
                best_day = data_obj[i]
    best_day["coffees"] = [t_coffee % 86400 for t_coffee in best_day["coffees"]]
    return best_day

def clusterise_data(data_obj):
    """ Assigns a cluster label to each days present in the data received 
        using three different algorithms: MeanShift, Affinity Propagation, 
        or KMeans. 
        @param data_obj: List of dictionaries
    """
    L = len(data_obj)
    
    #Simply converts data_obj to a 2D list for computation
    List2D = [[None for _ in range(4)] for _ in range(L-1)]
    for i in range(L-1): #don't include current day
        #wake_up and sleep_duration are the most important factors
        List2D[i][0] = 5 * data_obj[i]["wake_up"]
        List2D[i][1] = 1 * data_obj[i]["sleep"]
        List2D[i][2] = 5 * data_obj[i]["sleep_duration"]
        List2D[i][3] = 0.5 * data_obj[i]["activity"]
    points = NumpyArray(List2D) #converts 2D list to numpyarray
        
    if ALGO == "Affinity Propagation":
        labels = AffinityPropagation().fit_predict(points)
    elif ALGO == "KMeans":
        labels= KMeans(init='k-means++', n_clusters=5, n_init=10)   .fit_predict(points)
    elif ALGO == "MeanShift":
        bandwidth = estimate_bandwidth(points, quantile=0.2, n_samples=20)
        labels = MeanShift(bandwidth=bandwidth, bin_seeding=True).fit_predict(points)
    else:
        raise Exception("Algorithm not defined: "+str(ALGO))
        
    for i in range(L-1):
        data_obj[i]["cluster"] = labels[i]
    for unique_label in remove_duplicates(labels):
        debug_print(ALGO+": Cluster "+str(unique_label)+" contains "+str(labels.tolist().count(unique_label))+" data points")
    debug_print(ALGO+": Silhouette coefficient"+ str(metrics.silhouette_score(points, labels, metric='euclidean')*100)+"%")
        
def evaluate_clusters(data_obj_all):
    default_dict = dict()
    default_dict["wake_up"] = "undefined"
    default_dict["activity"] = "undefined"
    default_dict["sleep"] = "undefined"
    default_dict["sleep_duration"] = "undefined"
    labels = remove_duplicates([data_obj_all[i]["cluster"] for i in range(len(data_obj_all)-1)])
    for L in labels: #number of clusters
        debug_print("~~~~ FOR CLUSTER "+str(L)+" ~~~~")
        data_obj = []
        for obj in data_obj_all:
            if obj["cluster"] == L:
                data_obj.append(obj)        
        classifier = [default_dict for _ in range(len(data_obj))]
        for i in range(len(data_obj)):
            if data_obj[i]["wake_up"] >= 36000:
                classifier[i]["wake_up"] = "Late"
            elif data_obj[i]["wake_up"] <= 26000:
                classifier[i]["wake_up"] = "Early"    
            else:    
                classifier[i]["wake_up"] = "Average"
                
            if data_obj[i]["activity"] == 0:
                classifier[i]["activity"] = "Unactive"
            else:
                classifier[i]["activity"] = "Activity"

            if data_obj[i]["sleep"] <= 82000:
                classifier[i]["sleep"] = "Early"
            else:
                classifier[i]["sleep"] = "Late"

            if data_obj[i]["sleep_duration"] <= 28000:
                classifier[i]["sleep_duration"] = "Short"
            else:
                classifier[i]["sleep_duration"] = "Long"
            debug_print(str(classifier[i]))
