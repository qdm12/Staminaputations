from math import exp, log

#CONSTANT
cup_caffeine = 88 #88mg average
half_life = 5*60 #240 minutes

#MACHINE LEARNING
caffeine_sleep = 50 #50mg

class SleepException(Exception):
    pass

def frange(a, b, step):
    while a < b:
        yield a
        a += step
  
def get_caffeine(t):
    """ Get the mg of caffeine t minutes after one coffee is taken
        Params
            t: int (minutes)
        Returns
            caffeine: float (mg)
        Raises
            TypeError, ValueError    
    """
    if type(t) not in (int, float):
        raise TypeError("t must be an int or a float.")
    elif t < 0:
        raise ValueError("t must be positive.")
    elif t==0:
        return 0
    else:
        return cup_caffeine * exp(t * log(0.5)/half_life)

def get_time(caffeine):
    """ Get the minutes needed to be elapsed after one coffee taken to reach the caffeine level given.
        Params
            caffeine: float (mg)
        Returns
            t: int (minutes)
        Raises
            TypeError, ValueError    
    """
    if type(caffeine) not in (int, float):
        raise TypeError("caffeine must be an int or a float.")
    elif caffeine < 0:
        raise ValueError("caffeine must be positive.")
    elif caffeine==0:
        caffeine = 0.1 
    return 1/(log(0.5)/half_life) * log(float(caffeine)/cup_caffeine)

def get_caffeine_multi(H, coffee_list):
    """ Get the minutes needed to be elapsed after one coffee taken to reach the caffeine level given.
        Params
            H: float (hour)
            coffee_list: list of floats (hours when coffee were taken)
        Returns
            caffeine: float (mg)
        Raises
            TypeError, ValueError    
    """
    if type(H) not in (int, float):
        raise TypeError("H must be an int or a float.")
    elif type(coffee_list) is not list:
        raise TypeError("coffee_list must be a list.")
    elif type(coffee_list[0]) not in (int, float):
        raise TypeError("Elements of coffee_list must be an int or a float.")
    elif H < 0:
        raise ValueError("H must be positive.")
    temp = coffee_list[:]
    for i in range(len(temp)):
        if temp[i] == H:
            temp[i] = H-0.00001
        elif temp[i] > H:
            temp[i] = H #To give 0 for future intakes relative to H
    caffeine = 0
    for i in range(len(temp)):
        caffeine += get_caffeine((H - temp[i])*60)
    return caffeine

def get_caffeine_multi_all(present, coffee_list, step=15):
    """ Get the minutes needed to be elapsed after one coffee taken to reach the caffeine level given.
        Params
            present: float (hour)
            coffee_list: list of floats (hours when coffee were taken)
            step: int (minutes)
        Returns
            caffeine: float (mg)
        Raises
            TypeError, ValueError    
    """
    if type(present) not in (int, float):
        raise TypeError("H must be an int or a float.")
    if type(coffee_list) is not list:
        raise TypeError("coffee_list must be a list.")
    elif type(coffee_list[0]) not in (int, float):
        raise TypeError("Elements of coffee_list must be an int or a float.")
    elif present < 0:
        raise ValueError("H must be positive.")
    times = [H for H in frange(0,present,float(step)/60)]
    caffeines = [get_caffeine_multi(H,coffee_list) for H in times]
    return [times,caffeines]

def get_ReadyToSleep_time(coffee_list):
    """ Get the hour where the caffeine level will be lower than the sleep level, depending on the coffees taken.
        Params
            coffee_list: list of floats (hours when coffee were taken)
        Returns
            H: float (hour)
        Raises
            TypeError, ValueError    
    """
    if type(coffee_list) is not list:
        raise TypeError("coffee_list must be a list.")
    elif type(coffee_list[0]) not in (int, float):
        raise TypeError("Elements of coffee_list must be an int or a float.")
    step = 0.25 #0.25 hour = 15 minutes
    for H in frange(20,30,step): #From 8PM to 6AM
        if get_caffeine_multi(H, coffee_list) < caffeine_sleep:
            return H
    raise SleepException("You won't be able to fall asleep this night :(")

def test():
    time = 15
    caffeine = get_caffeine(time) #Minutes
    time = get_time(caffeine)
    print str(time)+" minutes after first coffee, you have "+str(caffeine)+"mg of caffeine."
    print "For "+str(caffeine)+"mg of caffeine, you have taken a coffee "+str(time)+" minutes ago."
    coffee_timestamps = [7.5, 12, 15]
    time = 7.5 #HOURS (from 0 to 26 etc.)
    caffeine = get_caffeine_multi(time, coffee_timestamps) #Hours
    print "If you drunk coffees at H="+str(coffee_timestamps)+" you would have "+str(caffeine)+"mg of caffeine at "+str(time)+"H"
    time = get_ReadyToSleep_time(coffee_timestamps)
    print "You will be able to sleep from "+str(time)+"H"
    print get_caffeine_multi_all(16,coffee_timestamps)
    
test()