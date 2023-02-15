# MiniTwit

TO DO


# How to dockerise the app.
To run the application, we suggest using docker and building an image of the app.
For this purpose we created a docker-compose.yml file. 

Instructions on how to build the docker image:
- Locate the docker-compose.yml file inside src directory 
- On VS code: Right click and select "Compose Up" and the image will be built and ran inside docker. 
- Alternatevely, in terminal write  docker-compose build.
- Then write docker-compose up to run the image in docker.

# How to install dependencies

Locate the folder where the requirements.txt file is and write the following to install all dependencies.

> pip install -r requirements.txt

To freeze the dependencies.

> pip freeze > requirements.txt

To install a package and updating it in requirements.txt:

> pip install -U package_name

There can be a case that pip is not installed in the container.
# To install pip
- in terminal write 'apt update'
- after it has done checking for updates. write ' apt install python3-pip'
This will install pip, so dependencies can be downloaded.
