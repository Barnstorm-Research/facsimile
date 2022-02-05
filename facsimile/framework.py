import functools as F
import scipy.integrate as SI
import numpy as N
import pylab as P
import gillespy2
import facsimile.fermi as fermi
import pprint

class DynamicsFactor:
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
        self.variables.append({'name':name,'indices':indices})
        return
    def add_process(self, name,source,moc,fun,indices=[]):
        names=[p['name'] for p in self.processes]
        imp={'source':source,'moc':moc,'function':fun}
        if name in names:
            i=names.index(name)
            self.processes[i]['implementations'].append(imp)
        else:
            self.processes.append({'name':name,'implementations':[imp],'indices':indices})

        return

    def get_variables(self):
        return self.variables
    def get_processes(self,moc=[]):
        if not moc:
            return self.processes
        else:
            a=sum([f['implementations'] for f in self.processes],[])
            return  [{'implementation':h['function'],\
                              'name':h['function'].__name__} for h in a if h['moc']==moc]


class SpaceFactor:
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
        self.indices.append({'name':name,'values':values})
        return
    def add_advection(self, name,index ,fun):
        self.advections[index]={'name':name,'implementation':fun}
        return

    def get_space(self):
        space=[]
        for ind in self.indices:
            if ind['name'] in self.advections:
                ind['advection']=self.advections[ind['name']]
            space.append(ind)
        return space


class ParameterFactor:
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
        self.parameters.append({'name':name,'implementation':fun})

    def get_parameters(self):
        return self.parameters



#######################################################
# FRAMEWORK FUNCTIONS
#######################################################

def distribute_to_ode(space,dynamics,parameters):
    """
    This functionn is the "inverse" of factorization. It takes as inputs the 2 factors, space and dynamics, and
    outputs the SIR model in ODE form.
    :param space:
    :param dynamics:
    :return:
    """

    # TODO: This assumes one index only
    indexvalues = space.get_space()[0]['values']
    advoper = space.get_space()[0]['advection']['implementation']
    var = [vv['name'] for vv in dynamics.variables]

    dynv= [p['implementation'] for p in dynamics.get_processes('ODE')]
    
    #paramf=lambda indexv : fermi.fermi(fquery,indexv)

    params=parameters.get_parameters()
    def paramf(indexv):
        return [p['implementation'](indexv)  for p in params ]


    mapfun = lambda l : lambda t,y :  dyn(t,y,l)
    redfun=lambda f1,f2: lambda t,x : f1(t,x[:-len(var)])+f2(t,x[-len(var):])

    dyn = lambda t,y,indexvalue,dynv=dynv : [sum(a) for a in zip(*map(lambda f:f(t,y,paramf(indexvalue)),dynv))]
    vdyn = list(map(lambda l,indexvalues=indexvalues : lambda t,y :  dyn(t,y,l),indexvalues))
    vout=lambda t,y,redfun=redfun,vdyn=vdyn :  [sum(a) for a in zip(F.reduce(redfun,vdyn)(t,y) ,  applyadv(advoper,var,indexvalues)(y))]
    return vout

def applyadv(advoper, var, indexvalues):
    """
    This is an utility function to apply the advection operator to the whole model.
    It's called by distribute only.
    :param advoper:
    :param var:
    :param indexvalues:
    :return:
    """
    aff=list()
    for i in range(len(indexvalues)):
        for j in range(len(var)):
           aff.append(lambda y,i=i,j=j: \
                      advoper(y[j+i*len(var)],y[j:len(var)*(len(indexvalues)):len(var)]))
    aadv=lambda y : [fff(y) for fff in aff]
    return aadv






                
#######################################################
# Model rendering and simulation  FUNCTIONS
#######################################################



def bvp(modelprocesses):
    """

    :param modelprocesses:
    :return:
    """
    # model assembly
    space =[ provinces() , travel]
    dynamics = [modelvariables(), modelprocesses(),'infrecrates']
    model=distribute_to_ode(space,dynamics)
    t=P.linspace(0,100,10)
    def bc(ya,yb):
        an = [(ya[0]-1000),yb[1]-300,ya[2], (ya[3]-1000), (yb[4]-450),ya[5]]
        return P.array(an)
        

    y_i = list(range(6))
    
    y_i[0]=[1000 for a in t]
    y_i[1]=[100 for a in t]
    y_i[2]=[100 for a in t]
    y_i[3]=[1000 for a in t]
    y_i[4]=[100 for a in t]
    y_i[5]=[100 for a in t]
    print(y_i)
    y_i = P.array(y_i)
    
    res_a = SI.solve_bvp(model, bc, t, y_i,tol=.01)
    return res_a




class Distribute_to_gillespie(gillespy2.Model):

    def __init__(self, dynfactor,spacefactor,parfactor,initvalue,maxt):
        """

        :param modelprocesses:
        :param modelspace:
        :param modelvariables:
        :param initvalue:
        :param advrate:
        :param parameter_query:
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
        paramd=dict()
        params=parfactor.get_parameters()

        for r in modelspace()[0]['values']:
            parameters = list()
            #prates= fermi.fermi(parameter_query,r)
            prates=[p['implementation'](r)  for p in params ]
            for i in range(len(prates)):
                parameters.append(gillespy2.Parameter(
                    name='k_c'+str(i)+r, expression=prates[i]))
            self.add_parameter(parameters)
            paramd[r]=parameters
            
        k_travel=gillespy2.Parameter(name='k_travel', expression=advrate)
        self.add_parameter(k_travel)
        
        #
        # Model Variables
        #
    
        speciesd=dict()
        for r in modelspace()[0]['values']:
            species=list()
            for mv in [x['name'] for x in modelvariables()]:
                species.append(gillespy2.Species(name=mv+r, initial_value=initvalue(mv,r)))
            self.add_species(species)
            speciesd[r]=species
        #
        # Processes and Advection
        #
        
        reactions=list()
        i=0
        modelprocesses=[f['implementation'] for f in dynfactor.get_processes('Gillespie')]
        for r in modelspace()[0]['values']:
            species=speciesd[r]
            parameters=paramd[r]
            for re in modelprocesses:
                react=re(species,parameters)
                reactions.append(gillespy2.Reaction(
                    name=react['name']+r, rate=react['rate'], \
                    reactants=react['reactants'],\
                    products=react['products']))

        ## Advection
        for r in modelspace()[0]['values']:
            species=speciesd[r]
            parameters=paramd[r]
            for rd in [ x for x in modelspace()[0]['values'] if x != r]:
                species1=speciesd[rd]
                parametersd=paramd[rd]
                for k in range(len(modelvariables())):
                     reactions.append(gillespy2.Reaction(
                        name="r_travel"+r+rd+modelvariables()[k]['name'], rate=k_travel,\
                        reactants={species[k]:1}, products={species1[k]:1}))

        self.add_reaction(reactions)
        
        # Set the timespan for the simulation.
        self.timespan(P.linspace(0, maxt, maxt+1))


def makeSDgraph(filename,spacefactor,dynfactor,parfactor):
    """

    :return:
    """
    mss=spacefactor.indices
    mssa=spacefactor.advections
    with open(filename+'.dot','w') as f:
        f.write('digraph test { \n')
        f.write('rankdir=TP \n')
        f.write('forcelabels=true compound=true\n')
        f.write('graph [fontname = "helvetica"] \n')
        f.write('node [fontname = "helvetica"] \n')
        f.write('edge [fontname = "helvetica"] \n')

        f.write('size="6,2" \n')
        f.write('ranksep=0.1 \n')
        f.write('fontsize=10 \n')
        f.write('subgraph clusterspace { \n')
        f.write('label = SPACE_Factor  \n')
        f.write('rankdir=LR \n')
        #mss=modelspace()
        start=True
        for l in mss:
            f.write('subgraph cluster'+l['name']+' {label ="'+l['name']+'"\n')
            f.write(l['name']+'a '+' [label="",style=invis,width=0] \n')
            for value in l['values']:
                f.write(value+' [shape=box,fontsize=10] \n')
            f.write('}')
            if start:
                lo=l['name']+'a'
                start=False
            else:
                f.write(lo+' -> '+l['name']+'a [style=invis]\n')
                lo=l['name']+'a'
            if l['name'] in mssa:
            #if 'advection' in l:
                advname=mssa[l['name']]['name']
                f.write(advname+' [shape=oval,fontsize=10] \n')
                f.write(lo+ '  -> ' + advname+ \
                        '[ltail = cluster'+l['name']+\
                        ',color=blue,penwidth=3]\n')
                f.write(advname + \
                        ' -> '+lo+' [lhead = cluster'+l['name']+ \
                        ',color=blue,penwidth=3] \n')
                lo=advname
                
        f.write('}')
        f.write('subgraph clusterparams { \n')
        f.write('label = Parameters_Factor  \n')
        f.write('paramsa '+' [label="",style=invis,width=0] \n')
        f.write(lo+' -> '+'paramsa [style=invis]\n')
        for l in parfactor.parameters:
            f.write(l['name']+' [shape=box, fontsize=10, label='+l['name']+' ] \n')
        f.write('}')
        
        f.write('subgraph clusterDynamics { \n')
        f.write('label = DYNAMICS_Factor  \n')
        f.write('subgraph clusterEmpty  { \n')
        f.write('label = "Diagram" \n fontcolor = black \n')
        mv=dynfactor.variables
        for l in mv:
            f.write(l['name']+' [shape=box, fontsize=10,label=<'+l['name']+\
                    '<BR /><FONT POINT-SIZE="5">'+ \
                    ', '.join(l['indices'])+ '</FONT>> ] \n')

        #pv=[p['name'] for p in modelprocessesO()]
        #for p in modelprocessesO():
        indlist=[a['indices'] for a in dynfactor.get_processes()]
        for p,indices  in zip(dynfactor.get_processes('ODE'),indlist):
            f.write(p['name']+' [shape=oval, fontsize=10,label=<'+p['name']+\
                    '<BR /><FONT POINT-SIZE="5">'+ \
                    ', '.join(indices)+ '</FONT>> ] \n')
            d=p['implementation'](0,[1 for x in range(len(mv))])
            sources = [i for i in range(len(d)) if d[i]<0]
            dest = [i for i in range(len(d)) if d[i]>0]
            for i in sources:
                f.write(mv[i]['name']+' -> '+p['name'] +'[color=green,penwidth=3]\n')
            for j in dest:
                f.write(p['name']+ ' -> ' + mv[j]['name']+ '[color = green,penwidth=3]\n')
        f.write('}\n')
        f.write('subgraph clusterImplementations  { \n')
        f.write('label = "Implementations" \n fontcolor = black \n')
        start=True
        for p in dynfactor.processes:
            mocs=[','.join([pm['moc'],pm['source'],'<BR />']) for pm in p['implementations']]
            f.write(p['name']+'i [shape=oval, fontsize=10,label=<'+p['name']+\
                    '<BR /><FONT POINT-SIZE="5">'+ \
                    ' '.join(mocs)+ '</FONT>> ] \n')
            if start:
                lo=p['name']+'i'
                start=False
            else:
                f.write(lo+' -> '+p['name']+'i [style=invis]\n')
                lo=p['name']+'i'
        f.write('}\n')
        f.write('}\n')

        f.write('}')


