###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    txt_file = open(str(filename), 'r') #open txt file
    cows = {} #create an empty dictionary
    
    for line in txt_file: #for each line in the file, 
        cows[str(line).split(',')[0]] = int(line.split(',')[1][0]) 
        #separate the name and the weight, change the weight type into integer 
        #and store it as a key - value pair in dictionary
    
    return cows

cows = load_cows('ps1_cow_data.txt')

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    dopoki list wag nie jest pusta, 
    """
    cows_copy = cows.copy() #copy of a dictionary
    trips = [] #list of trips
    while len(cows_copy) > 0: #while there's still a cow to transport
        used_weight = 0
        trip = []
        for weight in sorted(list(cows_copy.values()), reverse=True): #iterate over the sorted list of weights
            if weight + used_weight <= limit: #if there is still a place for a given weight
                used_weight += weight #let it on board
                for k, v in cows_copy.items():
                    if v == weight and k not in trip: #find the cow with the given weight that has not embarked yet
                        trip.append(k) #add her name to the trip
                        break
                
        for name in trip:
            cows_copy.pop(name) #delete the cows from last trip from the dictionary
        trips.append(trip) #append the trip to the list of trips
    return trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cows_copy = cows.copy()
    cows_names = list(cows_copy.keys()) #create the list of cows names
    partitions = []
    for partition in get_partitions(cows_names): #create the list of possible partitions
        partitions.append(partition)
    
    sets_of_trips = sorted(partitions, key=len) #sorts the partitions ascending
    optimum = []
    while len(optimum) == 0: #until there's no optimum found
        for set_of_trips in sets_of_trips: 
            for trip in set_of_trips:
                weight = sum([cows_copy[name] for name in trip]) #calculate the sum of each trip in a partition
                if weight > limit: #if one of them is over the limit
                    break
                if trip == set_of_trips[-1]: #if the trip is the last one in the set and we got to this point it means we've found the optimum
                    optimum = set_of_trips
                    break
            if len(optimum) > 0: #double-loop escape
                break
            
    return optimum
        
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start_greedy = time.time()
    result_greedy = greedy_cow_transport(cows)
    end_greedy = time.time()
    print('Number of trips returned by greedy algorithm: ', len(result_greedy))
    print('Time it took to find the result for greedy algorithm:', end_greedy - start_greedy)
    
    start_brute = time.time()
    result_brute = brute_force_cow_transport(cows)
    end_brute = time.time()
    print('Number of trips returned by greedy algorithm: ', len(result_brute))
    print('Time it took to find the result for brute force algorithm:', end_brute - start_brute)