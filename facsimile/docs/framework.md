<!-- markdownlint-disable -->

<a href="../../facsimile/framework.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `framework`
This module contains the class and method definitions used to compose, modify and  render factored models into executable simulations 


---

<a href="../../facsimile/framework.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `distribute_to_ode`

```python
distribute_to_ode(space, dynamics, parameters)
```

 This function is the "inverse" of factorization. It takes as inputs 3 factors, space,  dynamics and parameters, and outputs the SIR model in ODE form suitable to be  integrated with scipy.Integrate methods 

**Args:**
 
 - <b>`space`</b>:  Space Factor (framework.SpaceFator) 
 - <b>`dynamics`</b>:  Dynamics Factor 

**Returns:**
 
 - <b>`model`</b>:  ODE function with the signature expected by scipy integrate 




---

<a href="../../facsimile/framework.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `applyadv`

```python
applyadv(advoper, var, indexvalues)
```

This is an utility function to apply the advection operator to the whole model. It's called by distribute only. 


---

<a href="../../facsimile/framework.py#L222"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `bvp`

```python
bvp(modelprocesses)
```

:param modelprocesses: :return: 


---

<a href="../../facsimile/framework.py#L345"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `makeSDgraph`

```python
makeSDgraph(filename, spacefactor, dynfactor, parfactor)
```

Build a graph fo the model factors and save it in dot format. 

**Args:**
 filename: Name for the graph file. The extention .dot will be added spacefactor: Space Factor (framework.SpaceFactor) dynfactor: Dynamics Factor (framework.DynamicsFactor) parfactor: Parameters Factor (framework.ParameterFactor) 


---

<a href="../../facsimile/framework.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DynamicsFactor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_process`

```python
add_process(name, source, moc, fun, indices=[])
```

This Method adds a model process to an existing Dynamics Factor If the process already exists, this method can be used to add addtional modes of computation 

**Args:**
 
 - <b>`name`</b>:  Name of the model process (string) 
 - <b>`source`</b>:  Traceability string (string) 
 - <b>`moc`</b>:  Mode of computation (string) 
 - <b>`fun`</b>:  Function implementing the process for the model of computation specified 
 - <b>`indices `</b>:  List of indices the process depends on. (default []) 

---

<a href="../../facsimile/framework.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_variable`

```python
add_variable(name, indices=[])
```

This Method adds a model variable to an existing Dynamics Factor 

**Args:**
 
 - <b>`name`</b>:  Name of the model variable 
 - <b>`indices `</b>:  List of indices the variable depends on. (default []) 

---

<a href="../../facsimile/framework.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_processes`

```python
get_processes(moc=[])
```

Get the dynamic processes of the factor for a set of mocs. If the moc parameter is empty, return all the known mocs for each  process 

**Args:**
 moc (list): List of models of computation (default []) 

**Returns:**
 list: model processes 

---

<a href="../../facsimile/framework.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_variables`

```python
get_variables()
```

Get the Dynamic variables for the factor 

**Returns:**
 list: list of model variables 


---

<a href="../../facsimile/framework.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SpaceFactor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_advection`

```python
add_advection(name, index, fun)
```

This Method adds a new advection operator to an existing Space Factor 

**Args:**
 
 - <b>`name`</b>:  Name of the advection operator 
 - <b>`index`</b>:  Name of the index over which this advection operates 
 - <b>`fun`</b>:  function implementing the advection operator 

---

<a href="../../facsimile/framework.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_index`

```python
add_index(name, values)
```

This Method adds a new index type, and the corresponding values  to an existing Space Factor 

**Args:**
 
 - <b>`name`</b>:  Name of the Index type 
 - <b>`values`</b>:  List of values for the index type. 

---

<a href="../../facsimile/framework.py#L121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_space`

```python
get_space()
```






---

<a href="../../facsimile/framework.py#L130"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ParameterFactor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_parameter`

```python
add_parameter(name, fun)
```

This Method adds a new parameter to the Parameter Factor 

**Args:**
 
 - <b>`name`</b>:  Parameter name 
 - <b>`fun`</b>:  Function implementing a query to obtain the value of the parameter for a given condition 

---

<a href="../../facsimile/framework.py#L154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parameters`

```python
get_parameters()
```






---

<a href="../../facsimile/framework.py#L255"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Distribute_to_gillespie`




<a href="../../facsimile/framework.py#L257"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(dynfactor, spacefactor, parfactor, initvalue, maxt)
```

This function  is the "inverse" of factorization. It takes as inputs 3 factors, space, dynamic  parameters and outputs the SIR model in Reaction  form suitable to be integrated  with the Gillespy toolbox 

**Args:**
 space: Space Factor (framework.SpaceFator) dynamics: Dynamics Factor 

**Returns:**
 model: Gillespy Reaction model 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._