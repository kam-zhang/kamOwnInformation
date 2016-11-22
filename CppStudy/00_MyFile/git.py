#!/usr/bin/env python
# coding=utf-8
# If you have any question, send email to dong.minghui@zte.com.cn
#####################################################################
# This script packages 5 git commands : config,clone,checkout,pull,push 
#####################################################################
import commands
import os
import platform
import subprocess
import sys
import re

###################################################################
# User configuration
###################################################################
servernj = 'gerrit.zte.com.cn'
serverxa = 'gerritro.zte.com.cn'
project='lte'

###################################################################
git_action = {
    'config':'config',
    'clone':'clone',
    'checkout':'checkout',
    'pull':'pull',
    'push':'push',
}
###################################################################
# The LTE project all code repos and code path
# Repo : CodePath
repo_path = {
    'Core':'/Core',
    'TestCase':'/TestCase',
    'Tool':'/Tool',
    'Version':'/Version',
    'fpga':'/fpga',
    'other':'/other',
    'Code_CPUPlatform':'/code/Code_CPUPlatform',
    'Code_DSPPlatform':'/code/Code_DSPPlatform',
    'Code_FDDLTE20':'/code/Code_FDDLTE20',
    'Code_LWOSPlatform':'/code/Code_LWOSPlatform',
    'Code_TDDLTE20':'/code/Code_TDDLTE20',
    'DailyBuild':'/code/DailyBuild',
    'PCLINT':'/code/PCLINT',
    'Project':'/code/Project',
    'Code_RRU':'/code/Code_RRU',
    'Code_RTR':'/code/Code_RTR',
    'BaseBand_Dsp':'/code/Code_LTE/BaseBand_Dsp',
    'BaseBand_Dsp_9132':'/code/Code_LTE/BaseBand_Dsp_9132',
    'cmac':'/code/Code_LTE/cmac',
    'PHY':'/code/Code_LTE/PHY',
    'pub':'/code/Code_LTE/pub',
    'sdr':'/code/Code_LTE/sdr',
    'sps':'/code/Code_LTE/sps',   
}

###################################################################
# The following content developers can adjust the code repos, add/modify 
# But, don't delete
# When only one code repo is cloned, example: 'tddrru':('Version',), 
area_repo = {
    'all'   :repo_path.keys(),
    'sps'   :('pub','sdr','sps','Code_CPUPlatform','DailyBuild','Project'), 
    'rnlu'  :('pub','sdr','sps','Code_CPUPlatform','Code_LWOSPlatform','DailyBuild','Project','cmac'),
    'tool'  :('pub','sdr','sps','Code_CPUPlatform','Code_LWOSPlatform','DailyBuild','Project','cmac','Tool','Version','Code_DSPPlatform'), 
    'sdrxa' :('pub','Version','Code_CPUPlatform','DailyBuild','Project','sdr','sps'),
    'sdrsz' :('pub','Version','Code_CPUPlatform','DailyBuild','Project'),
    'pclint'   :('pub','Code_DSPPlatform','Code_LWOSPlatform','DailyBuild','Project','TestCase','cmac','PHY','BaseBand_Dsp'),    
    'cmac'     :('pub','Code_DSPPlatform','Code_LWOSPlatform','DailyBuild','Project','TestCase','cmac','Code_CPUPlatform'),
    'phy-bpn'  :('pub','Code_DSPPlatform','Code_LWOSPlatform','DailyBuild','Project','TestCase','PHY'),
    'phy-bpl'  :('pub','Code_DSPPlatform','Code_LWOSPlatform','DailyBuild','Project','TestCase','BaseBand_Dsp'),
    '8912'     :('pub','Code_DSPPlatform','Code_LWOSPlatform','DailyBuild','Project','TestCase','BaseBand_Dsp','Code_CPUPlatform','Code_FDDLTE20','Code_TDDLTE20','Code_RRU','Code_RTR','Tool'),
    '8922-phy' :('pub','Code_LWOSPlatform','DailyBuild','Project','PCLINT','PHY','BaseBand_Dsp_9132'),
    '8922-cmac':('pub','Code_LWOSPlatform','DailyBuild','Project','PCLINT','cmac','Code_CPUPlatform','TestCase','BaseBand_Dsp_9132'),
    '8901-cmac':('pub','Code_LWOSPlatform','DailyBuild','Project','PCLINT','cmac','Code_CPUPlatform','TestCase'),
    'dspplat'  :('pub','Code_LWOSPlatform','DailyBuild','Project','Code_DSPPlatform','Tool'),   
    'fddrru'   :('Code_RTR','Code_RRU','Code_CPUPlatform','DailyBuild','Project','Version'), 
    'tddrru'   :('Version',), 
    'bpl0'     :('Code_TDDLTE20','Code_FDDLTE20'), 
    'fpga'     :('fpga','Version'),
}
###################################################################

###################################################################
def usage_git():
    print """
Usage:
    These are common Git commands packaged by python:

    %s config <user.name> <user.email>
    %s clone <workdir> <team> <branchname> 
    %s checkout <workdir> <branchname>
    %s pull <workdir>
    %s push <workdir>

     workdir    - Working directory name
     team       - One of [all,sps,rnlu,tool,sdrxa,sdrsz,pclint,
                  camc,phy-bpn,phy-bpl,8912,8922-phy,8922-cmac,
                  8901-cmac,dspplat,fddrru,tddrru,bpl0,fpga]
     branchname - One of [spsdev,bbdev,sdrdev,feature/xxdev,...]
        
""" % (sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0],sys.argv[0])
#------------------------------------------------------------------
def usage_config():
    print """
Usage:

    [Config]
        Run `%s config <user.name> <user.email>` to set 
        user's name & email & global options
    [Example]
        %s config 董明慧10051333 dong.minghui@zte.com.cn
        
""" % (sys.argv[0], sys.argv[0])
#------------------------------------------------------------------
def usage_clone():
    print """
Usage:

    [Prepare]
      1. Run `%s config <user.name> <user.email>` to set
         user's name & email & global options.
      2. Run `ssh-keygen -t rsa -C "user.email"` and press enter on promote.
      3. Copy output from `cat ~/.ssh/id_rsa.pub` as SSH-Key.
      4. Open URL http://gerrit.zte.com.cn/#/settings/ssh-keys
         and click button "Add Key ...", then paste SSH-Key
         into box, and click button 'Add'.

    [Clone & Combine]
      5. Run `%s clone <workdir> <team> <branchname>` to clone
         all repos and combine repos into one project.

         workdir    - Working directory name
         team       - One of [all,sps,rnlu,tool,sdrxa,sdrsz,pclint,
                      camc,phy-bpn,phy-bpl,8912,8922-phy,8922-cmac,
                      8901-cmac,dspplat,fddrru,tddrru,bpl0,fpga]
         branchname - One of [spsdev,bbdev,sdrdev,feature/xxdev,...]

    [Example]
         %s clone V3.4_dev sps spsdev
        
""" % (sys.argv[0], sys.argv[0], sys.argv[0])
#------------------------------------------------------------------
def usage_checkout():
    print """
Usage:

    [Checkout]
      Run `%s checkout <workdir> <branchname>` switch to new branch
         workdir    - Working directory name
         branchname - One of [spsdev,bbdev,sdrdev,feature/xxdev,...]

    [Example]
         %s checkout V3.4_dev spsdev
        
""" % (sys.argv[0], sys.argv[0])
#------------------------------------------------------------------
def usage_pull():
    print """
Usage:

    [Pull]
      Run `%s pull <workdir>` to fetch from repository
         workdir - Working directory name

    [Example]
         %s pull V3.4_dev
        
""" % (sys.argv[0],sys.argv[0])
#------------------------------------------------------------------
def usage_push():
    print """
Usage:

    [Push]
      Run `%s push <workdir>` to updates remote refs using local refs
         workdir - Working directory name

    [Example]
         %s push V3.4_dev
                 
""" % (sys.argv[0],sys.argv[0])

###################################################################
# git config
###################################################################
def git_config():
    system_call('git config --global user.name %s' % name)
    system_call('git config --global user.email %s' % email)
    system_call('git config --global --remove-section user')
    system_call('git config --global user.name %s' % name)
    system_call('git config --global user.email %s' % email)

    system_call('git config --global pull.rebase true')
    system_call('git config --global core.longpaths true')  
    system_call('git config --global core.autocrlf input')

    system_call('git config --global alias.st status')
    system_call('git config --global alias.ci commit')
    system_call('git config --global alias.co checkout')
    system_call('git config --global alias.br branch')

    system_call('git config --global colore.ui true')

    system_call('git config --list')    

###################################################################
# git clone
###################################################################
def getid(number):
    system_name = platform.system()
    if 'Windows' == system_name:
        filepath = 'C:'+os.popen( "echo %homepath% ", "r ").read().strip('\n').strip()
        try:
            fo=open(filepath+'\.gitconfig','r')
            foiter=iter(fo)
            for l in foiter:
                m=re.match(r"\sname\s=\s",l)
                if m:
                    id=l.strip().split('name = ')[1]
                    uid=id.decode("utf-8")
                    print 'Cloned by %s' % id
                    if uid.isnumeric() or uid.isalpha():
                        print 'The format of the name(%s) is not valid.' % id
                        print 'Example: 董明慧10051333'
                        print 'Run `%s config <user.name> <user.email>` to reset' % sys.argv[0]
                        fo.close()
                        quit()
                    else:
                        number.append(id[-8:])
            fo.close()
        except IOError,e:
            print 'Error: Open file fail, please check .gitconfig'
            quit()

    if 'Linux' == system_name:
        filepath = os.popen('echo $HOME').readlines()[0].strip('\n').strip()
        try:
            fo=open(filepath+'/.gitconfig','r')
            foiter=iter(fo)
            for l in foiter:
                m=re.match(r"\sname\s=\s",l)
                if m:
                    id=l.strip().split('name = ')[1]
                    uid=id.decode("utf-8")
                    print 'Cloned by %s' % id
                    if uid.isnumeric() or uid.isalpha():
                        print 'The format of the name(%s) is not valid.' % id
                        print 'Example: 董明慧10051333'
                        print 'Run `%s config <user.name> <user.email>` to reset' % sys.argv[0]
                        fo.close()
                        quit()
                    else:
                        number.append(id[-8:])
            fo.close()
        except IOError,e:
            print 'Error: Open file fail, please check .gitconfig'
            quit()

def build_fetch_repo_url(repo_name):
    return 'ssh://%s@%s:29418/%s/%s' % (login, serverxa, project, repo_name)

def build_push_repo_url(repo_name):
    return 'ssh://%s@%s:29418/%s/%s' % (login, servernj, project, repo_name)

def git_clone(fetch_url, push_url, code_path):
    print 'Clone %s ...' % fetch_url
    os.chdir(rootpath)
    system_call('git clone %s %s' % (fetch_url, code_path))
    print 'Path: %s' % code_path
    os.chdir(code_path)
    system_call('git checkout %s' % branch)
    system_call('git branch --set-upstream-to=origin/%s %s' % (branch, branch))
    system_call('git remote set-url --push origin %s' % push_url)
    system_call('git config --global pull.rebase true')

def clone_repos(repo_list, rootpath):
    for repo in repo_list:
        git_clone(build_fetch_repo_url(repo), build_push_repo_url(repo), rootpath+repo_path[repo])

###################################################################
# git checkout
###################################################################
def git_checkout(code_path, branch):
    if not os.path.exists(code_path):
        pass
    else:        
        os.chdir(code_path)
        if not os.path.exists('.git'):
            print 'Path : %s' % code_path
            print 'Fatal: Not a git repository (or any of the parent directories): .git'
        else:
            os.chdir(code_path)
            print 'Path : %s' % code_path
            print 'git checkout %s' % branch    
#           system_call('git checkout .')
#           system_call('git clean -d -f')
            system_call('git checkout %s' % branch)
            system_call('git pull')

def checkout_branch(repo_list, rootpath, co_branch):
    for repo in repo_list:
        git_checkout(rootpath+repo_path[repo], co_branch)
        
###################################################################
# git pull
###################################################################
def git_pull(code_path):
    if not os.path.exists(code_path):
        pass
    else:        
        os.chdir(code_path)
        if not os.path.exists('.git'):
            print 'Pull : %s' % code_path
            print 'Fatal: Not a git repository (or any of the parent directories): .git'
        else:
            print 'Pull : %s' % code_path
#           system_call('git checkout .')
#           system_call('git clean -d -f')
            system_call('git log --oneline --decorate -1')
            system_call('git pull')
            system_call('git log --oneline --decorate -1')

def pull_repo(repo_list, rootpath):
    for repo in repo_list:
        git_pull(rootpath+repo_path[repo])

###################################################################
# git push
###################################################################
def git_push(code_path):
    if not os.path.exists(code_path):
        pass
    else:
        os.chdir(code_path)
        if not os.path.exists('.git'):
            print 'Push : %s' % code_path
            print 'Fatal: Not a git repository (or any of the parent directories): .git'
        else:
            print 'Push : %s' % code_path         
            system_call('git push')

def push_repo(repo_list, rootpath):
    for repo in repo_list:
        git_push(rootpath+repo_path[repo])
        
###################################################################
###################################################################
def system_call(cmd):
    system_name = platform.system()
    if 'Linux' == system_name:
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
            raise Exception(output)
    elif 'Windows' == system_name:
        subprocess.check_call(cmd)
    else:
        raise Exception('Unknown system type(%s)' % system_name)

def set_codepath(area_name,local_dir,content):
    if area_name not in area_repo:
        usage_clone()
        print 'Error: input team name[ %s ] is not one of %s.' % (area_name, area_repo.keys())
        quit()

    rootpath=os.getcwd()
    if rootpath[-1:] == '/' or rootpath[-1:]=='\\':
        codepath=rootpath+local_dir
    else:
        codepath=rootpath+'/'+local_dir

    if os.path.exists(codepath):
        print ''
        print 'Warning: input dir[ %s ] already exists.' % local_dir
        quit()

    if not os.path.exists(codepath+"/code/Code_LTE"):
        os.makedirs(codepath+"/code/Code_LTE")
    
    area = area_repo[area_name]
    content.append(area)
    content.append(rootpath)
    content.append(codepath)
     
def get_codepath(area_name,local_dir,content):
    if area_name not in area_repo:
        usage_clone()
        print 'Error: input team name[ %s ] is not one of %s.' % (area_name, area_repo.keys())
        quit()

    rootpath=os.getcwd()
    if rootpath[-1:] == '/' or rootpath[-1:]=='\\':
        codepath=rootpath+local_dir
    else:
        codepath=rootpath+'/'+local_dir
   
    area = area_repo[area_name]
    content.append(area)
    content.append(rootpath)
    content.append(codepath)     
    
###################################################################
###################################################################
if __name__ == '__main__':    
    number=[]
    content=[]
    rootpath=os.getcwd()
    if len(sys.argv) == 1:
          usage_git()
          quit()          

    action = sys.argv[1]  
    
    if 'config' == action: 
        if len(sys.argv) != 4:
            usage_config()
            quit()
        name = sys.argv[2]
        email = sys.argv[3]
        git_config()

    elif 'clone' == action:
        if len(sys.argv) != 5:
            usage_clone()
            quit()
        local_dir = sys.argv[2]
        area_name = sys.argv[3]
        branch    = sys.argv[4]

        getid(number)
        login=number[0]
        print 'Current user HROnline ID : %s' % login
        set_codepath(area_name,local_dir,content)
        clone_repos(content[0], content[2])           

    elif 'checkout' == action:
        if len(sys.argv) != 4:
            usage_checkout()
            quit()
        local_dir = sys.argv[2]
        branch    = sys.argv[3]
        area_name = 'all'
        get_codepath(area_name,local_dir,content)
        checkout_branch(content[0], content[2], branch)

    elif 'pull' == action:
        if len(sys.argv) != 3:
            usage_pull()
            quit()   
        local_dir = sys.argv[2]
        area_name = 'all'
        get_codepath(area_name,local_dir,content)
        pull_repo(content[0], content[2])

    elif 'push' == action:
        if len(sys.argv) != 3:
            usage_push()
            quit()   
        local_dir = sys.argv[2]
        area_name = 'all'
        get_codepath(area_name,local_dir,content)
        push_repo(content[0], content[2])
	
    else:
        usage_git()
