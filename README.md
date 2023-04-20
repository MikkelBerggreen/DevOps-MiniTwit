###### Main branch
![Lint and Test - Main Branch](https://github.com/MinitwitGroupI/Minitwit/actions/workflows/lint-and-test.yml/badge.svg?branch=main)

![Deployed to Server - Main Branch](https://github.com/MinitwitGroupI/Minitwit/actions/workflows/deploy.yaml/badge.svg?branch=main)

# MiniTwit

MiniTwit is a messaging application which was converted from Flask to FastAPI framework.

You can find the deployed application [here](https://opsdev.gg) or https://opsdev.gg

![Landing Page](docs/images/landingpage.png?raw=true)

### All Url's: 
*  [Main page](https://opsdev.gg)
*  [Elastic] (http://opsdev.gg:5601) (Username: helgeandmircea, password: sesame0uvr3toi)
*  [Grafana] (http://opsdev.gg:3000/d/DVJQxp-4k/minitwit-responses?orgId=1)

## How to install and run the application

### Prerequisites: 
- Docker must be installed.
- Inside src/backend there is a file called ".env_sample". Input all necessary fields and rename the file to ".env".

### How to install and run the application:

Inside src/ there is a [docker-compose.yml file](src/docker-compose.yml).
Composing this file up will generate all necessary containers, volumes and files to run the application.

Once the containers have been deployed: navigate to http://localhost:8000 to access the main page.

## How to install required dependencies

All required dependencies will be installed once docker-compose file is executed.

However, in the rare case that there is no way to run docker containers. You can find the list of all dependencies [here](src/backend/requirements.txt) or inside src/backend/requirements.txt

## Contributing

Anyone is welcome to [contribute](docs/CONTRIBUTE.md),
however, if you decide to get involved, please take a moment to review
the [guidelines](docs/CONTRIBUTE.md).

## SLA

The team is commited to providing excelent service to their customers. Check out our commitments [here](docs/SLA.md).

## Security report

The team is proud to support our fellow students by evaluating [their applications security](docs/security%20report/Group%20I%20%20-%20Security%20Assessment%20Findings%20Report.pdf).
Additionally, the team would like to thank group X for their contributions to the security of the application < link should be here>

## License

The code is available under the [MIT license](docs/LICENSE).