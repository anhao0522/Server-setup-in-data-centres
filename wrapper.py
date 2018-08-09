#my python version is 3.6
#to run my code, it should ensure all configuration file (include num_tests.txt) will be
# in the same directory with wrapper.py and type python3 wrapper.py in Terminal on cse system.
# Just run this file then it will read all file and give output.
#Also, for design part, all program is writen under python 3.6
import random
atime_list=[]
stime_list=[]
dtime_list=[]
Lambda=0
Mu=0
m=0

def find_states(L, m):
    l = []
    for i in range(len(L)):
        if L[i] == m:
            l.append(i)
    return l


def which_selected(L, target):
    l = []
    for x in L:
        l.append(target[x])
    return target.index(max(l))


def find_first_unmarked(L):
    for i in range(len(L)):
        if L[i][0] == 0:
            return i
    else:
        return


def sim_mmm_func(mode, m, setup_time, delayedoff_time):
    response_time_cumulative = 0  # The cumulative response time
    num_customer_served = 0  # number of completed customers at the end of the simulation

    # Initialising the events
    # Initialising the arrival event
    if mode == 'random':
        next_arrival_time = random.expovariate(Lambda)
        s1k = random.expovariate(Mu)
        s2k = random.expovariate(Mu)
        s3k = random.expovariate(Mu)
        service_time_next_arrival = s1k + s2k + s3k
    else:
        next_arrival_time = atime_list[0]
        service_time_next_arrival = stime_list[0]
        i = 1

    # Initialise both departure events to empty
    next_departure_time = [float("inf")] * m

    # Initialising the Master clock, server status, queue_length, buffer_content
    # Intialise the master clock
    master_clock = 0

    # Intialise server status
    # server_states = 1 if busy, 0 if off, 2 if setup, 3 if delayedoff
    server_states = [0] * m
    server_setup_endtime = [float("inf")] * m
    server_delayedoff_timer = [float("inf")] * m
    arrival_time_next_departure = [0] * m

    # Initialise buffer
    buffer_content = []
    queue_length = 0

    # Start iteration
    while True:
        if mode == 'random':
            if master_clock > time_end:
                break
        else:
            if num_customer_served == len(atime_list):
                break
        # decide next_event_time and which event
        first_departure_time = min(next_departure_time)
        first_departure_server = next_departure_time.index(first_departure_time)
        first_finishing_setup_time = min(server_setup_endtime)
        first_finishing_setup_server = server_setup_endtime.index(first_finishing_setup_time)
        first_off_time = min(server_delayedoff_timer)
        first_off_server = server_delayedoff_timer.index(first_off_time)
        which_first = [next_arrival_time, first_departure_time, first_finishing_setup_time, first_off_time]
        if next_arrival_time == min(which_first):
            next_event_time = next_arrival_time
            next_event_type = 1
        elif first_departure_time == min(which_first):
            next_event_time = first_departure_time
            next_event_type = 0
        elif first_finishing_setup_time == min(which_first):
            next_event_time = first_finishing_setup_time
            next_event_type = 2
        else:
            next_event_time = first_off_time
            next_event_type = 3
        # update master clock
        master_clock = next_event_time
        if mode == 'random':
            if master_clock > time_end:
                break
        # take actions depending on the event type
        if next_event_type == 1:  # arrival
            if mode == 'random':
                atime_list.append(next_arrival_time)
                stime_list.append(service_time_next_arrival)
            if find_states(server_states, 4):
                delayedoff_server = which_selected(find_states(server_states, 4), server_delayedoff_timer)
                next_departure_time[delayedoff_server] = next_arrival_time + service_time_next_arrival
                arrival_time_next_departure[delayedoff_server] = next_arrival_time
                server_delayedoff_timer[delayedoff_server] = float("inf")
                server_states[delayedoff_server] = 1
            elif find_states(server_states, 0):
                setup_server = min(find_states(server_states, 0))
                server_setup_endtime[setup_server] = master_clock + setup_time
                server_states[setup_server] = 3
                buffer_content.append([1, next_arrival_time, service_time_next_arrival])  # first element=1, marked
                queue_length += 1
            else:
                buffer_content.append([0, next_arrival_time, service_time_next_arrival])  # first element=0, ummarked
                queue_length += 1
            # get next arrival information
            if mode == 'random':
                next_arrival_time = master_clock + random.expovariate(Lambda)
                s1k = random.expovariate(Mu)
                s2k = random.expovariate(Mu)
                s3k = random.expovariate(Mu)
                service_time_next_arrival = s1k + s2k + s3k
            else:
                if i < len(atime_list):
                    next_arrival_time = atime_list[i]
                    service_time_next_arrival = stime_list[i]
                    i += 1
                else:
                    next_arrival_time = float("inf")
        elif next_event_type == 0:  # departure
            # Update response_time_cumulative and the number
            response_time_cumulative += master_clock - arrival_time_next_departure[first_departure_server]
            num_customer_served += 1
            dtime_list.append([arrival_time_next_departure[first_departure_server], first_departure_time])
            if not buffer_content:
                next_departure_time[first_departure_server] = float("inf")
                server_states[first_departure_server] = 4
                server_delayedoff_timer[first_departure_server] = master_clock + delayedoff_time
            else:
                sended_job = buffer_content.pop(0)
                queue_length -= 1
                next_departure_time[first_departure_server] = master_clock + sended_job[2]
                arrival_time_next_departure[first_departure_server] = sended_job[1]
                if sended_job[0] == 1:
                    if find_first_unmarked(buffer_content):
                        unmarked_job = find_first_unmarked(buffer_content)
                        buffer_content[unmarked_job][0] = 1
                    else:
                        off_server = which_selected(find_states(server_states, 3), server_setup_endtime)
                        server_states[off_server] = 0
                        server_setup_endtime[off_server] = float("inf")
        elif next_event_type == 2:  # finishing setup
            server_states[first_finishing_setup_server] = 1
            server_setup_endtime[first_finishing_setup_server]=float("inf")
            for index in range(len(buffer_content)):
                if buffer_content[index][0] == 1:
                    break
            sended_job = buffer_content.pop(index)
            queue_length -= 1
            next_departure_time[first_finishing_setup_server] = master_clock + sended_job[2]
            arrival_time_next_departure[first_finishing_setup_server] = sended_job[1]
        else:  # turn to Delayedoff state
            server_states[first_off_server] = 0
            server_delayedoff_timer[first_off_server] = float("inf")
    return response_time_cumulative / num_customer_served

#loop through all the tests.
with open('num_tests.txt') as num:
    num_tests=int(num.read())
for test_index in range(1,num_tests+1):
    with open(f'mode_{test_index}.txt') as mode:
        mode=mode.read()
        mode=mode.strip()
        #print(mode)
    if mode == 'trace':
        with open(f'para_{test_index}.txt') as para:
            m=int(para.readline())
            setup_time=float(para.readline())
            delayedoff_time=float(para.readline())
           # print(m,setup_time,delayedoff_time)
        with open(f'arrival_{test_index}.txt') as arrival:
            for line in arrival:
                atime_list.append(float(line))
           # print(atime_list)
        with open(f'service_{test_index}.txt') as service:
            for line in service:
                stime_list.append(float(line))
           # print(stime_list)
    else:
        with open(f'para_{test_index}.txt') as para:
            m=int(para.readline())
            setup_time = float(para.readline())
            delayedoff_time=float(para.readline())
            time_end = float(para.readline())
           # print(m,setup_time,delayedoff_time,time_end)
        with open(f'arrival_{test_index}.txt') as arrival:
            Lambda=float(arrival.read())
           # print(Lambda)
        with open(f'service_{test_index}.txt') as service:
            Mu=float(service.read())
           # print(Mu)
    random.seed(test_index)
    avg_response_time=sim_mmm_func(mode,m,setup_time,delayedoff_time)
    #print(atime_list,stime_list,dtime_list)
    with open(f'mrt_{test_index}.txt','w') as mrt:
        print(f'{avg_response_time:.3f}',file=mrt,end='')
    dtime_list=sorted(dtime_list,key=lambda x: x[1])
    with open(f'departure_{test_index}.txt','w') as departure:
        for line in range(len(dtime_list)):
            print(f'{dtime_list[line][0]:.3f}\t{dtime_list[line][1]:.3f}',file=departure,end='\n')
    atime_list=[]
    stime_list=[]
    dtime_list=[]
