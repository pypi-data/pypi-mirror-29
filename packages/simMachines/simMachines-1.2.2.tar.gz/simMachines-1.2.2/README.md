# simMachines Python Wrapper

simMachines is a Python 3 wrapper for the simMachines API. Further documentation can be found in simMachines's API Manual. 

## Requirements
Python modules required: numpy, pandas, requests

Also, you will need your simMachines username and password to authenticate into the wrapper.

## Installation
*Note: simMachines is only compatible with versions of Python 3 or later.*

To start using simMachines, run:
`pip install simMachines`

## Authentication
The following code will authenticate you into your simMachines's environment (for example purposes, this is being run locally)

```python
from simMachines import Authenticate
client =  Authenticate(path = '127.0.0.1'
                      , https = False, port = 9090
                      , username = 'YOUR_USERNAME'
                      , password = 'YOUR_PASSWORD')
```

If `username` and `password` are not passed to `Authenticate()`, you will be prompted to enter them.

# Examples
Usage examples can be found here: https://github.com/simMachines/solutions_notebooks/tree/master/PythonAPIWrapper/simMachines/examples
