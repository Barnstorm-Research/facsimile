<!-- markdownlint-disable -->

<a href="../../facsimile/framework.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `framework.py`





---

<a href="../../facsimile/framework.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `distribute_to_ode`

```python
distribute_to_ode(space, dynamics, parameters)
```

This functionn is the "inverse" of factorization. It takes as inputs the 2 factors, space and dynamics, and outputs the SIR model in ODE form. :param space: :param dynamics: :return: 


---

<a href="../../facsimile/framework.py#L136"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `applyadv`

```python
applyadv(advoper, var, indexvalues)
```

This is an utility function to apply the advection operator to the whole model. It's called by distribute only. :param advoper: :param var: :param indexvalues: :return: 


---

<a href="../../facsimile/framework.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `bvp`

```python
bvp(modelprocesses)
```

:param modelprocesses: :return: 


---

<a href="../../facsimile/framework.py#L286"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `makeSDgraph`

```python
makeSDgraph(filename, spacefactor, dynfactor, parfactor)
```

:return: 


---

## <kbd>class</kbd> `Distribute_to_gillespie`




<a href="../../facsimile/framework.py#L200"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(dynfactor, spacefactor, parfactor, initvalue, maxt)
```

:param modelprocesses: :param modelspace: :param modelvariables: :param initvalue: :param advrate: :param parameter_query: 





---

## <kbd>class</kbd> `DynamicsFactor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_process`

```python
add_process(name, source, moc, fun, indices=[])
```





---

<a href="../../facsimile/framework.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_variable`

```python
add_variable(name, indices=[])
```





---

<a href="../../facsimile/framework.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_processes`

```python
get_processes(moc=[])
```





---

<a href="../../facsimile/framework.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_variables`

```python
get_variables()
```






---

## <kbd>class</kbd> `ParameterFactor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_parameter`

```python
add_parameter(name, fun)
```





---

<a href="../../facsimile/framework.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_parameters`

```python
get_parameters()
```






---

## <kbd>class</kbd> `SpaceFactor`
Hold the data for a dynamic factor 

<a href="../../facsimile/framework.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__()
```








---

<a href="../../facsimile/framework.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_advection`

```python
add_advection(name, index, fun)
```





---

<a href="../../facsimile/framework.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `add_index`

```python
add_index(name, values)
```





---

<a href="../../facsimile/framework.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_space`

```python
get_space()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
