<!-- markdownlint-disable -->

<a href="../../facsimile/fermi.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `fermi`
This is a stand in for the FERMI tool. Computes  zone dependent constants First value is the transmission rate in the zone second number is the recovery rate out of the zone 


---

<a href="../../facsimile/fermi.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `fermi`

```python
fermi(query, indexvalue)
```

Stand in for a call to the Fermi Framework 

**Args:**
 
 - <b>`query`</b>:  string containing the query to pass to Fermi 
 - <b>`indexvalue`</b>:  parameters for the query 

**Returns:**
 
 - <b>`answer`</b>:  Answer to the query returned by Fermi. Empty if the query failed 


---

<a href="../../facsimile/fermi.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `infrecrate`

```python
infrecrate(zone)
```

Stand in for Fermi query execution 

**Args:**
 
 - <b>`zone`</b>:  Region element 

**Returns:**
 
 - <b>`parameters`</b>:  Value of the three parameters 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
