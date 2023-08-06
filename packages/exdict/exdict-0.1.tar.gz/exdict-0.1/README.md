

# Exdict

I created this extension to Python dictionary because sometimes I wanted a quick way of creating an object with attributes. Moreover, I wanted the hability to load this object from other data types like standard dictionaries, YAML files and whatever needed.

## Instalation

     pip install exdict

## Usage
The usage is quite simple:

    >>> from exdict import Exdict
    >>> exd = Exdict(foo="1")
    >>> exd["bar"] = "2"
    >>> print exd
    {'bar': '2', 'foo': '1'}
    >>> print exd["bar"]
    2
    >>> print exd.bar
    2
    >>> exd.bar = 3
    >>> exd["foo"] = 4
    >>> print exd.bar
    3
    >>> print exd.foo
    4

