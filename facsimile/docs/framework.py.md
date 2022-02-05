<!-- markdownlint-disable -->

<a href="../../facsimile/framework.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `framework.py`





---

<a href="../../facsimile/framework.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../../facsimile/framework.py#L169"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `applyadv`

```python
applyadv(advoper, var, indexvalues)
```

This is an utility function to apply the advection operator to the whole model. It's called by distribute only. 


---

<a href="../../facsimile/framework.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `bvp`

```python
bvp(modelprocesses)
```

:param modelprocesses: :return: 


---

<a href="../../facsimile/framework.py#L317"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `makeSDgraph`

```python
makeSDgraph(filename, spacefactor, dynfactor, parfactor)
```

:return: 


---

## <kbd>class</kbd> `Distribute_to_gillespie`




<a href="../../facsimile/framework.py#L229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(dynfactor, spacefactor, parfactor, initvalue, maxt)
```

This function  is the "inverse" of factorization. It takes as inputs 3 factors, space, dynamic  parameters and outputs the SIR model in Reaction  form suitable to be integrated  with the Gillespy toolbox 

**Args:**
 space: Space Factor (framework.SpaceFator) dynamics: Dynamics Factor 

**Returns:**
 model: Gillespy Reaction model 





---

## <kbd>class</kbd> `DynamicsFactor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_process`

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

<a href="../../facsimile/framework.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_variable`

```python
add_variable(name, indices=[])
```

This Method adds a model variable to an existing Dynamics Factor 

**Args:**
 
 - <b>`name`</b>:  Name of the model variable 
 - <b>`indices `</b>:  List of indices the variable depends on. (default []) 

---

<a href="../../facsimile/framework.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_processes`

```python
get_processes(moc=[])
```

Get the dynamic processes of the factor for a set of mocs. If the moc parameter is empty, return all the known mocs for each  process 

**Args:**
 moc (list): List of models of computation (default []) 

**Returns:**
 list: model processes 

---

<a href="../../facsimile/framework.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_variables`

```python
get_variables()
```

Get the Dynamic variables for the factor 

**Returns:**
 list: list of model variables 


---

## <kbd>class</kbd> `ParameterFactor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_parameter`

```python
add_parameter(name, fun)
```





---

<a href="../../facsimile/framework.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_parameters`

```python
get_parameters()
```






---

## <kbd>class</kbd> `SpaceFactor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_advection`

```python
add_advection(name, index, fun)
```





---

<a href="../../facsimile/framework.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_index`

```python
add_index(name, values)
```





---

<a href="../../facsimile/framework.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_space`

```python
get_space()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
