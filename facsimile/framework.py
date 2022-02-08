'''
This module contains the class and method definitions used to compose, modify and
render factored models into executable simulations
'''

import pprint
import functools as F
import pylab as P
import gillespy2



class Dynamics_Factor:
    '''
    Hold the data for a dynamic factor
    '''

    def __init__(self):
        self.processes = []
        self.variables = []

    def __repr__(self):
        return repr({'Variables':self.variables,'Processes':self.processes})
    def __str__(self):
        return pprint.pformat({'Variables':self.variables,'Processes':self.processes})

    def add_variable(self,name,indices=[]):
        '''
        This Method adds a model variable to an existing Dynamics Factor
        Args:
         name: Name of the model variable
         indices : List of indices the variable depends on. (default [])
        '''
        self.variables.append({'name':name,'indices':indices})

    def add_process(self, name,source,moc,fun,indices=[],aggregators=[]):
        '''
        This Method adds a model process to an existing Dynamics Factor
        If the process already exists, this method can be used to add addtional
        modes of computation
        Args:
         name: Name of the model process (string)
         source: Traceability string (string)
         moc: Mode of computation (string)
         fun: Function implementing the process for the model of computation specified
         indices : List of indices the process depends on. (default [])
        '''
        #print(aggregators)
        names=[p['name'] for p in self.processes]
        imp={'source':source,'moc':moc,'function':fun}
        if name in names:
            i=names.index(name)
            self.processes[i]['implementations'].append(imp)
        else:
            self.processes.append({'name':name,'implementations':[imp],'indices':indices,'aggregators':aggregators})

    def get_variables(self):
        '''
        Get the Dynamic variables for the factor
        Returns:
        list: list of model variables
        '''
        return self.variables
    def get_processes(self,moc=[]):
        '''
        Get the dynamic processes of the factor for a set of mocs.
        If the moc parameter is empty, return all the known mocs for each  process
        Args:
        moc (list): List of models of computation (default [])
        Returns:
        list: model processes
        '''
        if not moc:
            return self.processes
        all_proc=[h for h in sum([f['implementations'] for f in self.processes],[]) if h['moc']==moc]
        all_proc=list(zip(all_proc,[f['aggregators']for f in self.processes]))
        return  [{'implementation':h['function'],\
                  'name':h['function'].__name__,'aggregators':aggregators} for (h,aggregators) in all_proc]

    def to_dot (self,file):
        '''
        Build Dynamics Factor subgraph in dot format
        Args:
            f: file object
        '''

        file.write('subgraph clusterDynamics { \n')
        file.write('label = DYNAMICS_Factor  \n')

    # Dynamics subgraph

        file.write('subgraph clusterEmpty  { \n')
        file.write('label = "Diagram" \n fontcolor = black \n')
        model_vars=self.variables
        for model_var in model_vars:
            file.write(model_var['name']+' [shape=box, fontsize=10,label=<'+model_var['name']+\
                    '<BR /><FONT POINT-SIZE="5">'+ \
                    ', '.join(model_var['indices'])+ '</FONT>> ] \n')
        indlist=[a['indices'] for a in self.get_processes()]
        for proc,indices ,aggregators in zip(self.get_processes('ODE'),indlist,[p['aggregators']for p in self.get_processes()]):
            file.write(proc['name']+' [shape=oval, fontsize=10,label=<'+proc['name']+\
                    '<BR /><FONT POINT-SIZE="5">'+ \
                    ', '.join(indices)+ '</FONT>> ] \n')
            d_values=proc['implementation'](0,[1 for x in range(len(model_vars))])
            sources = [i for i in range(len(d_values)) if d_values[i]<0]
            dest = [i for i in range(len(d_values)) if d_values[i]>0]
            for i in sources:
                file.write(model_vars[i]['name']+' -> '+proc['name'] +'[color=green,penwidth=3]\n')
            for j in dest:
                file.write(proc['name']+ ' -> ' + model_vars[j]['name']+ \
                    '[color = green,penwidth=3]\n')
            for (i,agg) in enumerate(aggregators):
                if  agg=='sum':
                    file.write(model_vars[i]['name']+'->'+proc['name'] + '[label=<<FONT POINT-SIZE="10"   >'+agg+'</FONT>>]\n')
                elif  agg=='dirac': 
                    file.write(model_vars[i]['name']+'->'+proc['name'] +'\n')
        file.write('}\n') # Close Dynamics subgraph

    #
    # Build Implementations SubGraph
    #

        file.write('subgraph clusterImplementations  { \n')
        file.write('label = "Implementations" \n fontcolor = black \n')
        start=True
        for proc in self.processes:
            mocs=[','.join([pm['moc'],pm['source'],'<BR />']) for pm in proc['implementations']]
            file.write(proc['name']+'i [shape=oval, fontsize=10,label=<'+proc['name']+\
                    '<BR /><FONT POINT-SIZE="5">'+ \
                    ' '.join(mocs)+ '</FONT>> ] \n')
            if start:
                link_to=proc['name']+'i'
                start=False
            else:
                file.write(link_to+' -> '+proc['name']+'i [style=invis]\n')
                link_to=proc['name']+'i'
        file.write('}\n') # Close Implementations
        file.write('}\n') # Close Dynamics



class Space_Factor:
    '''
    Hold the data for a dynamic factor
    '''

    def __init__(self):
        self.indices = []
        self.advections = {}

    def __repr__(self):
        return repr({'Indices':self.indices,'Advections':self.advections})
    def __str__(self):
        return pprint.pformat({'Indices':self.indices,'Advections':self.advections})


    def add_index(self,name,values):
        '''
        This Method adds a new index type, and the corresponding values
        to an existing Space Factor
        Args:
         name: Name of the Index type
         values: List of values for the index type.
        '''
        self.indices.append({'name':name,'values':values})


    def add_advection(self, name,index ,fun):
        '''
        This Method adds a new advection operator to an existing Space Factor
        Args:
         name: Name of the advection operator
         index: Name of the index over which this advection operates
         fun: function implementing the advection operator
        '''

        self.advections[index]={'name':name,'implementation':fun}


    def get_space(self):
        '''
        Create a list object with indices and advections
        Returns:
            list of indices with their advections
        '''
        space=[]
        for ind in self.indices:
            if ind['name'] in self.advections:
                ind['advection']=self.advections[ind['name']]
            space.append(ind)
        return space

    def to_dot (self,file):
        '''
        Write to file a subgraph  in dot format with the space factor
        '''
    #
    # Build Space Factor
    #

        mss=self.indices
        mssa=self.advections
        file.write('subgraph clusterspace { \n')
        file.write('label = SPACE_Factor  \n')
        file.write('rankdir=LR \n')
        start=True
        for index in mss:
            # Build Index Subgraph
            file.write('subgraph cluster'+index['name']+' {label ="'+index['name']+'"\n')
            file.write(index['name']+'a '+' [label="",style=invis,width=0] \n')
            for value in index['values']:
                file.write(value+' [shape=box,fontsize=10] \n')
            file.write('}') # Close Index Subgraph
            if start:
                link_to=index['name']+'a'
                start=False
            else:
                file.write(link_to+' -> '+index['name']+'a [style=invis]\n')
                link_to=index['name']+'a'
            if index['name'] in mssa:
                # Add Advection to Index
                advname=mssa[index['name']]['name']
                file.write(advname+' [shape=oval,fontsize=10] \n')
                file.write(link_to+ '  -> ' + advname+ \
                        '[ltail = cluster'+index['name']+\
                        ',color=blue,penwidth=3]\n')
                file.write(advname + \
                        ' -> '+link_to+' [lhead = cluster'+index['name']+ \
                        ',color=blue,penwidth=3] \n')
                link_to=advname
        file.write('}') # Close Space Factor


class Parameter_Factor:
    '''
    Hold the data for a dynamic factor
    '''

    def __init__(self):
        self.parameters = []

    def __repr__(self):
        return repr({'Parameters':self.parameters})
    def __str__(self):
        return pprint.pformat({'Parameters':self.parameters})


    def add_parameter(self,name,fun):
        '''
        This Method adds a new parameter to the Parameter Factor
        Args:
         name: Parameter name
         fun: Function implementing a query to obtain the value
         of the parameter for a given condition
        '''

        self.parameters.append({'name':name,'implementation':fun})

    def get_parameters(self):
        '''
        Return List object with the factor parameters
        '''
        return self.parameters

    def to_dot(self,file):
        '''
        Build Parameter Factor Subgraph
        In the dot format
        Args:
            f: file object
        '''


        file.write('subgraph clusterparams { \n')
        file.write('label = Parameters_Factor  \n')
        #f.write('paramsa '+' [label="",style=invis,width=0] \n')
        #f.write(lo+' -> '+'paramsa [style=invis]\n')
        for param in self.parameters:
            file.write(param['name']+' [shape=box, fontsize=10, label='+param['name']+' ] \n')
        file.write('}') # Close Parameters Factor



#######################################################
# FRAMEWORK FUNCTIONS
#######################################################

def distribute_to_ode(space,dynamics,parameters):
    """
    This function is the "inverse" of factorization. It takes as inputs 3 factors, space,
    dynamics and parameters, and outputs the SIR model in ODE form suitable to be
    integrated with scipy.Integrate methods
Args:
    space: Space Factor (framework.SpaceFator)
    dynamics: Dynamics Factor
Returns:
    model: ODE function with the signature expected by scipy integrate
    """

    # TODO: This assumes one index only
    indexvalues = space.get_space()[0]['values']
    if 'advection' in space.get_space()[0]:
        advoper = space.get_space()[0]['advection']['implementation']
    else:
        advoper=[]
    var = [vv['name'] for vv in dynamics.variables]

    params=parameters.get_parameters()
    def paramf(indexv):
        return [p['implementation'](indexv)  for p in params ]
    
    def expand(agg,num_ind_values):
        def agg_fun(agg,y,i):
            if agg=='dirac':
                return y[i]
            if agg == 'sum':
                return sum(y)
            return 0

        num_var=len(agg)
        return lambda y, i: [agg_fun(agg_e,y[j:num_var*num_ind_values:num_var],i) for (j,agg_e) in enumerate(agg)]


    #
    # all the processes in ODE implementation
    # with expanded aggregators    
    # Each process takes as additional argument 
    # which index value it is applied to
    #
    ode_procs= [lambda t,y,parms,i,p=p : p['implementation'](t,expand(p['aggregators'],len(indexvalues))(y,i),parms) for p in dynamics.get_processes('ODE')]
 
    #
    # Sum all processes for a fixed index value
    #
   
    ode_procs_sum = lambda t,y,params,i :[sum(a) for a in zip(*[op(t,y,params,i) for op in ode_procs])]

    #
    # repeat processes for all index values
    #
    ode_procs_allv = lambda t, y : sum([ode_procs_sum(t,y,paramf(indexvalue),i) for (i,indexvalue) in enumerate(indexvalues)],[])

    #
    # Add advection
    #
    if advoper:
        advff=apply_advection(advoper,var,indexvalues)
        redfun=lambda f1,f2: lambda t,x : f1(t,x[:-len(var)])+f2(t,x[-len(var):]) 
        vout=lambda t,y: [sum(a) for a in zip(ode_procs_allv(t,y),advff(y))]
        return vout
    return ode_procs_allv

def apply_advection(advoper, var, indexvalues):
    """
    This is an utility function to apply the advection operator to the whole model.
    It's called by distribute only.
    """
    aff=[]
    for i in range(len(indexvalues)):
        for j in range(len(var)):
            aff.append(lambda y,i=i,j=j: \
                      advoper(y[j+i*len(var)],y[j:len(var)*(len(indexvalues)):len(var)]))
    aadv=lambda y : [fff(y) for fff in aff]
    return aadv


#######################################################
# Model rendering and simulation  FUNCTIONS
#######################################################

class Distribute_to_gillespie(gillespy2.Model):
    '''
    Class to hold model in Gillespie form
    Inherits from gillespy2.Model
    '''

    def __init__(self, dynfactor,spacefactor,parfactor,initvalue,maxt):
        """
        This function
        is the "inverse" of factorization. It takes as inputs 3 factors, space, dynamic
        parameters and outputs the SIR model in Reaction  form suitable to be integrated
        with the Gillespy toolbox
        Args:
        space: Space Factor (framework.SpaceFator)
        dynamics: Dynamics Factor
        Returns:
        model: Gillespy Reaction model
        """
        gillespy2.Model.__init__(self, name='Gillespie')

        modelspace=spacefactor.get_space
        modelvariables=dynfactor.get_variables

        # TODO
        # This is valid only for one index
        # simple advection
        index0=spacefactor.indices[0]['name']
        advrate=-spacefactor.advections[index0]['implementation'](1,[0])

        #
        # Parameters from FERMI
        #
        paramd={}
        params=parfactor.get_parameters()

        for rvalue in modelspace()[0]['values']:
            parameters = []
            #prates= fermi.fermi(parameter_query,r)
            prates=[p['implementation'](rvalue)  for p in params ]
            for i in range(len(prates)):
                parameters.append(gillespy2.Parameter(
                    name='k_c'+str(i)+rvalue, expression=prates[i]))
            self.add_parameter(parameters)
            paramd[rvalue]=parameters

        k_travel=gillespy2.Parameter(name='k_travel', expression=advrate)
        self.add_parameter(k_travel)

        #
        # Model Variables
        #

        speciesd={}
        for rvalue in modelspace()[0]['values']:
            species=[]
            for model_var in [x['name'] for x in modelvariables()]:
                species.append(gillespy2.Species(
                    name=model_var+rvalue, initial_value=initvalue(model_var,modelspace()[0]['name'],rvalue)))
            self.add_species(species)
            speciesd[rvalue]=species
        #
        # Processes and Advection
        #

        reactions=[]
        i=0
        modelprocesses=[f['implementation'] for f in dynfactor.get_processes('Gillespie')]
        for rvalue in modelspace()[0]['values']:
            species=speciesd[rvalue]
            parameters=paramd[rvalue]
            for proc in modelprocesses:
                react=proc(species,parameters)
                reactions.append(gillespy2.Reaction(
                    name=react['name']+rvalue, rate=react['rate'], \
                    reactants=react['reactants'],\
                    products=react['products']))

        ## Advection
        for rvalue in modelspace()[0]['values']:
            species=speciesd[rvalue]
            parameters=paramd[rvalue]
            for rvalue_to in [ x for x in modelspace()[0]['values'] if x != rvalue]:
                species1=speciesd[rvalue_to]
                for k in range(len(modelvariables())):
                    reactions.append(gillespy2.Reaction(
                        name="r_travel"+rvalue+\
                            rvalue_to+modelvariables()[k]['name'], rate=k_travel,\
                        reactants={species[k]:1}, products={species1[k]:1}))

        self.add_reaction(reactions)

        # Set the timespan for the simulation.
        self.timespan(P.linspace(0, maxt, maxt+1))


def build_factors_graph(filename,spacefactor,dynfactor,parfactor):
    """
    Build a graph fo the model factors and save it in dot format.
    Args:
       filename: Name for the graph file. The extention .dot will be added
       spacefactor: Space Factor (framework.Space_Factor)
       dynfactor: Dynamics Factor (framework.Dynamics_Factor)
       parfactor: Parameters Factor (framework.Parameter_Factor)
    """

    with open(filename+'.dot','w') as file:
        #
        # Graph Header
        #
        file.write('digraph test { \n')
        file.write('rankdir=TP \n')
        file.write('forcelabels=true compound=true\n')
        file.write('graph [fontname = "helvetica"] \n')
        file.write('node [fontname = "helvetica"] \n')
        file.write('edge [fontname = "helvetica"] \n')
        file.write('size="6,2" \n')
        file.write('ranksep=0.1 \n')
        file.write('fontsize=10 \n')

        spacefactor.to_dot(file)
        dynfactor.to_dot(file)
        parfactor.to_dot(file)
        file.write('}') # Close Graph
