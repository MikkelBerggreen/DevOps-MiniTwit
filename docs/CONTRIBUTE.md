# Which repository setup will we use?
We agreed to use a monorepo approach. 
- All our application and database code and configuration will be placed in the "src" directory. Application specifics are in the "backend" directory and database specifics are in the "db" one.
- All CI/CD pipelines and configuration will be placed in the ".github" directory. The pipelines are placed in the "workflows" directory and the ansible jobs are placed in the "ansible" directory
- All our IaC configuration will be placed in the "VagrantMiniTwit" directory
- All our external and internal documentation will be placed in the "docs" directory
- The final report will be placed in the "report" directory, with the built pdf being placed in "report/build"

# Which branching model will we use?
There will be a "main" branch which will contain a collection of all working features.
Whenever we will implement a new feature, we will create a feature branch and this branch will contain all code changes related to a single feature.
If we need to make a "hot-fix" to a feature in the main branch. We will create a branch labeled "hot-fix" and the changes related to fixing immediate critical bugs will be contained there.
However, there are exceptions where direct commits will be done to main (relating to CD/CI).

In short: Development branches will be created for each feature while commits to main brach will be done trough pull requests. 

# Which distributed development workflow will we use?
To keep track of bugs and new features we will use Github issues and Github project (which will act as a kanban board). 

# What do we expect contributions to look like?
- When an issue is located, a github issue is created and the specific details of the issue are highlighted. 
- A branch for this single issue is created.
- Then a single or multiple developers assign the issue to themselves. 
- These developers will commit code to the speciiced branch and once the feature is deemed "complete".
- Then they will create a pull request and assign relevant reviewers.
- The responsible reviewers will review the code and will approve the proposed changes.
- Lastly, once the changes have been aproved. The developers responsible for the issue will merge the changes to the main branch. 

# Who is responsible for integrating/reviewing contributions?
Everyone in the team is equaly responsible for reviewing changes. However, the reviewers should be chosen from the basis of who worked previously with a specific issue or is relevant to inform about any proposed changes.
For a pull request to the main branch, atleast 1 reviewer needs to be assigned and the changes need to be approved before merging.
To prevent any direct merging, github rules are used to ensure that no code can be pushed directly to the main branch.

However, Integration is done using CI pipelines.
