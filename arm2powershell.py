import io
import os
import json
import logging
from string import Template
from pshelp import PowershellHelpHeader


class ARM2Powershellfest:
    def __init__(self, arm_template_file, resourceGroup=None, overwrite=None,
                 newRgDepCmd="New-AzResourceGroupDeployment",
                 links=[
                     'https://docs.microsoft.com/en-us/powershell/module/az.resources/new-azresourcegroupdeployment'],
                 loglevel=logging.DEBUG, logfilename=None):
        self.arm_file = arm_template_file
        self.resGrp = resourceGroup
        self.overwrite = overwrite
        self.newRgDep = newRgDepCmd
        self.loglevel = loglevel
        self.logfilename = logfilename

    def init(self):
        f = io.open(self.arm_file, mode="r", encoding="utf-8").read()

        filename, file_extension = os.path.splitext(self.arm_file)
        if self.logfilename is None:
            self.logfilename = filename+'.log'
        #print("\t"+self.logfilename)
        logging.basicConfig(filename=self.logfilename,
                            filemode='w', level=self.loglevel,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        if ".json" in file_extension:
            j = json.loads(f)
            schema = None
            try:
                schema = j["$schema"]
            except Exception as e:
                logging.warning("[" + os.path.basename(self.arm_file) +
                              "] is not an ARM template schema")
            try:
                if schema is not None and "deploymentTemplate" in schema:
                    self.ps1file = filename + ".ps1"
                    fsize = -1

                    try:
                        fsize = os.path.getsize(self.ps1file)
                    except:
                        logging.info(self.ps1file+" does not exist")

                    if self.overwrite is not 'a':
                        if os.path.isfile(self.ps1file) and fsize > 1:
                            self.overwrite = input(
                                "overwrite '" + self.ps1file + "' ? : ")

                    if self.overwrite == 'y' or self.overwrite == 'a' or fsize < 1:
                        self.items = j["parameters"].items()
                        self.output = io.open(
                            self.ps1file, mode="w", encoding="utf-8")

                        header = PowershellHelpHeader(
                            output=self.output, parameters=self.items, origin_file=self.arm_file)
                        header.write_header()

                        self.generate_params()
                        self.generate_AzResourceGroupDeployment()
                        self.output.close()
                else:
                    logging.warning("[" + os.path.basename(self.arm_file) +
                                   "] is not a Deployment Template")
            except Exception as e:
                logging.warning(e)

    def generate_params(self):
        t_default = Template('''\t[${type}]$$${key} = ${defaultValue}''')
        t_nodefault = Template('''\t[${type}]$$${key}''')

        self.output.write("param (")
        self.output.write("\n")
        self.output.write(
            "\t[String]$SubscriptionID = (Get-AzContext).Subscription.id,\n")
        self.output.write("\t[String]$ResourceGroupName,\n")
        noi = len(self.items)
        for key, value in self.items:
            if "defaultValue" in value:
                defVal = value["defaultValue"]
                defList = None
                listOfInt = False
                if type(defVal) is list:
                    try:
                        listOfInt = all(type(int(x)) is int for x in defVal)
                    except Exception as e:
                        logging.debug(e)
                        # not all int, fallback to string
                        pass
                    if(listOfInt):
                        defList = "@("+", ".join(defVal)+")"
                    else:
                        defList = "@('"+"', '".join(defVal)+"')"

                if type(defVal) is list:
                    if listOfInt:
                        param = (t_default.substitute(
                            type="int[]", key=key, defaultValue=defList))
                    else:
                        param = (t_default.substitute(
                            type="string[]", key=key, defaultValue=defList))
                if type(defVal) is str:
                    param = (t_default.substitute(
                        type=value["type"], key=key, defaultValue='"'+defVal+'"'))
                # logging.debug(param)

            else:
                param = (t_nodefault.substitute(type=value["type"], key=key))
            self.output.write(param)
            noi = noi - 1
            if(noi > 0):
                self.output.write(",")
            self.output.write("\n")
        self.output.write(")")

    def generate_AzResourceGroupDeployment(self):
        self.output.write("\n")
        self.output.write(self.newRgDep)
        self.output.write(" -TemplateFile ./" +
                          os.path.basename(self.arm_file) + " `\n")
        if(self.resGrp is None):
            self.output.write("\t-ResourceGroupName $ResourceGroupName `\n")
        else:
            self.output.write("\t-ResourceGroupName " +
                              str(self.resGrp) + " `\n")

        for key, value in self.items:
            self.output.write("\t-" + key + " $" + key + " `\n")

        logging.debug('Generated [' + os.path.basename(self.ps1file) +
                      '] with ' + str(len(self.items)) + ' parameters')
