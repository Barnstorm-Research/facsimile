from typing import List
from facsimile import framework as F
import facsimile.fermi as fermi
import scipy.integrate as SI
import numpy as N
import pylab as P
import gillespy2

'''
SIR Model Factors Definition
'''


'''
Dynamics Factor

'''

def get_dynamics_factor(nproc=3):
    sir_df=F.DynamicsFactor()
    for v in  ['S','I','R']:
        sir_df.add_variable(v,'Region')
    
    for (po,pg) in zip([infection,recovery,reinfection][:nproc],[infectionG,recoveryG,reinfectionG][:nproc]):
        mp=dict()
        mp['name']=po.__name__
        mp['implementations']=list()
        source='reference'
        for (moc,fun)  in zip(['ODE','Gillespie'],[po,pg]):
            sir_df.add_process(po.__name__,source,moc,fun,['Region'])
            source='translated'
    return sir_df


'''
Space Component

'''

def get_space_factor():
    SIRsp=F.SpaceFactor()    
    SIRsp.add_index('Region',['Metroton','Suburbium','Ruralia'])
    SIRsp.add_advection('Travel','Region',travel)
    return SIRsp 
                        

'''
Parameters Factor

'''

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


def get_parameters_factor():
    
    SIRparams=F.ParameterFactor()
    SIRparams.add_parameter('Infection_rate',lambda zone: fermi.fermi('infrecrates',zone)[0])
    SIRparams.add_parameter('Recovery_rate',lambda zone: fermi.fermi('infrecrates',zone)[1])
    SIRparams.add_parameter('Reinfection_rate',lambda zone: fermi.fermi('infrecrates',zone)[2])
    return SIRparams


'''
Function definitions
'''


def infection(t,y,params=[1e-2,1e-3,1e-3]):
    r"""
    Reference implementation for infection
    as an ODE

    :param t: time
    :param y: list of current values of S, I, R
    :param params: list of model paramters 
    :return: list with contributions of infection process to S, I, R derivatives

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

    :param t: time
    :param y: list of current values of S, I, R
    :param params: list of model paramters 
    :return: list with contributions of recovery process to S, I, R derivatives

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

    :param t: time
    :param y: list of current values of S, I, R
    :param params: list of model paramters 
    :return: list with contributions of recovery process to S, I, R derivatives

    :math:'\frac{dS}{dt}=0'
    :math:'\frac{dI}{dt}=\beta I S'
    :math:'\frac{dR}{dt}=-\beta I R'

    """
    beta = params[2]
    flow=y[1]*y[2]*beta
    return [0.0,flow,-flow]


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

