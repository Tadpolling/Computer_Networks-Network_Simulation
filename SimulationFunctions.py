# This is a sample Python script.
import random
import sys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
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
    print(uniform_sample)
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
if __name__ == '__main__':
    print(sys.argv)
    #Defining Parameters
    T, N, Prob_list, lambda_parameter, Q_size_list, mu_list=get_default_parameters()
    test_poisson_distribution(N=400,lambda_parameter=lambda_parameter)
    prob_delim_list=create_probability_delimiters(Prob_list)
    val=probability_choosing(Probs_delim_list=prob_delim_list)
    
    print(val)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
