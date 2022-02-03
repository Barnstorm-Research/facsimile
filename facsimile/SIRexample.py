import functools as F
from typing import List

import scipy.integrate as SI
import numpy as N
import pylab as P
import gillespy2


#######################################################
# Model Definition  FUNCTIONS
#######################################################



#
# This is the dynamics factor
#

def modelvariables():
    """
    This function returns a list of dictionnaries 
    describing the Model Variables in the SIR epidemiology model
    The three variables represent the sizes of the Susceptible population
    the infected population and the recovered population
    :return: list of dictionaries with keys name and indices
    """
    mv=list()
    for v in  ['S','I','R']:
        mvd=dict()
        mvd['name'] = v
        mvd['indices'] = ['Region'] #['Region','Age_Group']
        mv.append(mvd)
    return mv

def modelprocessesO():
    """

    :return:
    """
    mps=list()
    for p in [infection,recovery,reinfection]:
        mp=dict()
        mp['name']=p.__name__
        mp['implementation']=p
        mp['indices']=['Region']
        mps.append(mp)
    return mps

def modelprocesses():
    """
    This function returns a list of dictionaries
    describing the model processes in the SIR epidemiology model
    :return:
    """
    mps=list()
    for (po,pg) in zip([infection,recovery,reinfection],[infectionG,recoveryG,reinfectionG]):
        mp=dict()
        mp['name']=po.__name__
        mp['implementations']=list()
        source='reference'
        for (moc,fun)  in zip(['ODE','Gillespie'],[po,pg]):
            imp=dict()
            imp={'source':source,'moc':moc,'function':fun}
            mp['implementations'].append(imp)
            source='translated'
        mp['indices']=['Region']
        mps.append(mp)
    return mps



def infection(t,y,params=[1e-2,1e-3,1e-3]):
    """
    Reference implementation for infection
    :param t:
    :param y:
    :param params:
    :return:
    :math:$\frac{dI}{dt}=\beta I S$
    """
    beta = params[0]
    flow=y[0]*y[1]*beta
    return [-flow,flow,0.0]

def recovery(t,y,params=[1e-2,1e-3,1e-3]):
    """
    Reference implementation for recovery
    :param t:
    :param y:
    :param params:
    :return:
    """
    rho=params[1]
    flow = y[1]*rho
    return [0.0, -flow,flow]

def reinfection(t,y,params=[1e-2,1e-3,1e-3]):
    """
    Reference implementation for reinfection
    :param t:
    :param y:
    :param params:
    :return:
    """
    beta = params[2]
    flow=y[1]*y[2]*beta
    return [0.0,flow,-flow]


def modelspace():
    """
    Creates the geometry, index space
    :return:
    """
    msp=list()
    ms=dict()
    ms['name']='Region'
    ms['values']=['Metroton','Suburbium','Ruralia']
    ms['advection']={'name':'travel','implementation':travel}
    msp.append(ms)
    #ms=dict()
    #ms['name']='Age_Group'
    #ms['values']=['Age0to16','Age16to40','Age40plus']
    #msp.append(ms)
    return msp
#
# This is the advection operator
#

def travel(x,y):
    """
    Advection operator.
    :param x: population in zone of interest
    :param y: vector of population in all zones
    :return:
    """
    # Fraction of Population traveling out of zone a and
    # into zone b per unit time
    ff = 1e-4  
    # advection is balance of population out of
    # zone of interest
    return sum([ff*(x-yy) for yy in y])


def initvalue(variable,zone):
    """

    :param variable:
    :param zone:
    :return:
    """
    iv=0
    if variable == 'S':
        iv=1000
    elif variable == 'I':
        if zone=='Ruralia':
            iv=100
    return iv
        
    
    
def parameters():
    """

    :return:
    """
    parms=list()
    parms.append({'name':'Infection_rate','implementation':lambda zone: infrecrate(zone)[0]})
    parms.append({'name':'Recovery_rate','implementation':lambda zone: infrecrate(zone)[1]})
    parms.append({'name':'Reinfection_rate','implementation':lambda zone: infrecrate(zone)[2]})
    return parms
                

#
# Gillespie Rendering
#

def modelprocessesG():
    """
    Reder model as Gillespie
    :return:
    """
    return [infectionG,recoveryG,reinfectionG]

# Translation of reference implementation

def infectionG(y,params):
    """
    Reference:
    def infection(t,y,params=[1e-2,1e-3,1e-3]):
       beta = params[0]
       flow=y[0]*y[1]*beta
       return [-flow,flow,0.0]
    :param y:
    :param params:
    :return:
    """
    beta=params[0]
    react=dict()
    react['name']='Infection'
    react['rate']=beta
    react['reactants']={y[0]:1,y[1]:1}
    react['products']={y[1]:2}
    return react
def recoveryG(y,params):
    """
    Reference:
    def recovery(t,y,params=[1e-2,1e-3,1e-3]):
    rho=params[1]
    flow = y[1]*rho
    return [0.0, -flow,flow]
    :param y:
    :param params:
    :return:
    """
    rho=params[1]
    react=dict()
    react['name']='Recovery'
    react['rate']=rho
    react['reactants']={y[1]:1}
    react['products']={y[2]:1}
    return react

def reinfectionG(y,params):
    """
    Reference:
    def reinfection(t,y,params=[1e-2,1e-3,1e-3]):
        beta = params[2]
        flow=y[1]*y[2]*beta
        return [0.0,flow,-flow]
    :param y:
    :param params:
    :return:
    """
    beta = params[2]
    react=dict()
    react['name']='Reinfection'
    react['rate']=beta
    react['reactants']={y[1]:1,y[2]:1}
    react['products']={y[1]:2}
    return react
