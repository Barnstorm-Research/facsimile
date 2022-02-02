import scipy.integrate as SI
import numpy as N
import pylab as P
import gillespy2
import SIRexample as S
import facsimile as F


def simul():
    # model assembly
    modelspace = S.modelspace()
    travel=S.travel
    modelvariables=S.modelvariables()
    modelprocesses=S.getprocessimplementation('ODE')
    fquery='infrecrates'
    initvalue=S.initvalue
    
    space=[modelspace,travel]
    dynamics=[modelvariables, modelprocesses,'infrecrates']
    model=F.distribute_to_ode(space,dynamics)

    # simulation
    maxt=100 # maximum time of simulation
    
    y0=[1000,0,0,1000,0,0,1000,100,10] # Initial state

    y0=list()
    mvss=[mm['name'] for mm in modelvariables]
    for r in modelspace[0]['values']:
        for mv in mvss:
            y0.append(initvalue(mv,r))
    
    out = SI.RK45(model,0,y0,maxt)

    tv=list()
    yv=list()
    t=0
    while t< maxt:
        out.step()
        t=out.t
        tv.append(out.t)
        yv.append(list(out.y))


    c=[95*(1-P.e**(-t/40))+5 for t in tv]
        
    # positivity rate
    p=[0]
    yo=yv[0]
    to=tv[0]
    for (t,y) in zip(tv[1:],yv[1:]):
        p.append((y[4]-yo[4]-yo[5]+y[5])/(t-to))
        yo=y
        to=t
    P.figure()
    P.plot(tv,p,label='infection rate (Idot)',linewidth=2)
    P.plot(tv,c,label= 'Coverage (% of new infections  getting tested',linewidth=2)
    P.plot(tv,[pp*cc/100.0 for (pp,cc) in zip(p,c)], label='New positive tests',linewidth=2)
    P.legend()
    P.grid()

    # plot results
    P.figure()
    regions=space[0][0]['values']

    for j in range(len(regions)):
        #P.figure()
        for i in range(len(dynamics[0])):
            P.plot(tv,[y[i+j*len(dynamics[0])] for y in yv],label= dynamics[0][i]['name'] + ' in Province '+regions[j],linewidth=4)
    P.grid()
    P.title('_'.join([f['name'] for f in modelprocesses]))
    P.legend()
    P.savefig(regions[j]+'SIR.pdf')

    # plot results
    P.figure()
    regions=space[0][0]['values']
    for j in [0,1]:
        for i in [1,2,0]:

        #P.figure()

            P.plot(tv,[y[i+j*len(dynamics[0])] for y in yv],label= dynamics[0][i]['name'] + ' in Province '+regions[j],linewidth=4)
    P.grid()
    P.title('_'.join([f['name'] for f in modelprocesses]))
    P.legend()
    P.savefig('SIRGcolors.png')

    # plot results
    #P.figure()
    #for i in [1,2,0]:
    #    for j in [1,0]:
    #        P.plot(tv,[y[i+j*len(dynamics[0])] for y in yv],label= dynamics[0][i] + ' in Province '+space[0][j],linewidth=4)
    #        P.grid()
    #        P.legend()
    #    P.savefig(space[0][j]+'SIR.pdf')
    #P.close()
    return model,tv,yv

def assembleg():
    advrate=1e-4
    modelprocesses=[p['implementation'] for p in S.getprocessimplementation('Gillespie')]
    model = F.React(modelprocesses,S.modelspace,S.modelvariables,S.initvalue,advrate,parameter_query='infrecrates')
    results = model.run(number_of_trajectories=10)
    results.plot()
    P.grid()
    P.title('_'.join([f.__name__ for f in S.modelprocessesG()]))
    P.savefig('SIRG.png')
    return results, model



def runboth():
    P.close('all')
    simul()
    fsize=P.gcf().get_size_inches()
    assembleg()
    P.gcf().set_size_inches(fsize)
    P.show(block=False)

