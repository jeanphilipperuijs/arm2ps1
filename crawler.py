import os
import sys
import time
from arm2powershell import ARM2Powershellfest

# MANDATORY: import path
'''
    Import directory to crawl can be given as command line argument or env variable
'''

rootDir = None
if("ARMTEMPLATEPATH2CRAWL" in os.environ):
    rootDir = os.environ["ARMTEMPLATEPATH2CRAWL"]
    print("using env value 'ARMTEMPLATEPATH2CRAWL'")
if(len(sys.argv) > 1):
    rootDir = sys.argv[1]
if(rootDir is None):
    print('''Need path to crawl as first argument or as envvar "ARMTEMPLATEPATH2CRAWL"''')
    sys.exit(1)

# OPTIONAL: default resource group name
resourceGrp = None
if("RESOURCEGROUP" in os.environ):
    resourceGrp = os.environ["RESOURCEGROUP"]
    print("using env value 'RESOURCEGROUP'")

## OPTIONAL: logfile
'''
    default None same as string value 'std'
'''
# logFile = 'std'
# to write in your home dir
logFile = os.environ['HOME']+"/arm2ps1.log"
# get value from ENV
if("ARM2PS1LOGFILE" in os.environ):
    logFile = os.environ["ARM2PS1LOGFILE"]
    print("using env value 'ARM2PS1LOGFILE'")
## OPTIONAL: logLevel
'''
    CRITICAL 50
    ERROR 40
    WARNING 30
    INFO 20
    DEBUG 10
    NOTSET 0
'''
logLevel = 20 # 50 debug
if("ARM2PS1LOGLEVEL" in os.environ):
    logLevel = os.environ["ARM2PS1LOGLEVEL"]
    print("using env value 'ARM2PS1LOGLEVEL'")

for dirPath, dirNames, fileNames in os.walk(rootDir):
    #print("Looking in ["+dirPath+"] for ARM templates")
    for fileName in fileNames:
        if "json" in fileName:
            v = os.path.join(dirPath, fileName)
            psf = ARM2Powershellfest(
                arm_template_file=v,
                resourceGroup=resourceGrp,
                logLevel=logLevel,
                logFileName=logFile)
            psf.init()
