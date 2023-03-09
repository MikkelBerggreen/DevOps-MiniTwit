# MiniTwit

MiniTwit is a messaging application being converted from Flask to FastAPI.

It is deployed here:

http://157.245.16.6:8000/


# How to dockerise the app.
To run the application, we suggest using docker and building an image of the app.
For this purpose we created a docker-compose.yml file. 

Instructions on how to build the docker image:
- Locate the docker-compose.yml file inside src directory 
- On VS code: Right click and select "Compose Up" and the image will be built and ran inside docker. 

Alternatevely, you can use terminal commands to achieve the same thing.

>  docker-compose build

>  docker-compose up 


# How to install dependencies

Locate the folder where the requirements.txt file is and write the following to install all dependencies.

> pip install -r requirements.txt

To freeze the dependencies.

> pip freeze > requirements.txt

To install a package and updating it in requirements.txt:

> pip install -U package_name

There can be a case that pip is not installed in the container.
# To install pip

> apt update

> apt install python3-pip

This will install pip, so dependencies can be downloaded.
