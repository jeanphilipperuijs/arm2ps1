import os
import sys
from generate_powershell import Powershellfest

rootDir = None
if("ARMTEMPLATEPATH2CRAWL" in os.environ):
    rootDir = os.environ["ARMTEMPLATEPATH2CRAWL"]
    print("using env value 'ARMTEMPLATEPATH2CRAWL'")
if(len(sys.argv) > 1):
    rootDir = sys.argv[1]
if(rootDir is None):
    print('''Need path to crawl as first argument or as envvar "ARMTEMPLATEPATH2CRAWL" 
    ''')
    sys.exit(1)

print("Crawling '"+rootDir+"' for ARM templates")

for dirPath, dirNames, fileNames in os.walk(rootDir):
    for fileName in fileNames:
        if(".json" in fileName and "parameters" not in fileName):
            v = os.path.join(dirPath, fileName)
            psf = Powershellfest(v)
            psf.generate_powershell()
