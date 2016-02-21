from api_csv import CSV
from coffee import get_caffeine_multi
from reinforce import learn


#MACHINE LEARNING
half_life = 5*60 #300 minutes
caffeine_sleep = 50 #50mg
sleep_time=22
csv = CSV("data1.csv")
M2D = csv.read_data_rows()
threshold=70.0
sleep_quality =[float(M2D[i][1]) for i in range(len(M2D))]
day = [M2D[i][0] for i in range(len(M2D))]
first_coffees = [float(M2D[i][2])  for i in range(len(M2D))]
second_coffees = [float(M2D[i][3])  for i in range(len(M2D))]
third_coffees = [float(M2D[i][4])  for i in range(len(M2D))] 

states = day[:]
caffeine = [get_caffeine_multi(sleep_time,
                               [first_coffees[i],
                                second_coffees[i],
                                third_coffees[i]]
                               ) for i in range(len(states))]



rewards = sleep_quality[:]
action = [None for i in range(len(states))]
for i in range(len(sleep_quality)):
    if sleep_quality[i] > threshold:
        rewards[i]=1
    else: rewards[i]=0
print rewards
         
for i in range(len(states)):
    if caffeine[i] < 10:
        action[i] = "10"
    elif caffeine[i] < 20:
        action[i] = "20"
    elif caffeine[i] < 30:
        action[i] = "39"
    elif caffeine[i] < 40:
        action[i] = "40"
    elif caffeine[i] < 50:
        action[i] = "50"
    elif caffeine[i] < 60:
        action[i] = "60"
    elif caffeine[i] < 70:
        action[i] = "70"
    elif caffeine[i] < 80:
        action[i] = "80"
    elif caffeine[i] < 90:
        action[i] = "90"
    else:
        action[i]="100"                      

nb_weeks = (len(states)+1)/7
week = [None for i in range(nb_weeks)]
for i in range(nb_weeks):
    week[i] = [[states[j], action[j], rewards[j]] for j in range(i*7,(i+1)*7-1)]
for i in range(nb_weeks):    
    print week[i][0]
print week    
gamma=0.6
model = learn(week,gamma)
print caffeine
print ("From these five paths, the learned strategy is: ")
print (model)
print 