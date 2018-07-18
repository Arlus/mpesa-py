# mpesa-py

  
This is an unofficial wrapper providing convenient access to the Safaricom MPESA Daraja API for applications written in Python.  
  
It has been tested with Python 2 & 3

### Installation

To install the library from Pypi:
``` bash
 pip install mpesa-py 
 ```


To get the latest version of the library.
```bash
pip install git+git://github.com/Arlus/mpesa-py.git#egg=mpesa-py
```

You can also clone or download the library package and install it using setuptools:

``` bash 
python setup.py install
```

### Tests

The library comes with simple integration tests with Safaricom's sandbox APIs. Due to factors beyond my control, the tests are structured to pass even when a specific Daraja API is under maintenance. To run the tests, simply execute pytest from the library's root directory:

``` bash
pytest
```

### Usage

``` python
from mpesa.api.<API> import <API Class>
```
***API***
The following APIs are supported:
-   transaction_status
-   mpesa_express
-   reversal
-   balance
-   auth
-   b2c
-   c2b
-   b2b

***API Class***
The following are the corresponding API classes:
 - TransactionStatus
 - MpesaExpress
 - Reversal
 - Balance
 - MpesaBase
 - B2B
 - C2B
 - B2C
 

### Documentation

For more information about the modules and APIs, please see the [documentation](https://python-mpesa.readthedocs.io/).
