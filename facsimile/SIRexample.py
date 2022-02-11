'''This Module contains definitiopns for the Space, parameter and Dynamics factor for
an SIR epidemics model. These factors can be composed, modified, and rendered into
executable modelsusing the tools of the FACSIMILE framework
'''
from abc import ABC, abstractmethod

import simpy as spy
import numpy as np

from facsimile import framework as F
from  facsimile import  fermi
from typing import Iterator, List, Optional
from dataclasses import dataclass

###
# SIR Model Factors Definition
###


###
# Dynamics Factor
###

def get_ABM_dynamics_factor(npro=3):
    """
    Create Dynamics Factor with only an ABM dynamics
    :param npro: The number of processes
    :return:
    """
    sir_df=F.Dynamics_Factor()
    for varName in  ['S','I','R']:
        sir_df.add_variable(varName,['Region'])

    for processABM in [InfectionABMProc('S','I'),RecoveryABMProc('I','R')]:
        model_proc={}
        model_proc['name']=processABM.__name__
        model_proc['implementations']=[]
        source='reference'
        for (moc,fun)  in zip(['ABM'],[processABM]):
            sir_df.add_process(processABM.__name__,source,moc,fun,['Region'])
            source='translated'
    return sir_df


def get_dynamics_factor(nproc=3):
    '''
    Create Dynamics Factor for the SIR model
    There are 3 processes defined in this example, Infection recovery and reinfection
    the optional parameter nproc dis used to select how many of these 3 are used.
    The processes have one reference implementation (ODE) and one translated
    implementation (Gillespie)
    There are threee dynamic variables, S, I and R which are indexed with the Region index
    Args:
        nproc: Number of processes (default 2)
    Returns:
        sir_df: (frameowrk.DynamicsFactor) SIR Dynamics Factor
    '''
    sir_df=F.Dynamics_Factor()
    for variab in  ['S','I','R']:
        sir_df.add_variable(variab,['Region'])

    for (proc_ode,proc_gilles) in zip([infection,recovery,reinfection][:nproc],\
                       [infection_G,recovery_G,reinfection_G][:nproc]):
        model_proc={}
        model_proc['name']=proc_ode.__name__
        model_proc['implementations']=[]
        source='reference'
        for (moc,fun)  in zip(['ODE','Gillespie'],[proc_ode,proc_gilles]):
            sir_df.add_process(proc_ode.__name__,source,moc,fun,['Region'])
            source='translated'
    return sir_df


###
# Space Component
###

def get_space_factor(nregions=3):
    '''
    Create Space Factor for the SIR model. There is one index type (Region) with up
    to 5 possible values
    Args:
        nregions: Number of regions used for the model (default 3)
    Returns:
        sir_sf: (frameowrk.SpaceFactor) SIR Space Factor
    '''

    SIR_space=F.Space_Factor()
    SIR_space.add_index('Region',['Metroton','Suburbium','Ruralia','Westcosta','Islandii'][:nregions])
    SIR_space.add_advection('Travel','Region',travel)
    return SIR_space

###
# Parameters Factor
###


def init_value(variable,zone):
    """
    Return the initial value for a variable in a given Region
    Args:
        variable: Dynamic Variable, one of S, I or R
        zone: Name of the region
    Returns:
        iv: initial value for the variable in the region
    """
    init_value=0
    if variable == 'S':
        init_value=1000
    elif variable == 'I':
        if zone=='Ruralia':
            init_value=100
        elif zone == 'Westcosta':
            init_value=10
        else:
            init_value=0
    return init_value

def get_parameters_factor():

    SIR_params=F.Parameter_Factor()
    SIR_params.add_parameter('Infection_rate',lambda zone: fermi.fermi('infrecrates',zone)[0])
    SIR_params.add_parameter('Recovery_rate',lambda zone: fermi.fermi('infrecrates',zone)[1])
    SIR_params.add_parameter('Reinfection_rate',lambda zone: fermi.fermi('infrecrates',zone)[2])
    return SIR_params

###
# Function definitions
###

def infection(t,y,params=[1e-2,1e-3,1e-3]):
    r"""
    Reference implementation for infection as an ODE
    Args:
       t: time
       y: list of current values of S, I, R
       params: list of model paramters
    Returns:
        list with contributions of infection process to S, I, R derivatives

    :math:'\frac{dS}{dt}=-\beta I S'
    :math:'\frac{dI}{dt}=\beta I S'
    :math:'\frac{dR}{dt}=0'
    """
    beta = params[0]
    flow=y[0]*y[1]*beta
    return [-flow,flow,0.0]

def recovery(t,y,params=[1e-2,1e-3,1e-3]):
    r"""
    Reference implementation for recovery
    Args:
        t: time
        y: list of current values of S, I,R
        params: list of model paramters
    Returns:
        list with contributions of recovery process to S, I, R derivatives

    :math:'\frac{dS}{dt}=0'
    :math:'\frac{dI}{dt}=-\rho I'
    :math:'\frac{dR}{dt}=\rho I'
    """
    rho=params[1]
    flow = y[1]*rho
    return [0.0, -flow,flow]

def reinfection(t,y,params=[1e-2,1e-3,1e-3]):
    r"""
    Reference implementation for recovery
    Args:
        t: time
        y: list of current values of S, I, R
        params: list of model paramters
    Returns:
    list with contributions of recovery process to S, I, R derivatives

    :math:'\frac{dS}{dt}=0'
    :math:'\frac{dI}{dt}=\beta I S'
    :math:'\frac{dR}{dt}=-\beta I R'

    """
    beta = params[2]
    flow=y[1]*y[2]*beta
    return [0.0,flow,-flow]

# Agent-Based Model Implementation

class ABMProcess(ABC):
    """
    Describes a process for an agent based model.
    """

    def __init__(self,startState:chr,endState:chr,name:str):
        self.startState = startState
        self.endState = endState
        self.name = name

    def nChooseK(self,n,k):
        return np.math.factorial(n)*1./(np.math.factorial(k)*np.math.factorial(n-k)*1.)

    @property
    def __name__(self):
        return self.name

    @abstractmethod
    def apply(self,y:List[float],params:List[float]) -> bool:
        """
        If true, then the process applies and the agent should transition to the endState.
        :param y:
        :param params:
        :return:
        """
        pass

class InfectionABMProc(ABMProcess):

    def __init__(self,startState:chr,endState:chr): ABMProcess.__init__(self,startState,endState,"Infection")

    def apply(self,y:List[float],params:List[float]) -> bool:
        S,I,R = y
        a,b = params
        totalProb = 0.0
        for numInfected in range(1,I+1):
            totalProb += (a**numInfected)*((1-a)**(I-numInfected))*self.nChooseK(I,numInfected)
        return np.random.choice(2,1,p=[totalProb,1-totalProb]) == 0

class RecoveryABMProc(ABMProcess):

    def __init__(self,startState:chr,endState:chr): ABMProcess.__init__(self,startState,endState,"Recovery")

    def apply(self,y:List[float],params:List[float]) -> bool:
        return np.random.choice(2,1,p=[params[1],1.-params[1]]) == 0

# Translation of reference implementation

def infection_G(y,params):
    """
    Reference:
    def infection(t,y,params=[1e-2,1e-3,1e-3]):
       beta = params[0]
       flow=y[0]*y[1]*beta
       return [-flow,flow,0.0]
    """
    beta=params[0]
    react={}
    react['name']='Infection'
    react['rate']=beta
    react['reactants']={y[0]:1,y[1]:1}
    react['products']={y[1]:2}
    return react

def recovery_G(y,params):
    """
    Reference:
    def recovery(t,y,params=[1e-2,1e-3,1e-3]):
    rho=params[1]
    flow = y[1]*rho
    return [0.0, -flow,flow]
    """
    rho=params[1]
    react={}
    react['name']='Recovery'
    react['rate']=rho
    react['reactants']={y[1]:1}
    react['products']={y[2]:1}
    return react

def reinfection_G(y,params):
    """
    Reference:
    def reinfection(t,y,params=[1e-2,1e-3,1e-3]):
        beta = params[2]
        flow=y[1]*y[2]*beta
        return [0.0,flow,-flow]
    """
    beta = params[2]
    react={}
    react['name']='Reinfection'
    react['rate']=beta
    react['reactants']={y[1]:1,y[2]:1}
    react['products']={y[1]:2}
    return react


#
# This is the advection operator
#

def travel(x,y):
    """
    Implementation of the travel Advection operator.

    Args:
       x: population in zone of interest
       y: vector of population in all zones
    Returns:
       v: vector of rate of travel into zone of interest from each of the zones
    """
    # Fraction of Population traveling out of zone a and
    # into zone b per unit time
    travel_rate = 1e-4
    # advection is balance of population out of
    # zone of interest
    return sum([-travel_rate*(x-yy) for yy in y])
