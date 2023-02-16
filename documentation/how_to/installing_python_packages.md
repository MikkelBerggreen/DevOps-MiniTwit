# Working with python packages

## Installation

Installation of requirements.txt is part of the process with the Dockerfile. 
Not necessary but generally to install:

> pip install -r requirements.txt

## Adding new dependencies

Step 1. To install a package:

> pip install package_name

Step 2. To freeze the dependencies.

> echo \ >> requirements.txt & pip freeze | tr -d '\n' >> requirements.txt

Explanation: Since the installed dependencies from the Docker file are not shown when running pip freeze and it only  shows the manually installed package, it must be appended to requirements.txt.

echo \ is to add a new line to the file. 
| tr -d '\n\ strips a new line that pip freeze generates after which would add a lot of unecessary lines. 

The result is appended to requirements.txt.

