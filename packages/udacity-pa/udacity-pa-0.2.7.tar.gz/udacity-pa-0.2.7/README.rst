==============
Udacity Project Assistant
==============

udacity_pa is the command-line tool for submitting code to Udacity's automatic feedback agent.

Usage
---------

To submit your code, first navigate to the top-level directory of the repository you cloned from github.  From here, run
::
    udacity submit <PROJECT_NAME>

This will create a zipfile containing the required files and submit it to an automated feedback agent.  When you are  satisfied with the result, you may submit this zipfile for a human review.

In case you accidentally removed the zipfile, you may list all of your submissions with the command

::
    udacity ls <PROJECT_NAME>

To re-download the zipfile and the feedback, use

::
    udacity get <SUBMISSION_ID>
