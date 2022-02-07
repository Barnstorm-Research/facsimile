<!-- markdownlint-disable -->

<a href="../../facsimile/demo.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `demo`
Demonstration script to assemble, render and run SIR models 


---

<a href="../../facsimile/demo.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simul_o`

```python
simul_o(nreg=3, nproc=2)
```

Distribute the SIR Factors into an ODE based simulation runs the simulation and plots the results 

**Args:**
 
 - <b>`nreg`</b>:  Number of regions to be used (default 3) 
 - <b>`nproc`</b>:  Number of processes to be used  2 (inf, rec) or 3 (inf,rec,reinf) 

**Returns:**
 
 - <b>`[tv,yv]`</b>:  Time vectot and values vector 
 - <b>`model`</b>:  ODE based model function 




---

<a href="../../facsimile/demo.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `simul_g`

```python
simul_g(nreg=3, nproc=2)
```

Distribute the SIR Factors into an Gillespie based simulation runs the simulation and plots the results 

**Args:**
 
 - <b>`nreg`</b>:  Number of regions to be used (default 3) 
 - <b>`nproc`</b>:  Number of processes to be used  2 (inf, rec) or 3 (inf,rec,reinf) 

**Returns:**
 
 - <b>`results`</b>:  Time vector and values vector 
 - <b>`model`</b>:  Gillespie  based model object 




---

<a href="../../facsimile/demo.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `run_both`

```python
run_both(figuresBlock=True)
```

Run Both ODE and GIllespie simulations 

**Args:**
 
 - <b>`figuresBlock`</b>:  If true, then the plots block the function 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
