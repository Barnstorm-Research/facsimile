# Facsimile 0.1

To execute both simulations:

1. Ensure you have created and activated the conda environment from `environment.yml`
2. Run from the repo folder: `python -m facsimile.demo`



## EXAMPLE SIR Model
![](docs/figs/SIRFactoredModel.png)

### SIR FACTORS

#### Dynamics
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

#### Space
```
{'Advections': {'Region': {'implementation': <function travel at 0x130a08700>,
                           'name': 'Travel'}},
 'Indices': [{'name': 'Region',
              'values': ['Metroton', 'Suburbium', 'Ruralia']}]}
```
#### Parameters
```
{'Parameters': [{'implementation': <function get_parameters_factor.<locals>.<lambda> at 0x1052a39d0>,
                 'name': 'Infection_rate'},
                {'implementation': <function get_parameters_factor.<locals>.<lambda> at 0x1052b8ee0>,
                 'name': 'Recovery_rate'},
                {'implementation': <function get_parameters_factor.<locals>.<lambda> at 0x154e70f70>,
                 'name': 'Reinfection_rate'}]}
```


## Simulation Using ODE

![ODE Sim](docs/figs/SIRODE.png)

## Simulation using Gillespie

![Gillespie Sim](docs/figs/SIRG.png)
