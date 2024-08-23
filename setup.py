from setuptools import setup, find_packages

setup(
    name="CountryPy",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "requests",
        "colorama",
    ],
    entry_points={
        'console_scripts': [
            'countrypy = countrypy.cli:cli',
        ],
    },
    description="A modern python library for country data",
    author="Arjun Sharda",
    author_email="sharda.aj17@gmail.com",
    url="https://github.com/ArjunSharda/CountryPy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
