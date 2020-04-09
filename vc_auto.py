import argparse, os, sys, path, platform, datetime
import subprocess
from subprocess import Popen, PIPE

ENCODING = 'utf-8'

def add_folders(repo_path_tracker):
    #prompt user for adding paths

    while True:
        inp = input('Please copy full path to folder. Leave empty to continue: ')
        if inp=='':
            break
        else:
            if (os.path.exists(inp)):
                repo_path_tracker.write(os.path.abspath(inp))
            else:
                print('Directory not valid. Please add a correct directory.')

def verify_folders():
    #checks each folder in a repo_path_tracker to verify it is local repo
    #and is setup to push and pull to remote repo
    repo_path_tracker = open('repo_path_tracker.txt', 'r')
    r_c = 0

    for curline in repo_path_tracker:
        if not curline.startswith('#'):
            git_exist = os.path.isdir(os.path.join(curline,'.git'))
            if (git_exist == False):
                r_c = 1
                break
    
    repo_path_tracker.close()
    return r_c


def run_subprocess(cmd, stdout=False):
    if (stdout == True):
        p = Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE,)
        stdout, stderr = p.communicate()
        return p.returncode, stdout
    else:
        p = Popen(cmd)
        stdout, stderr = p.communicate()
        return p.returncode

def push_subop(branch, curr_time, curline, master=False):
    
    if (master==True):
        branch = 'branch_{}'.format(curr_time)
        cmd = 'git checkout -b {}'.format(branch)
        r_c = run_subprocess(cmd)
        if (r_c != 0):
            print('Problem with dir {}, branch: {} in checkout'.format(curline, branch))
            return r_c
    
    cmd = 'git checkout {}'.format(branch) #change to local_branch_n
    r_c = run_subprocess(cmd)
    if (r_c != 0):
        print('Problem with dir {}, branch: {} in checkout'.format(curline, branch))
        return r_c
    cmd = 'git add .'
    r_c = run_subprocess(cmd)
    if (r_c != 0):
        print('Problem with dir {}, branch: {} in add'.format(curline, branch))
        return r_c
    cmd = 'git commit -m "Automatic commit done at: {}"'.format(curr_time)
    r_c, out = run_subprocess(cmd, stdout=True)
    if (r_c != 0):
        print('Problem with dir {}, branch: {} in commit'.format(curline, branch))
        decoded_out = str(out, ENCODING)
        com_error = 'nothing to commit, working tree clean'
        if (com_error in decoded_out):
            r_c = com_error
        return r_c

    # push remotely
    cmd = 'git push origin {}'.format(branch)
    r_c, out = run_subprocess(cmd, stdout=True)
    if (r_c != 0):
        print('Problem with dir {}, branch: {} in push'.format(curline, branch))
        decoded_out = str(out, ENCODING)
        com_error = 'Everything up-to-date'
        if (com_error in decoded_out):
            r_c = com_error
        return r_c
    
    if (master==True):
        cmd = 'git checkout master'
        r_c = run_subprocess(cmd)
        
        cmd = 'git branch -D {}'.format(branch)
        r_c = run_subprocess(cmd)
        if (r_c != 0):
            print('Problem with dir {}, branch: {} in deleting')
            return r_c

    return r_c

def pull_push(curline, log_vc_auto, curr_time):
    os.chdir(curline)

    # pull operation
    cmd = 'git checkout master'
    r_c = run_subprocess(cmd)
    cmd = 'git pull origin master'
    r_c, out = run_subprocess(cmd, stdout=True)
    log_msg = 'Pull operation for {} finished with return code : {}\n'.format(
            curline, r_c) 
    log_vc_auto.write(curr_time + '\t' + log_msg)
    
    # push operation
    cmd = 'git branch -a'
    r_c, out = run_subprocess(cmd, stdout=True)
    #print(out) #prints "b '{local_branch_1}\n{local_branch_2}\n{remote_branch_n}\n" in byte
    decoded_out = str(out[:-1], ENCODING)
    out_clean = decoded_out.replace(' ', '').replace('*', '')
    branch_list = out_clean.split('\n')
    branch_list = [branch.replace('\n', '') for branch in branch_list]
    branch_list = [branch for branch in branch_list if 'remote' not in branch]

    for branch in branch_list:
        print(branch)
        if len(branch_list) > 1:
            if branch != 'master':
                r_c = push_subop(branch, curr_time, curline)
                log_msg = 'Push operation for: {}, branch: {} finished with return code : {}\n'.format(
                    curline, branch, r_c) 
                log_vc_auto.write(curr_time + '\t' + log_msg)
        else:
            r_c = push_subop(branch, curr_time, curline, master=True)
            log_msg = 'Push operation for: {}, branch: {} finished with return code : {}\n'.format(
                curline, branch, r_c) 
            log_vc_auto.write(curr_time + '\t' + log_msg)
            
def task_scheduler_linux(path_exe, path_curr, time_run1, time_run2):
    # makes a task scheduler using cron which runs on fixed times
    # to do cron
    pass

def task_scheduler_win(path_exe, path_curr, time_run1, time_run2):
    # makes a task schedule script which runs on fixed times

    #syntax: /CREATE /SC [MINUTE/HOURLY/DAILY/WEEKLY/MONTHLY/
    # ONCE/ONSTART/ONLOGON/ONIDLE/ONEVENT] /D [MON to SUN or 1-31 or *]
    # /TN [TASK NAME AND LOCATION] /TR [LOCATION AND NAME OF TASK TO RUN]
    # /ST [TIME TO TRUN TASK (24 HOURS FORMAT)]

    bat_name = 'task_scheduler.bat'
    task_scheduler = open(bat_name, 'w')
    task_scheduler.write('''SCHTASKS /CREATE /SC DAILY /TN "vc_auto_1" /TR "{} {}" /ST {}:00\n'''.format(path_exe, path_curr, time_run1))
    task_scheduler.write('''SCHTASKS /CREATE /SC DAILY /TN "vc_auto_2" /TR "{} {}" /ST {}:00'''.format(path_exe, path_curr, time_run2))
    task_scheduler.close()

    r_c = run_subprocess(bat_name)
    
    return r_c

def initialize(curr_time, curr_os):
    log_vc_auto = open('log_vc_auto.txt', 'w')
    log_vc_auto.write('curr_time\tlog_msg\n')

    repo_path_tracker = open('repo_path_tracker.txt', 'w')
    repo_path_tracker.write('#local_repo_path\n')

    time_run1 = input('Fixed time 1 to run script(number from 01-23): ')
    time_run2 = input('Fixed time 2 to run script(number from 01-23): ')

    try:
        exe = sys.executable #python executabe path
        path_exe = path.Path(exe)  #path for the exe
        path_curr = path.Path(os.getcwd())
    except:
        log_msg = 'Error in either executable or current path. Closing prematurely.'
        log_vc_auto.write(curr_time + '\t' + log_msg)
        log_vc_auto.close()
        repo_path_tracker.close()

    print('OS:', curr_os)
    if (curr_os == 'Windows'):
        rc = task_scheduler_win(path_exe, path_curr, time_run1, time_run2)
        log_msg = 'Return code for initializing task_scheduler_win: {}\n'.format(rc)
        log_vc_auto.write(curr_time + '\t' + log_msg)
    elif (curr_os == 'Linux'):
        task_scheduler_linux(path_exe, path_curr, time_run1, time_run2)
        log_msg = 'No task scheduler for this platform. Manual operation only.\n'
        log_vc_auto.write(curr_time + '\t' + log_msg)
    else:
        log_msg = 'No task scheduler for this platform. Manual operation only.\n'
        log_vc_auto.write(curr_time + '\t' + log_msg)

    add_folders(repo_path_tracker)
    repo_path_tracker.close()
        
    return log_vc_auto

def check_setup(ft):
    print('First time setup: ', ft)
    curr_time = str(datetime.datetime.now()).replace(' ','_').replace(':','-')
    curr_time = curr_time.split('.', 1)[0]
    curr_os = platform.system()
    
    #initializes log, path tracker and scheduler if first time, else runs updating
    if ft:
        log_vc_auto = initialize(curr_time, curr_os) 
    else:
        log_vc_auto = open('log_vc_auto.txt', 'a')
    
    r_c = verify_folders()
    log_msg = 'Folder verification return code: {}\n'.format(r_c)
    log_vc_auto.write(curr_time + '\t' + log_msg)
    
    # to do: go through each folder in repo_path_tracker.txt, pull then push
    repo_path_tracker = open('repo_path_tracker.txt', 'r')
    
    for curline in repo_path_tracker:
        if not curline.startswith('#'):
            pull_push(curline, log_vc_auto, curr_time)

    repo_path_tracker.close()
    log_vc_auto.close()
    
def main():
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