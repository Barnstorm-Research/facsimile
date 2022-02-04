import scipy.integrate as SI
import numpy as N
import pylab as P
import gillespy2
import facsimile.SIRexample as S
import facsimile.framework as F


def simul_o():
    """

    :return:
    """

    SIRdyn=S.get_dynamics_factor()
    SIRspace=S.get_space_factor()
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
            y0.append(S.initvalue(mv,r))
            
    maxt=100 # maximum time of simulation
    out = SI.RK45(model,0,y0,maxt)

    tv=list()
    yv=list()
    t=0
    while t< maxt:
        out.step()
        t=out.t
        tv.append(out.t)
        yv.append(list(out.y))


    # plot results
    P.figure()

    for j in range(len(regions)):
        #P.figure()
        for i in range(len(SIRdyn.variables)):
            P.plot(tv,[y[i+j*len(SIRdyn.variables)] for y in yv],label= SIRdyn.variables[i]['name'] + ' in Province '+regions[j],linewidth=4)
    P.grid()
    #P.title('_'.join([f['name'] for f in modelprocesses]))
    P.legend()
    P.savefig(regions[j]+'SIR.pdf')

    # plot results
    P.figure()
    for j in [0,1]:
        for i in [1,2,0]:

        #P.figure()

            P.plot(tv,[y[i+j*len(SIRdyn.variables)] for y in yv],label= SIRdyn.variables[i]['name'] + ' in Province '+regions[j],linewidth=4)
    P.grid()
    #P.title('_'.join([f['name'] for f in modelprocesses]))
    P.legend()
    P.savefig('SIRGcolors.png')

    return [tv,yv],model

def simul_g():
    """

    :return:
    """



    SIRdyn=S.get_dynamics_factor()
    SIRspace=S.get_space_factor()
    SIRparameters=S.get_parameters_factor()
    y0=S.initvalue
    maxt=100
    model = F.Distribute_to_gillespie(SIRdyn,SIRspace,SIRparameters,y0,maxt)

    results = model.run(number_of_trajectories=10)
    results.plot()
    P.grid()
#    P.title('_'.join([f.__name__ for f in modelprocesses]))
    P.savefig('SIRG.png')
    return results, model



def runboth(figuresBlock=True):
    """

    :param figuresBlock: If true, then the plots block the function
    :return:
    """
    P.close('all')
    simul_o()
    fsize=P.gcf().get_size_inches()
    simul_g()
    P.gcf().set_size_inches(fsize)
    P.show(block=figuresBlock)

if __name__ == "__main__":
    print("facsimile demo. Running both simulations:")
    runboth(figuresBlock=True)
    print("Good-bye")
