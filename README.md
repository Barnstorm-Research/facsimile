# Facsimile 0.1

To execute both simulations:

1. Ensure you have created and activated the conda environment from `environment.yml`
2. Run from the repo folder: `python -m facsimile.demo`



## EXAMPLE SIR Model
![](docs/figs/SIRFactoredModel.png)

### SIR FACTORS

#### Dynamics (`SIRdyn`)
```
{'Processes': [{'implementations': [{'function': <function infection at 0x130a083a0>,
                                     'moc': 'ODE',
                                     'source': 'reference'},
                                    {'function': <function infectionG at 0x130a08550>,
                                     'moc': 'Gillespie',
                                     'source': 'translated'}],
                'indices': ['Region'],
                'name': 'infection'},
               {'implementations': [{'function': <function recovery at 0x130a08430>,
                                     'moc': 'ODE',
                                     'source': 'reference'},
                                    {'function': <function recoveryG at 0x130a085e0>,
                                     'moc': 'Gillespie',
                                     'source': 'translated'}],
                'indices': ['Region'],
                'name': 'recovery'},
               {'implementations': [{'function': <function reinfection at 0x130a084c0>,
                                     'moc': 'ODE',
                                     'source': 'reference'},
                                    {'function': <function reinfectionG at 0x130a08670>,
                                     'moc': 'Gillespie',
                                     'source': 'translated'}],
                'indices': ['Region'],
                'name': 'reinfection'}],
 'Variables': [{'indices': 'Region', 'name': 'S'},
               {'indices': 'Region', 'name': 'I'},
               {'indices': 'Region', 'name': 'R'}]}

```

#### Space (`SIRspace`)
```
{'Advections': {'Region': {'implementation': <function travel at 0x130a08700>,
                           'name': 'Travel'}},
 'Indices': [{'name': 'Region',
              'values': ['Metroton', 'Suburbium', 'Ruralia']}]}
```
#### Parameters (`SIRparameters`)
```
{'Parameters': [{'implementation': <function get_parameters_factor.<locals>.<lambda> at 0x1052a39d0>,
                 'name': 'Infection_rate'},
                {'implementation': <function get_parameters_factor.<locals>.<lambda> at 0x1052b8ee0>,
                 'name': 'Recovery_rate'},
                {'implementation': <function get_parameters_factor.<locals>.<lambda> at 0x154e70f70>,
                 'name': 'Reinfection_rate'}]}
```


## Example Workflows

### ODE based Simulation

The workflow for ODE based simulation proceeds in the following steps:

1. Assemble space, dynamics and parameters factors into a model suitable for  ODE simulation: `model=F.distribute_to_ode(SIRspace,SIRdyn,SIRparams)`
1. Select initial conditions `y0` and simulation end time `maxt`
1. Attach the model to a Runge Kutta engine: `out = SI.RK45(model,0,y0,maxt)`
1. Simulate and plot the results

![ODE Sim](docs/figs/SIRODE.png)

### Gillespie algorithm stochastic simulation

The workflow for stochastic simulation is analogous as ODE:

1. Select initial conditions `y0` and simulation end time `maxt`
1. Assemble space, dynamics and parameters factors into a model suitable for stochastic simulation: `model = F.Distribute_to_gillespie(SIRdyn,SIRspace,SIRparameters,y0,maxt)`
1. Simulate and plot 10 stochastic runs (the gillespie model includes a simulation engine) `    results = model.run(number_of_trajectories=10)`


![Gillespie Sim](docs/figs/SIRG.png)
