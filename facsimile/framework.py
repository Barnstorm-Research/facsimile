import functools as F
import scipy.integrate as SI
import numpy as N
import pylab as P
import gillespy2
import facsimile.fermi as fermi


class DynamicsFactor:
    ''' 
    Hold the data for a dynamic factor
    '''
    processes = list()
    variables = list()

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
    
#######################################################
# FRAMEWORK FUNCTIONS
#######################################################

def distribute_to_ode(space,dynamics):
    """
    This functionn is the "inverse" of factorization. It takes as inputs the 2 factors, space and dynamics, and
    outputs the SIR model in ODE form.
    :param space:
    :param dynamics:
    :return:
    """
    indexvalues = space[0][0]['values']

    advoper = space[1]
    var = [vv['name'] for vv in dynamics[0]]

    dynv= [p['implementation'] for p in dynamics[1]]
    paramf=lambda indexv : fermi.fermi(dynamics[2],indexv)
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
            ff= lambda y: advoper(y[j+i*len(var)],y[j:j+len(var)*(len(indexvalues)-1):len(var)])
            aff.append(ff)
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




class React(gillespy2.Model):

    def __init__(self, modelprocesses,modelspace,modelvariables,initvalue,advrate,parameter_query=None):
        """

        :param modelprocesses:
        :param modelspace:
        :param modelvariables:
        :param initvalue:
        :param advrate:
        :param parameter_query:
        """
        gillespy2.Model.__init__(self, name='Gillespie')

        #
        # Parameters from FERMI
        #
        paramd=dict()
        for r in modelspace()[0]['values']:
            parameters = list()
            prates= fermi.fermi(parameter_query,r)
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
        self.timespan(P.linspace(0, 100, 101))


def makeSDgraph():
    """

    :return:
    """
    with open('testSD.dot','w') as f:
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
        mss=modelspace()
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
            if 'advection' in l:
                f.write(l['advection']['name']+' [shape=oval,fontsize=10] \n')
                f.write(lo+ '  -> ' + l['advection']['name']+ \
                        '[ltail = cluster'+l['name']+\
                        ',color=blue,penwidth=3]\n')
                f.write(l['advection']['name'] + \
                        ' -> '+lo+' [lhead = cluster'+l['name']+ \
                        ',color=blue,penwidth=3] \n')
                lo=l['advection']['name']
                
        f.write('}')
        f.write('subgraph clusterparams { \n')
        f.write('label = Parameters_Factor  \n')
        f.write('paramsa '+' [label="",style=invis,width=0] \n')
        f.write(lo+' -> '+'paramsa [style=invis]\n')
        for l in parameters():
            f.write(l['name']+' [shape=box, fontsize=10, label='+l['name']+' ] \n')
        f.write('}')
        
        f.write('subgraph clusterDynamics { \n')
        f.write('label = DYNAMICS_Factor  \n')
        f.write('subgraph clusterEmpty  { \n')
        f.write('label = "Diagram" \n fontcolor = black \n')
        mv=modelvariables()
        for l in modelvariables():
            f.write(l['name']+' [shape=box, fontsize=10,label=<'+l['name']+\
                    '<BR /><FONT POINT-SIZE="5">'+ \
                    ', '.join(l['indices'])+ '</FONT>> ] \n')

        #pv=[p['name'] for p in modelprocessesO()]
        for p in modelprocessesO():
            f.write(p['name']+' [shape=oval, fontsize=10,label=<'+p['name']+\
                    '<BR /><FONT POINT-SIZE="5">'+ \
                    ', '.join(p['indices'])+ '</FONT>> ] \n')
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
        for p in modelprocesses():
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


