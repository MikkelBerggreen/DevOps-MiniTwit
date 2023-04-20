###### Main branch
![Lint and Test - Main Branch](https://github.com/MinitwitGroupI/Minitwit/actions/workflows/lint-and-test.yml/badge.svg?branch=main)

###### All branches
![Lint and Test - All Branches](https://github.com/MinitwitGroupI/Minitwit/actions/workflows/lint-and-test.yml/badge.svg)


# MiniTwit

MiniTwit is a messaging application which was converted from Flask to FastAPI framework.

You can find the deployed application [here](https://opsdev.gg) or https://opsdev.gg

![Landing Page](https://github.com//MinitwitGroupI/MiniTwit/blob/main/documentation/images/landingpage.png?raw=true)

# How to install and run the application

Prerequesesites: 
- Docker must be installed.
- Inside src/backend there is a file called ".env_sample". Input all necessary fields and rename the file to ".env".

How to install and run the application:
Inside src/ there is a docker-compose.yml file. Composing this file up will generate all necessary containers, volumes and files to run the application.

Once the containers have been deployed: navigate to http://localhost:8000 to access the main page.

# How to install required dependencies

All required dependencies will be installed once docker-compose file is executed.

However, in the rare case that there is no way to run docker containers. You can find the list of all dependencies [here](https://github.com/MinitwitGroupI/MiniTwit/blob/main/src/backend/requirements.txt) or inside src/backend/requirements.txt
