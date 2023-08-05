godocker CLI - Client to use godocker in command line
========================================================

Installation with pip:

    pip install godocker_cli

Update with pip:

    pip install godocker_cli --upgrade

Installation from sources:

    git clone https://bitbucket.org/osallou/go-docker-cli.git
    cd go-docker-cli
    python setup.py install

Update from sources (in go-docker-cli directory):

    git pull
    python setup.py install

Command-lines:

    godlogin
    goduser
    godjob
    godfile
    godimage
    godproject
    godssh
    godbatch


Documentation:

You can access to the complete godocker CLI documentation [here](https://bitbucket.org/osallou/go-docker-cli/wiki/Home)

godocker_cli is compatible with python 3


1.0.23:
  Catch some error messages from godocker web
1.0.22:
  Add archive/delete operations (godweb >= 1.3.8)
1.0.21:
  Print size in human format in godfile list
1.0.20:
  In case of authentication error, return exit code > 0
1.0.19:
  Add gpu option (godocker >= 1.3.2)
  Fix setup to execute godX instead of godX.py
1.0.18:
  Add placement option in godjob to specify executor to use
  Fix tags
1.0.17:
  fix container status display
1.0.16:
  add container status for running jobs (container may be started but not ready)
1.0.15:
  add --project option on active/over job listing to filter by project (and see other project member tasks if enabled, godocker-web >= 1.2)
  add additional table to godimage list with GoDocker users images
  allow users to use these images without --external-image option
1.0.14:
  add --retry option to godjob to specify number fo retry in case of node failure (defaults to global config)
  add godjob archive option
1.0.13:
  Add --tag to killall to kill all user jobs with tag specified (needs go-docker-web >= 1.1.2)
1.0.12:
  Add --wait option to wait a job completion
1.0.11:
  Add --cmd option to specify command via command line instead of script file
1.0.10:
  Add new fields for temporary storage
  Add --env option to job create to substitute env variables in script file
1.0.9:
  Add exitcode on job status
  Manage project volumes


