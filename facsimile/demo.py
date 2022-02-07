'''
Demonstration script to assemble, render and run SIR models
'''
import scipy.integrate as SI
import pylab as P
import facsimile.SIRexample as S
import facsimile.framework as F


def simul_o(nreg=3,nproc=2):
    """
    Distribute the SIR Factors into an ODE based simulation
    runs the simulation and plots the results
    Args:
       nreg: Number of regions to be used (default 3)
       nproc: Number of processes to be used  2 (inf, rec) or 3 (inf,rec,reinf)
    Returns:
       [tv,yv]: Time vectot and values vector
       model: ODE based model function
       
    """

    SIRdyn=S.get_dynamics_factor(nproc)
    SIRspace=S.get_space_factor(nreg)
    SIRparams=S.get_parameters_factor()

    print(SIRdyn)
    print(SIRspace)
    print(SIRparams)

    model=F.distribute_to_ode(SIRspace,SIRdyn,SIRparams)



    # simulation
    y0=list()
    mvss=[mm['name'] for mm in SIRdyn.variables]
    regions=SIRspace.get_space()[0]['values']
    for r in regions:
        for mv in mvss:
            y0.append(S.init_value(mv,r))

    maxt=100 # maximum time of simulation
    out = SI.RK45(model,0,y0,maxt,rtol=1e-5,max_step=0.1,atol=1e-5)
    tv=list()
    yv=list()
    t=0
    while out.status=='running':
        out.step()

        t=out.t
        tv.append(out.t)
        yv.append(list(out.y))


    # plot results
    P.figure()

    for j in range(len(regions)):
        #P.figure()
        for i in range(len(SIRdyn.variables)):
            P.plot(tv,[y[i+j*len(SIRdyn.variables)] for y in yv],\
                   label= SIRdyn.variables[i]['name'] + \
                   ' in Province '+regions[j],linewidth=4)
    P.grid()
    #P.title('_'.join([f['name'] for f in modelprocesses]))
    P.legend()

    P.savefig(regions[j]+'SIR.pdf')
    # plot results
    P.figure()
    for j in [0,1]:
        for i in [1,2,0]:
        #P.figure()
            P.plot(tv,[y[i+j*len(SIRdyn.variables)] for y in yv],\
                   label= SIRdyn.variables[i]['name'] + \
                   ' in Province '+regions[j],linewidth=4)
    P.grid()
    #P.title('_'.join([f['name'] for f in modelprocesses]))
    P.legend()
    P.savefig('SIRGcolors.png')

    return [tv,yv],model

def simul_g(nreg=3,nproc=2):
    """
    Distribute the SIR Factors into an Gillespie based simulation
    runs the simulation and plots the results
    Args:
       nreg: Number of regions to be used (default 3)
       nproc: Number of processes to be used  2 (inf, rec) or 3 (inf,rec,reinf)
    Returns:
       results: Time vector and values vector
       model: Gillespie  based model object
       
    """


    SIRdyn=S.get_dynamics_factor(nproc)
    SIRspace=S.get_space_factor(nreg)
    SIRparameters=S.get_parameters_factor()
    y0=S.init_value
    maxt=100
    model = F.Distribute_to_gillespie(SIRdyn,SIRspace,SIRparameters,y0,maxt)

    results = model.run(number_of_trajectories=10)
    results.plot()
    P.grid()
#    P.title('_'.join([f.__name__ for f in modelprocesses]))
    P.savefig('SIRG.png')
    return results, model



def run_both(figuresBlock=True):
    """
    Run Both ODE and GIllespie simulations
    Args:
       figuresBlock: If true, then the plots block the function
    """
    P.close('all')
    simul_o()
    fsize=P.gcf().get_size_inches()
    simul_g()
    P.gcf().set_size_inches(fsize)
    P.show(block=figuresBlock)

if __name__ == "__main__":
    print("facsimile demo. Running both simulations:")
    run_both(figuresBlock=True)
    print("Good-bye")
