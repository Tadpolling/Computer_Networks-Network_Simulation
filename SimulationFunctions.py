# This is a sample Python script.
import random
import sys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np

LOAD_BALANCER_SERVER_NUMBER=-1
EVENT_SERVER_NUMBER_INDEX=0
EVENT_INPUT_INDEX=1
EVENT_OCCURRENCE_TIME_INDEX=2
REQUEST_INPUT_TIME_INDEX=1
#Statistics Globals

def sample_poisson(lambda_parameter=1,t=1):
    a=0
    n=0
    while(a<t):
        a=a+np.random.exponential(scale=1/lambda_parameter)
        n+=1
    return n


def get_default_parameters():
    #Creates Values for Simulation, Based on input from the Assignment
    T=5000
    N=2
    Prob_list=[0.2,0.8]
    lambda_parameter=200
    Q_size_list=[10,20]
    mu_list=[20,190]
    return T, N, Prob_list, lambda_parameter, Q_size_list, mu_list
def get_parameters():
    #Creates values for Simulation, based on input from command line
    args_list=sys.argv
    T=int(args_list[0])
    N=int(args_list[1])
    Prob_list=list(map(float,args_list[2:2+N]))
    lambda_parameter=int(args_list[2+N])
    Q_size_list=list(map(int,args_list[3+N:3+2*N]))
    mu_list=list(map(float,args_list[3+2*N:3+3*N]))

    return T,N,Prob_list,lambda_parameter,Q_size_list,mu_list

def create_probability_delimiters(Probs_list):
    #From a list of probabilities, creates a list of delimeters that break up the segment [0,1] so that
    #we can know which server was chosen to handle a certain request
    delim_list=[]
    prev_value=0
    for p in Probs_list:
        prev_value=prev_value+p
        delim_list.append(prev_value)
    return delim_list
def probability_choosing(Probs_delim_list):
    #Chooses a server according to probabilites(Weighted Probabilities)
    index=0
    uniform_sample=np.random.uniform()
    while Probs_delim_list[index]<uniform_sample:
        index+=1
    #print(uniform_sample)
    return index

def test_poisson_distribution(N=400,lambda_parameter=50):
    #Used to make sure the poisson distribution works as intended
    sample_size = N
    sum = 0
    for i in range(sample_size):
        sum += sample_poisson(lambda_parameter=lambda_parameter)

    #The Expectation of a poisson distribution is its parameter lambda
    print(sum / sample_size)
# Press the green button in the gutter to run the script.

def add_event(event_list,event):

    i=0
    for i in range(0,len(event_list)):
        if event_list[i][EVENT_OCCURRENCE_TIME_INDEX]>event[EVENT_OCCURRENCE_TIME_INDEX]:
            event_list.insert(i,event)
            return event_list
    event_list.append(event)
    return event_list

def is_server_running(server_number,event_list):
    for event in event_list:
        event_server_number=event[EVENT_SERVER_NUMBER_INDEX]
        if event_server_number==server_number:
            return True
    return False
def give_event_to_server(event_list,event,prob_delim_list,server_queue_dict,Q_size_list,mu_list):

    global NUMBER_OF_THROWN_OUT_REQUESTS

    accepting_server_number=probability_choosing(prob_delim_list)
    current_time = event[EVENT_OCCURRENCE_TIME_INDEX]
    #If the server is not running, we will add it to the event list as it will now be running
    if not is_server_running(accepting_server_number,event_list):

        new_event=(accepting_server_number,current_time,current_time+np.random.exponential(scale=1/mu_list[accepting_server_number]))
        return add_event(event_list,new_event),server_queue_dict

    #Check if the server queue is full
    if len(server_queue_dict[accepting_server_number])>=Q_size_list[accepting_server_number]:
        #Throw event away
        NUMBER_OF_THROWN_OUT_REQUESTS+=1
        return event_list,server_queue_dict

    #Here we know we can add the request to the queue
    new_request=(accepting_server_number,current_time,None)
    server_queue_dict[accepting_server_number].append(new_request)
    return event_list,server_queue_dict


def print_output(A,B,T_end,sum_T_w,sum_T_S):
    #Calculating Averages
    if A==0:
        T_w = 0
        T_s = 0
    else:
        T_w=sum_T_w/A
        T_s=sum_T_S/A

    print(f"{A} {B} {T_end} {T_w} {T_s}\n")
if __name__ == '__main__':
    global NUMBER_OF_THROWN_OUT_REQUESTS
    global NUMBER_OF_REQUESTS_SERVICED
    global TIME_OF_LAST_REQUEST_SERVICED
    global SUM_OF_TIME_WAITED_FOR_SERVICE
    global SUM_OF_TIME_SERVICED
    NUMBER_OF_REQUESTS_SERVICED = 0
    NUMBER_OF_THROWN_OUT_REQUESTS = 0
    TIME_OF_LAST_REQUEST_SERVICED = 0
    SUM_OF_TIME_WAITED_FOR_SERVICE = 0
    SUM_OF_TIME_SERVICED = 0
    #print(sys.argv)
    #Defining Parameters
    T, N, Prob_list, lambda_parameter, Q_size_list, mu_list=get_default_parameters()
    prob_delim_list=create_probability_delimiters(Prob_list)
    event_list=[]
    event_list.append((LOAD_BALANCER_SERVER_NUMBER,None,np.random.exponential(scale=1/lambda_parameter)))
    #(#server,time_out,time_in)
    server_queue_dict={}
    #Initializing the lengths of the server's queues to be 0
    for i in range(0,N):
        server_queue_dict[i]=[] #this list represents the queue for the server




    t=0
    while(len(event_list)>0):
        current_event=event_list.pop(0)
        server_number,input_time,occurrence_time=current_event
        t=occurrence_time
        #if the event is for the load balancer
        if server_number==LOAD_BALANCER_SERVER_NUMBER:
            if t>=T:
                continue
            next_request=(LOAD_BALANCER_SERVER_NUMBER, None, t+np.random.exponential(scale=1 / lambda_parameter))
            event_list=add_event(event_list,next_request)
            event_list,server_queue_dict=give_event_to_server(event_list,current_event,prob_delim_list,server_queue_dict,Q_size_list,mu_list)
            continue

        #if the event is for the servers
        current_time=current_event[EVENT_OCCURRENCE_TIME_INDEX]
        server_number=current_event[EVENT_SERVER_NUMBER_INDEX]
        NUMBER_OF_REQUESTS_SERVICED+=1
        TIME_OF_LAST_REQUEST_SERVICED=current_event[EVENT_OCCURRENCE_TIME_INDEX]
        time_serviced=current_time-current_event[EVENT_INPUT_INDEX]
        SUM_OF_TIME_SERVICED+=time_serviced

        if len(server_queue_dict[server_number])>0:
            #If we are here the server has another request to service
            request=server_queue_dict[server_number].pop(0)
            new_event=(server_number,current_time,current_time+np.random.exponential(scale=1 / mu_list[server_number]))
            event_list=add_event(event_list,new_event)
            waiting_time=current_time-request[REQUEST_INPUT_TIME_INDEX]
            SUM_OF_TIME_WAITED_FOR_SERVICE+=waiting_time

    print_output(A=NUMBER_OF_REQUESTS_SERVICED,
                 B=NUMBER_OF_THROWN_OUT_REQUESTS,
                 T_end=TIME_OF_LAST_REQUEST_SERVICED,
                 sum_T_w=SUM_OF_TIME_WAITED_FOR_SERVICE,
                 sum_T_S=SUM_OF_TIME_SERVICED)