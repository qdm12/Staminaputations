from sys import maxint

def average_sleep(data_obj, cluster):
    t_day_start = (data_obj[-1]["wake_up"] / 86400)*86400
    i = 0
    acc = 0
    for obj in data_obj:
        if obj["cluster"] == cluster:
            temp = obj["sleep"] % 86400
            if temp < 43200:
                temp += 86400 #if the user goes to sleep the morning (before 12am)
            acc += temp
            i += 1
    return t_day_start + acc / i

def average_activity(data_obj, cluster):
    t_day_start = (data_obj[-1]["wake_up"] / 86400)*86400
    i = 0
    acc = 0
    for obj in data_obj:
        if obj["cluster"] == cluster:
            if obj["activity"] != 0:
                temp = obj["activity"] % 86400
                acc += temp
                i += 1
    if i == 0: #No activity in cluster
        return 0 #XXX to do in app
    return t_day_start + acc / i

def most_common(data):
    L = len(data)
    common = dict()
    for d in data:
        common[d] = 1
    done = []
    for i in range(L):
        if (i not in done):
            for j in range(L):
                if (j not in done) and (i != j) and (data[i] == data[j]):
                    common[data[i]] += 1
                    done.append(j)
        done.append(i)
    maxi = -1
    for d, occurences in common.iteritems():
        if occurences > maxi:
            maxi = occurences
            mc = d
    most_commons = [mc]
    for d, occurences in common.iteritems():
        if (occurences == maxi) and (d != mc):
            most_commons += [d]     
    return most_commons

def remove_duplicates(data):
    temp = dict()
    for d in data:
        temp[d] = 0
    return [key for key in temp.iterkeys()]

#Finds closest element in a list to a given number
def closest(data, x):
    bound = maxint
    for i in range(len(data)):
        diff = abs(data[i] - x)
        if diff < bound:
            bound = diff
            closest = data[i]
    return closest