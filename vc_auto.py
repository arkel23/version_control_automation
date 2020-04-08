import argparse, os, sys, path, platform
import subprocess
from subprocess import Popen, PIPE
from datetime import date

def day_start():
    pass
    # first go into each tracked repo then pull from rem master into local master
    # log into vc_auto_log.txt

def day_end():
    pass
    #at certain time stage first check which branch it's being worked on
    #if not master then stage, commit and push remotely. Log into vc_auto_log.txt
    #if master then create temp_branch, stage, commit and push remotely. Log

def check_setup(ft):
    #check if first time setup or update
    print('First time setup: ', ft)
    # check platform and adjust steps based on system:
    # setup cron or windows scheduler/mac to run the script at certain times
    # only needed for the first time. script should save this info so it is automated next
    # save or create a new .bash or something file
    curr_os = platform.system()
    if (curr_os == 'Linux'):
        print('OS:', curr_os)
    elif (curr_os == 'Darwin'):
        print('OS:', curr_os)
    elif (curr_os == 'Windows'):
        print('OS:', curr_os)
    else:
        print('OS:', curr_os)
        #log irregular OS into vc_auto_log.txt
        sys.exit(1)


    #check credentials (git config user.name and user.email)
    #check each folder to contain .git folder
    # if everything normal then return 0, otherwise 1 and shutdown

def main():
    """
    to do: 
    read input parameters (initialize new path tracker file, update)
    check integrity of path repos and os
    startup routine (day_start)
    end routine (day_end)
    
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-ft', required=False, 
    dest='ft', type=str, default=False,
    help='''Tells script if needs to do initial setup (first time). Default is False.\n
    If first time please run with flag: -init True which will make it run initial setup.
    If False then runs update routine.''')
    
    args = parser.parse_args()

    if (args.ft == 'True'):
        init_setup = True
        check_setup(ft=init_setup)
    else:
        init_setup = False
        check_setup(ft=init_setup)

main()