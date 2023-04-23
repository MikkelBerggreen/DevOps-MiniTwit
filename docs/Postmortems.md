In order to test out the teams logging system. The team created two subteams:

Team A - introduced two simple bugs in the system. Login would not work with correct credentials and a technical error inside the create message function as the message string will be converted to int. 

Team B - will look at logs and attempt to isolate the components where the bugs are.

For the incorrect credential bug the Team B managed to isolate the specific endpoint which is causing the error. But could not give any detailed explanation what is causing the error as the logging only registered the error message and not the actual cause of the error.
For the technical error, Team B could see the proper stack trace inside the logging stack and could isolate the problem component and even pinpoint the exact line where the error has occured. 

As a result the loggin infrastructure is sufficient for this project. However, it could be improved with more detailed overview on why certain errors occur. 