# Staminaputations: Machine learning for Smarter coffee consumption

##### What is it?
This program composes the machine learning and data processing program of the back-end of Stamina.
It is executed from a NodeJS webserver from the module main.py.
##### Inputs
It takes as input daily records of  past coffee consumption, wake up time, sleep time, physical activity time, sleep duration and sleep quality. 
##### Computations
The machine learning called clustering (Affinity Propagation, or KMeans or MeansShift algorithm) is performed on all the past days. Once the days are clustered, the program searches for the most appropriate cluster for the current day which only has a sleep duration and a wake up time. From this cluster are then extracted various information such as the expected sleep time or the day with the best quality. There is more information on that in the code and in our report/video.
##### Outputs
Practically, the program answers to the three possible questions in the following way:
- Question: When would I perform my physical activity today according to my previous data? "expected_activity"
    - Answer: Epoch timestamp of predicted expected future physical activity time
- Question: Can I drink a coffee now or will my sleep be compromised? "can_he_drink"
    - Answer: "yes", "no" or "last" meaning that you can drink your last coffee for today.
- Question: Is the coffee I am drinking now my last coffee for today? "is_last_coffee"
    - Answer: "yes" or "no"

##### Requirements
This program requires (install in this order):
- Python 2.7
- numpy 1.10.4
- scipy 0.17.0
- scikit-learn 0.17

Python has to be installed and the other libraries can then be installed with 
>> pip install numpy scipy sklearn scikit-learn
