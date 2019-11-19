import io
import os
import json
from string import Template

# template
tmplt = '''\t[${type}]$$${key} = "${defaultValue}"'''
t_default = Template(tmplt)
tmplt = '''\t[${type}]$$${key}'''
t_nodefault = Template(tmplt)


class Powershellfest:
    def __init__(self, arm_template_file, resourceGroup=None, overwrite=None):
        self.arm_file = arm_template_file
        self.resGrp = resourceGroup
        self.overwrite = overwrite
        print(self.arm_file, self.resGrp, self.overwrite)

    def generate_powershell(self):
        f = io.open(self.arm_file, mode="r", encoding="utf-8").read()

        filename, file_extension = os.path.splitext(self.arm_file)
        if ".json" in file_extension:
            self.ps1file = filename+".ps1"
            fsize = -1

            try:
                fsize = os.path.getsize(self.ps1file)
            except:
                pass

            if self.overwrite is not 'a':
                if os.path.isfile(self.ps1file) and fsize > 1:
                    self.overwrite = input(
                        "overwrite '"+self.ps1file + "' ? : ")

            if self.overwrite == 'y' or self.overwrite == 'a' or fsize < 1:
                j = json.loads(f)
                self.items = j["parameters"].items()
                self.generate_params()
                self.appendAzResourceGroupDeployment()

    def generate_params(self):
        output = io.open(self.ps1file, mode="w", encoding="utf-8")
        output.write("param (")
        output.write("\n")
        output.write(
            "\t[String]$SubscriptionID = (Get-AzContext).Subscription.id,\n")
        output.write("\t[String]$ResourceGroupName,\n")
        noi = len(self.items)
        for key, value in self.items:
            if "defaultValue" in value:
                param = (t_default.substitute(
                    type=value["type"], key=key, defaultValue=value["defaultValue"]))
            else:
                param = (t_nodefault.substitute(type=value["type"], key=key))
            output.write(param)
            noi = noi - 1
            if(noi > 0):
                output.write(",")
            output.write("\n")
            # for pkey, pvalue in value.items():
            #    print("\t", pkey, ":", pvalue)
        output.write(")")
        output.close()

    def appendAzResourceGroupDeployment(self):
        output = io.open(self.ps1file, mode="a", encoding="utf-8")
        output.write("\n")
        output.write("New-AzResourceGroupDeployment")
        output.write(" -TemplateFile ./" +
                     os.path.basename(self.arm_file)+" `\n")
        if(self.resGrp is None):
            output.write("\t-ResourceGroupName $ResourceGroupName `\n")
        else:
            output.write("\t-ResourceGroupName "+str(self.resGrp)+" `\n")

        for key, value in self.items:
            output.write("\t-"+key+" $"+key+" `\n")

        output.close()
        print('Done with '+self.ps1file)
