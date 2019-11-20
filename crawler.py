import os
import sys
import time
from arm2powershell import ARM2Powershellfest

# mandatory import path
rootDir = None
if("ARMTEMPLATEPATH2CRAWL" in os.environ):
    rootDir = os.environ["ARMTEMPLATEPATH2CRAWL"]
    print("using env value 'ARMTEMPLATEPATH2CRAWL'")
if(len(sys.argv) > 1):
    rootDir = sys.argv[1]
if(rootDir is None):
    print('''Need path to crawl as first argument or as envvar "ARMTEMPLATEPATH2CRAWL"''')
    sys.exit(1)


# optional resource group
resourceGrp = None
if("RESOURCEGROUP" in os.environ):
    resourceGrp = os.environ["RESOURCEGROUP"]
    print("using env value 'RESOURCEGROUP'")


print("Crawling '"+rootDir+"' for ARM templates")

for dirPath, dirNames, fileNames in os.walk(rootDir):
    for fileName in fileNames:
        if(".json" in fileName):
            print("Analyzing ["+dirPath+fileName+"]")
            v = os.path.join(dirPath, fileName)
            psf = ARM2Powershellfest(
                v, resourceGrp, overwrite='a', logfilename=os.environ['HOME']+"/arm2ps1.log")
            psf.init()
