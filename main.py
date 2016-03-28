from api_data import read_data
from parameters import DEBUG
from api_caffeine import get_caffeine_multi, get_latest_t_coffee
from api_utilities import average_sleep, average_activity, debug_print
from api_clustering import get_cluster, best_day_cluster, evaluate_clusters, \
                            clusterise_data


present, command, data_obj = read_data()
clusterise_data(data_obj) #Sets a cluster number to each day

if DEBUG:
    evaluate_clusters(data_obj)


cluster_now = get_cluster(data_obj)
if cluster_now is None:
    debug_print("No cluster found !") # Should never go here


# Finds the expected sleep time for the current day    
t_sleep_expected = average_sleep(data_obj, cluster_now)
debug_print("Expected sleep time: " + str(t_sleep_expected))


# Finds the day wit the best sleep quality in the cluster of today
best_day = best_day_cluster(data_obj, cluster_now)
debug_print("The day with the best sleep quality in the cluster: " + str(best_day))


#Finds the corresponding caffeine threshold at sleep time during this best day
suggested_sleep_caffeine = get_caffeine_multi(best_day["sleep"],
                                              best_day["coffees"])             
debug_print("Associated sleep caffeine level: " + str(suggested_sleep_caffeine))



# Treats the request from the NodeJS servr
if command == "expected_activity": 
    # Returns the epoch timestamp of the expected physical activity.
    # This should only be asked when the user wakes up.
    expected_activity = average_activity(data_obj, cluster_now)
    debug_print("expected_activity = "+str(expected_activity))
    print expected_activity # to communicate with NodeJS


elif command == "can_he_drink":
    # Returns yes, no or last to answer the question can_he_drink
    # This should be triggered when the user enters a coffee zone.
    t_coffees_virtual = data_obj[-1]["coffees"] + [present]
    sleep_caffeine = get_caffeine_multi(t_sleep_expected, t_coffees_virtual)
    debug_print("sleep_caffeine = "+str(sleep_caffeine))
    if sleep_caffeine > suggested_sleep_caffeine:
        debug_print("can_he_drink = no")
        print "no" # to communicate with NodeJS
    else:
        t_latest_coffee = get_latest_t_coffee(t_coffees_virtual,
                                              suggested_sleep_caffeine,
                                              t_sleep_expected)
        if t_latest_coffee < 0:
            debug_print("can_he_drink = no") #should never come here but who knows
            print "no" # to communicate with NodeJS
        else:
            remaining_coffee_duration = t_latest_coffee - present
            debug_print("Minutes left before last possible coffee: " \
                        + str(remaining_coffee_duration / 60))
            if remaining_coffee_duration < 6000: #6000 seconds
                debug_print("can_he_drink = last")
                print "last" # to communicate with NodeJS
            else:
                debug_print("can_he_drink = yes")
                print "yes" # to communicate with NodeJS
                
                
elif command == "is_last_coffee":
    # Returns yes or no to answer the question is_last_coffee
    # This should be triggered when the user was detected to drink a coffee.
    t_latest_coffee = get_latest_t_coffee(data_obj[-1]["coffees"],
                                          suggested_sleep_caffeine,
                                          t_sleep_expected)
    remaining_coffee_duration = t_latest_coffee - present
    debug_print("Hours left before last possible api_caffeine: " + str(float(remaining_coffee_duration)/3600))
    if remaining_coffee_duration < 6000: #6000 seconds
        debug_print("is_last_coffee = yes")
        print "yes"
    else:
        debug_print("is_last_coffee = no")
        print "no"
else:
    print "undefined_command"
# EOF