<!-- markdownlint-disable -->

<a href="../../facsimile/SIRexample.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `SIRexample`





---

<a href="../../facsimile/SIRexample.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_dynamics_factor`

```python
get_dynamics_factor(nproc=3)
```

Create Dynamics Factor for the SIR model There are 3 processes defined in this example, Infection recovery and reinfection the optional parameter nproc dis used to select how many of these 3 are used.  The processes have one reference implementation (ODE) and one translated  implementation (Gillespie) There are threee dynamic variables, S, I and R which are indexed with the Region index 

**Args:**
 
 - <b>`nproc`</b>:  Number of processes (default 2) 

**Returns:**
 (frameowrk.DynamicsFactor) SIR Dynamics Factor 


---

<a href="../../facsimile/SIRexample.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_space_factor`

```python
get_space_factor(nregions=3)
```






---

<a href="../../facsimile/SIRexample.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `initvalue`

```python
initvalue(variable, zone)
```

Return the initial value for a variable in a given Region 



**Args:**
 variable: Dynamic Variable, one of S, I or R zone: Name of the region 

**Returns:**
 double iv: initial value for the variable in the region 


---

<a href="../../facsimile/SIRexample.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_parameters_factor`

```python
get_parameters_factor()
```






---

<a href="../../facsimile/SIRexample.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `infection`

```python
infection(t, y, params=[0.01, 0.001, 0.001])
```

Reference implementation for infection as an ODE 

:param t: time :param y: list of current values of S, I, R :param params: list of model paramters  :return: list with contributions of infection process to S, I, R derivatives 

:math:'\frac{dS}{dt}=-\beta I S' :math:'\frac{dI}{dt}=\beta I S' :math:'\frac{dR}{dt}=0' 


---

<a href="../../facsimile/SIRexample.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `recovery`

```python
recovery(t, y, params=[0.01, 0.001, 0.001])
```

Reference implementation for recovery 

:param t: time :param y: list of current values of S, I, R :param params: list of model paramters  :return: list with contributions of recovery process to S, I, R derivatives 

:math:'\frac{dS}{dt}=0' :math:'\frac{dI}{dt}=-\rho I' :math:'\frac{dR}{dt}=\rho I' 


---

<a href="../../facsimile/SIRexample.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `reinfection`

```python
reinfection(t, y, params=[0.01, 0.001, 0.001])
```

Reference implementation for recovery 

:param t: time :param y: list of current values of S, I, R :param params: list of model paramters  :return: list with contributions of recovery process to S, I, R derivatives 

:math:'\frac{dS}{dt}=0' :math:'\frac{dI}{dt}=\beta I S' :math:'\frac{dR}{dt}=-\beta I R' 


---

<a href="../../facsimile/SIRexample.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `infectionG`

```python
infectionG(y, params)
```

Reference: def infection(t,y,params=[1e-2,1e-3,1e-3]):  beta = params[0]  flow=y[0]*y[1]*beta  return [-flow,flow,0.0] :param y: :param params: :return: 


---

<a href="../../facsimile/SIRexample.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `recoveryG`

```python
recoveryG(y, params)
```

Reference: def recovery(t,y,params=[1e-2,1e-3,1e-3]): rho=params[1] flow = y[1]*rho return [0.0, -flow,flow] :param y: :param params: :return: 


---

<a href="../../facsimile/SIRexample.py#L196"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `reinfectionG`

```python
reinfectionG(y, params)
```

Reference: def reinfection(t,y,params=[1e-2,1e-3,1e-3]):  beta = params[2]  flow=y[1]*y[2]*beta  return [0.0,flow,-flow] :param y: :param params: :return: 


---

<a href="../../facsimile/SIRexample.py#L220"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `travel`

```python
travel(x, y)
```

Advection operator. :param x: population in zone of interest :param y: vector of population in all zones :return: 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
