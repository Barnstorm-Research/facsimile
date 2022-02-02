import functools as F
import scipy.integrate as SI
import numpy as N
import pylab as P
import gillespy2


#######################################################
# Model Definition  FUNCTIONS
#######################################################

#
# This is the FERMI part.
# Computes  zone dependent constants
# First value is the transmission rate in the zone
# second number is the recovery rate out of the zone
#

def fermi(query,indexvalue):

    if query=='infrecrates':
        return infrecrate(indexvalue)
    else:
        return []

def infrecrate(zone):
    if zone == 'Metroton':
        return 1e-4,1e-2,1e-5
    elif zone == 'Suburbium':
        return 1e-3,1e-2,1e-4
    else:
        return 1e-4,1e-2,1e-5

def initvalue(variable,zone):
    iv=0
    if variable == 'S':
        iv=1000
    elif variable == 'I':
        if zone=='Ruralia':
            iv=100
    return iv
        
    
    
def parameters():
    parms=list()
    parms.append({'name':'Infection_rate','implementation':lambda zone: infrecrate(zone)[0]})
    parms.append({'name':'Recovery_rate','implementation':lambda zone: infrecrate(zone)[1]})
    parms.append({'name':'Reinfection_rate','implementation':lambda zone: infrecrate(zone)[2]})
    return parms

#
# This is the dynamics factor
#

def modelvariables():
    mv=list()
    for v in  ['S','I','R']:
        mvd=dict()
        mvd['name'] = v
        mvd['indices'] = ['Region'] #['Region','Age_Group']
        mv.append(mvd)
    return mv

def modelprocessesO():
    mps=list()
    for p in [infection,recovery,reinfection]:
        mp=dict()
        mp['name']=p.__name__
        mp['implementation']=p
        mp['indices']=['Region']
        mps.append(mp)
    return mps

def modelprocesses():
    mps=list()
    for p in [infection,recovery,reinfection]:
        mp=dict()
        mp['name']=p.__name__
        mp['implementations']=list()
        source='reference'
        for moc in ['ODE','Stochastic','PDE']:
            imp=dict()
            imp={'source':source,'moc':moc}
            mp['implementations'].append(imp)
            source='translated'
        mp['indices']=['Region']
        mps.append(mp)
    return mps


# Reference Implementations
def infection(t,y,params=[1e-2,1e-3,1e-3]):
    beta = params[0]
    flow=y[0]*y[1]*beta
    return [-flow,flow,0.0]

def recovery(t,y,params=[1e-2,1e-3,1e-3]):
    rho=params[1]
    flow = y[1]*rho
    return [0.0, -flow,flow]

def reinfection(t,y,params=[1e-2,1e-3,1e-3]):
    beta = params[2]
    flow=y[1]*y[2]*beta
    return [0.0,flow,-flow]



#
# This is the geometry or index space
#
def modelspace():
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
    # x: population in zone of interest
    # y: vector of population in all zones
    # Fraction of Population traveling out of zone a and
    # into zone b per unit time
    ff = 1e-4  
    # advection is balance of population out of
    # zone of interest
    return sum([ff*(x-yy) for yy in y])

                

#
# Gillespie Rendering
#

def modelprocessesG():
    return [infectionG,recoveryG,reinfectionG]

# Translation of reference implementation

def infectionG(y,params):
    '''
    Reference:
    def infection(t,y,params=[1e-2,1e-3,1e-3]):
       beta = params[0]
       flow=y[0]*y[1]*beta
       return [-flow,flow,0.0]
    '''
    beta=params[0]
    react=dict()
    react['name']='Infection'
    react['rate']=beta
    react['reactants']={y[0]:1,y[1]:1}
    react['products']={y[1]:2}
    return react
def recoveryG(y,params):
    '''
    Reference:
    def recovery(t,y,params=[1e-2,1e-3,1e-3]):
    rho=params[1]
    flow = y[1]*rho
    return [0.0, -flow,flow]
    '''
    rho=params[1]
    react=dict()
    react['name']='Recovery'
    react['rate']=rho
    react['reactants']={y[1]:1}
    react['products']={y[2]:1}
    return react

def reinfectionG(y,params):
    '''
    Reference:
    def reinfection(t,y,params=[1e-2,1e-3,1e-3]):
        beta = params[2]
        flow=y[1]*y[2]*beta
        return [0.0,flow,-flow]
    '''
    beta = params[2]
    react=dict()
    react['name']='Reinfection'
    react['rate']=beta
    react['reactants']={y[1]:1,y[2]:1}
    react['products']={y[1]:2}
    return react



