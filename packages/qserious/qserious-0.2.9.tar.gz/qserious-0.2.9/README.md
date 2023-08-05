
# qserious

[![PyPI version](https://badge.fury.io/py/qserious.svg)](https://badge.fury.io/py/qserious)
[![Build Status](https://travis-ci.org/pyKilt/qserious.svg?branch=master)](https://travis-ci.org/pyKilt/qserious)

``` sh
pip install qserious
```

``` py
from qserious import deserialize

print deserialize('nested[value]=foobar&foo=bar&hola=caracola&adios=caracol')

# output: {'hola':'caracola','adios':'caracol','foo':'bar','nested':{'value': 'foobar'}}
```

``` py
from qserious import serialize

print serialize({'hola':'caracola','adios':'caracol','foo':'bar','nested':{'value': 'foobar'}})

# output: 'nested[value]=foobar&foo=bar&hola=caracola&adios=caracol'
```
