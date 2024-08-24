CountryPy
=========

<img align="left" src="http://estruyf-github.azurewebsites.net/api/VisitorHit?user=ArjunSharda&repo=CountryPy&countColorcountColor&countColor=%237B1E7B"/>
<img align="right" src="https://img.shields.io/github/repo-size/ArjunSharda/CountryPy?style=for-the-badge&logo=appveyor" alt="GitHub repo size"/>

![CountryPy](https://socialify.git.ci/ArjunSharda/CountryPy/image?description=1&descriptionEditable=%F0%9F%97%BA%EF%B8%8F%20A%20lightweight%20%26%20efficient%20library%20for%20fetching%20country%20data.&font=Raleway&forks=1&issues=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2FArjunSharda%2FCountryPy%2Fmain%2Fext%2FCountryPy.png&name=1&owner=1&pattern=Signal&pulls=1&stargazers=1&theme=Auto)

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

Search
-----------
```python
>>> from countrypy import Search
>>> searching = Search(Search.timezones, "UTC-12:00")
>>> print(searching)
'United States'
```

CLI Quick Start
---------------
```bash
$ countrypy quickinfo US
```
Take a look at more examples in the [examples](https://github.com/ArjunSharda/CountryPy/tree/main/examples) folder!

v1.1.0 Changes
--------------
v1.1.0
- **[ADDED]** Added `Search` option & `search_by` for CLI - you can now sort countries by data such as timezones & languages!
- **[ADDED]** Added more error handling
- **[MODIFIED]** Changed API URL to use filters to reduce load time
- **[PATCH]** Fixed a bug for both CLI and non-cli with phone country codes and their suffixes


## Want to contribute?
Take a look at the [contributing guidelines](CONTRIBUTING.md)!

<hr>
<h6 align="center">© Arjun Sharda 2024-present
<br>
All Rights Reserved</h6>
