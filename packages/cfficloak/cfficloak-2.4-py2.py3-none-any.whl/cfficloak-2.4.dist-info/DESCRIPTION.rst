cfficloak - A simple but flexible module for creating object-oriented, pythonic CFFI wrappers.
This is an extension of cffiwrap from https://bitbucket.org/memotype/cffiwrap

The intention is to more fully wrap/hide binary extensions build with cffi to improve auto-completion, inspection of objects and reading/writing/copying/assigning to c objects, especially structs and unions.
Wrapped functions provide a number of auto-conversion to/from types with error handling and output pointer argument creation.
Function skeletons can provide python definitions of c functions to improve auto-compiletion in python code and declaration of out args, error checking and default arguments.
Structs can take numpy arrays assigned to array elements and handle two-way linking for you without any copies.
There are a number of other utilities and wrappers provided to simpliy usage of cffi modules in day-to-day coding.

Install with 
# pip install cfficloak

Automatic documentation is here: http://cfficloak.readthedocs.org/

Copyright (c) 2017, Andrew Leech <andrew@alelec.net>

Original cffiwrap copyright (c) 2013, Isaac Freeman <memotype@gmail.com>
All rights reserved.

Licensed under Apache License, Version 2.0.
See LICENSE.txt for licensing details.


