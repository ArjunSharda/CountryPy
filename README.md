CountryPy
=========

# Description

CountryPy is a lightweight & efficient modern country data library, used for fetching information about a variety of countries with support for command-line interface (CLI).

Installation
------------
**[Python 3.6+](https://www.python.org/downloads/) is required**
```bash
# MacOS / Linux (via Terminal)
python3 -m pip install -U countrypy

# Windows (via CMD Prompt)
py -3 -m pip install -U countrypy
```

Quick Start
-----------
```python
>>> from countrypy import Country
>>> country = Country("United States of America")
>>> print(f"Capital: {country.capital}")
'Washington, D.C'
```

CLI Quick Start
---------------
```bash
$ countrypy quickinfo US
```
Take a look at more examples in the [examples](https://github.com/ArjunSharda/CountryPy/tree/main/examples) folder!

v1.0 Changes
--------------
v1.0
- **[START]** Start of the CountryPy library


## Want to contribute?
Take a look at the [contributing guidelines](CONTRIBUTING.md)!

<hr>
<h6 align="center">© Arjun Sharda 2024-present
<br>
All Rights Reserved</h6>
