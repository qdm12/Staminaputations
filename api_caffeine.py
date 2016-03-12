from math import exp, log
from parameters import cup_caffeine, half_life
  
def get_caffeine(seconds):
    """ Returns the mg of caffeine after seconds elapsed since the 
        drink of a coffee. Based on the half life of elimination of caffeine.
        @param seconds: int
        @return: int
        @raise TypeError 
    """
    if type(seconds) is not int:
        raise TypeError("seconds must be an integer.")
    if seconds < 0:
        return 0 #This is for coffee not taken yet (in the future).
    if seconds == 0:
        return cup_caffeine
    return int(cup_caffeine * exp(seconds * log(0.5)/half_life))

def get_time(caffeine):
    """ Returns the seconds elapsed corresponding to the given level 
        of caffeine after the drink of a coffee.
        @param caffeine: int
        @return: int
        @raise TypeError 
    """
    if type(caffeine) is not int:
        raise TypeError("caffeine must be an integer representing the mg of caffeine.")
    if caffeine < 0:
        raise ValueError("caffeine must be positives")
    caffeine = float(caffeine)
    if caffeine == cup_caffeine:
        return 0 #0 seconds have elapsed.
    if caffeine == 0:
        caffeine = 1 #1mg is the same as 0.1mg of caffeine in real life...
    return int(half_life/log(0.5) * log(float(caffeine)/cup_caffeine))

def get_caffeine_multi(t, t_coffees):
    """ Returns the caffeine level at timestamp t given the list of timestamps
        t_coffees where the user drank coffee in the past. All the timestamps 
        are using epoch time in seconds. 
        @param t: int
        @param t_coffees: list of int 
        @return: int
        @raise TypeError, ValueError 
    """
    if type(t) is not int:
        raise TypeError("t must be an integer.")
    if type(t_coffees) is not list:
        raise TypeError("t_coffees must be a list.")
    if len(t_coffees) == 0:
        return 0 #If no coffee(s) were drunk, there is no caffeine
    for temp in t_coffees:
        if type(temp) is not int:
            raise TypeError("t_coffees must contain integers only.")
    caffeine = 0
    for i in range(len(t_coffees)):
        caffeine += get_caffeine(t - t_coffees[i])
    return caffeine


def get_latest_t_coffee(t_coffees, caffeine_sleep, t_sleep):
    """ Returns the latest possible timestamp where a coffee could be drunk
        without having the caffeine level higher than recommended at sleep time.
        Takes into account the list of timestamps of coffees, the recommended 
        level of caffeine to sleep and the expected sleep timestamp.
        @param t_coffees: list of int (epoch)
        @param caffeine_sleep: int
        @param t_sleep: int (epoch)
        @param t_coffee_interval: int
        @return: int (epoch)
        @raise TypeError, ValueError 
    """
    if type(t_coffees) is not list:
        raise TypeError("t_coffees must be a list.")
    if len(t_coffees) == 0:
        return 0 #If no coffee(s) were drunk, there is no caffeine
    for temp in t_coffees:
        if type(temp) is not int:
            raise TypeError("t_coffees must contain integers only.")
    if type(caffeine_sleep) is not int:
        raise TypeError("caffeine_sleep must be an integer representing the mg of caffeine.")
    if caffeine_sleep < 0:
        raise ValueError("caffeine_sleep must be positive.")
    if type(t_sleep) is not int:
        raise TypeError("t_sleep must be an integer representing the time of sleep (epoch).")
    t_now = t_coffees[-1] #As the present time is always the last coffee for higher layers
    t_virtual_step = 60 #checks for each minute XXXXX check if too slow
    for t_virtual in range(t_sleep, t_now, -t_virtual_step):
        if get_caffeine_multi(t_sleep, t_coffees + [t_virtual]) < caffeine_sleep:
            return t_virtual
    return -1 # Not possible to drink coffee anymore