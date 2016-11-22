#!/usr/bin/env python
# coding=utf-8
import commands
import os
import platform
import subprocess
import sys

#
# 用户配置区
#
#server = 'gerrit.zte.com.cn'
server = '10.93.50.62'
login = '10032866'
project = 'lte'
main_repo = 'main'

#Repo vs CodePath
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

#Area vs Repos
area_repo = {
    'all': repo_path.keys(),
    'wxxalte': ('Tool', 'Version', 'Code_CPUPlatform', 'Code_DSPPlatform', 'Code_FDDLTE20','Code_LWOSPlatform', 'Code_TDDLTE20', 'DailyBuild', 'PCLINT', 'Project', 'cmac', 'phy-bpn', 'phy-bpl', 'pub', 'sdr', 'sps', 'Code_RRU', 'Code_RTR'),
    'spsci': ('TestCase', 'Version', 'Code_CPUPlatform', 'Code_LWOSPlatform', 'DailyBuild', 'Project', 'pub', 'cmac', 'sdr', 'sps'),
    'sps': ('TestCase', 'Version', 'Code_CPUPlatform', 'Code_LWOSPlatform', 'DailyBuild', 'Project', 'pub', 'sdr', 'sps'),
    'sdrxa': ('TestCase', 'Version', 'Core', 'Code_CPUPlatform', 'Code_RRU', 'DailyBuild', 'Project', 'pub', 'sdr', 'sps'),
#   'cmac': ('TestCase', 'Code_CPUPlatform','Code_DSPPlatform', 'Code_LWOSPlatform', 'DailyBuild', 'Project', 'pub', 'cmac'),
    'cmac': ('Code_LWOSPlatform', 'DailyBuild', 'Project', 'pub', 'cmac'),
    'phy-bpn': ('TestCase', 'fpga', 'Code_DSPPlatform', 'Code_LWOSPlatform', 'DailyBuild', 'Project', 'pub', 'PHY'),
    'phy-bpl': ('TestCase', 'fpga', 'Code_DSPPlatform', 'Code_LWOSPlatform', 'DailyBuild', 'Project', 'pub', 'BaseBand_Dsp'),
	'8912': ('TestCase','Code_DSPPlatform', 'Code_LWOSPlatform', 'DailyBuild', 'Project', 'pub', 'BaseBand_Dsp','Code_CPUPlatform','Code_FDDLTE20','Code_RRU','Code_RTR','Code_TDDLTE20','Tool'),
	'8922-phy': ('Code_LWOSPlatform', 'Project','PHY','pub','BaseBand_Dsp_9132','PCLINT'),
	'8922-cmac':('TestCase','Code_CPUPlatform','Code_LWOSPlatform','DailyBuild','PCLINT','Project','BaseBand_Dsp_9132','cmac','pub'),
	'8901-cmac':('TestCase', 'Code_CPUPlatform','Code_LWOSPlatform', 'DailyBuild', 'Project', 'pub', 'cmac','PCLINT'),
	'pclint': ('TestCase', 'fpga', 'Code_DSPPlatform', 'Code_LWOSPlatform', 'DailyBuild', 'Project', 'pub', 'BaseBand_Dsp','PHY','cmac'),
}


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


def git_push(code_path):
    print 'Push : %s' % code_path
    os.chdir(code_path)
    system_call('git push origin %s' % branch)

def push_repo(repo_list, rootpath):
    for repo in repo_list:
        git_push(rootpath+repo_path[repo])


def usage():
    print """
Usage:

    [Prepare]
        1. Run ssh-keygen and press enter on promote
        2. Copy output from `cat ~/.ssh/id_rsa.pub` as SSH-Key
        3. Open URL http://gerrit.zte.com.cn/#/settings/ssh-keys
           and click button "Add Key ...", then paste SSH-Key
           into box, and click button 'Add';

    [Checkout]
        4. Run `%s id team dst` to clone
           all repos and combine repos into one project
            team    - One of %s
            dst     - dir
            branch  - develop branch
        
""" % (sys.argv[0], area_repo.keys())

if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
        quit()

    area_name = sys.argv[1]
    branch_dir = sys.argv[2]
    branch = sys.argv[3]

    if area_name not in area_repo:
        usage()
        quit()

    rootpath=os.getcwd()
    codepath=rootpath+"/"+branch_dir
    if not os.path.exists(codepath+"/code/Code_LTE"):
        os.makedirs(codepath+"/code/Code_LTE")
    
    area = area_repo[area_name]
    push_repo(area, codepath)

