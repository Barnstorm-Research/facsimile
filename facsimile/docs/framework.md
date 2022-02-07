<!-- markdownlint-disable -->

<a href="../../facsimile/framework.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `framework`
This module contains the class and method definitions used to compose, modify and render factored models into executable simulations 


---

<a href="../../facsimile/framework.py#L281"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../facsimile/framework.py#L317"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `apply_advection`

```python
apply_advection(advoper, var, indexvalues)
```

This is an utility function to apply the advection operator to the whole model. It's called by distribute only. 


---

<a href="../../facsimile/framework.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `build_factors_graph`

```python
build_factors_graph(filename, spacefactor, dynfactor, parfactor)
```

Build a graph fo the model factors and save it in dot format. 

**Args:**
 
 - <b>`filename`</b>:  Name for the graph file. The extention .dot will be added 
 - <b>`spacefactor`</b>:  Space Factor (framework.Space_Factor) 
 - <b>`dynfactor`</b>:  Dynamics Factor (framework.Dynamics_Factor) 
 - <b>`parfactor`</b>:  Parameters Factor (framework.Parameter_Factor) 


---

<a href="../../facsimile/framework.py#L13"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Dynamics_Factor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../facsimile/framework.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_variable`

```python
add_variable(name, indices=[])
```

This Method adds a model variable to an existing Dynamics Factor 

**Args:**
 
 - <b>`name`</b>:  Name of the model variable 
 - <b>`indices `</b>:  List of indices the variable depends on. (default []) 

---

<a href="../../facsimile/framework.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../facsimile/framework.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_variables`

```python
get_variables()
```

Get the Dynamic variables for the factor 

**Returns:**
 list: list of model variables 

---

<a href="../../facsimile/framework.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dot`

```python
to_dot(file)
```

Build Dynamics Factor subgraph in dot format 

**Args:**
 
 - <b>`f`</b>:  file object 


---

<a href="../../facsimile/framework.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Space_Factor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../facsimile/framework.py#L150"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_index`

```python
add_index(name, values)
```

This Method adds a new index type, and the corresponding values to an existing Space Factor 

**Args:**
 
 - <b>`name`</b>:  Name of the Index type 
 - <b>`values`</b>:  List of values for the index type. 

---

<a href="../../facsimile/framework.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_space`

```python
get_space()
```

Create a list object with indices and advections 

**Returns:**
  list of indices with their advections 

---

<a href="../../facsimile/framework.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dot`

```python
to_dot(file)
```

Write to file a subgraph  in dot format with the space factor 


---

<a href="../../facsimile/framework.py#L227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Parameter_Factor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L232"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L241"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `add_parameter`

```python
add_parameter(name, fun)
```

This Method adds a new parameter to the Parameter Factor 

**Args:**
 
 - <b>`name`</b>:  Parameter name 
 - <b>`fun`</b>:  Function implementing a query to obtain the value of the parameter for a given condition 

---

<a href="../../facsimile/framework.py#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_parameters`

```python
get_parameters()
```

Return List object with the factor parameters 

---

<a href="../../facsimile/framework.py#L258"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dot`

```python
to_dot(file)
```

Build Parameter Factor Subgraph In the dot format 

**Args:**
 
 - <b>`f`</b>:  file object 


---

<a href="../../facsimile/framework.py#L335"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Distribute_to_gillespie`
Class to hold model in Gillespie form Inherits from gillespy2.Model 

<a href="../../facsimile/framework.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(dynfactor, spacefactor, parfactor, initvalue, maxt)
```

This function is the "inverse" of factorization. It takes as inputs 3 factors, space, dynamic parameters and outputs the SIR model in Reaction  form suitable to be integrated with the Gillespy toolbox 

**Args:**
 space: Space Factor (framework.SpaceFator) dynamics: Dynamics Factor 

**Returns:**
 model: Gillespy Reaction model 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
