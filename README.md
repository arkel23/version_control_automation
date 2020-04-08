## Version Control Automator Script
To run: `python vc_auto.py [-ft True/False]`

-ft (first time) opt. parameter tells script if  it needs to do initial setup. Def: False.

If first time running please run with flag: `-ft True` 
which will make it run initial setup routine which consists of:
1) Creating scheduler file depending on OS.
2) Prompting user to create path tracker file and then check on integrity of repos.
3) Running startup and shutdown routines.

If False then runs update routine consists of: 
1) Checking integrity of repositories path tracker file.
2) Running either startup or shutdown routines, depending on scheduler.

Made by Edwin Arkel Rios for NCTU PCS Lab.
