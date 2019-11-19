import io
import os
import json
from string import Template

# template
tmplt = '''\t[${type}]$$${key} = "${defaultValue}"'''
t_default = Template(tmplt)
tmplt = '''\t[${type}]$$${key}'''
t_nodefault = Template(tmplt)

# load arm template


class Powershellfest:
    def __init__(self, arm_template_file, resourceGroup='jru-test'):
        self.arm_template_file = arm_template_file
        self.resGrp = resourceGroup
        print(arm_template_file)

    def generate_powershell(self):
        f = io.open(self.arm_template_file, mode="r", encoding="utf-8").read()

        filename, file_extension = os.path.splitext(self.arm_template_file)
        self.ps1file = filename+".ps1"
        fsize = -1

        # try:
        #    fsize = os.path.getsize(ps1file)
        # except:
        #    pass

        # if os.path.isfile(ps1file and fsize > 1):
        #    print("Skipping: '"+ps1file+"' exists")

        if ".json" in file_extension and fsize < 1:
            j = json.loads(f)
            self.items = j["parameters"].items()
            self.generate_params()
            self.appendCommand()

    def generate_params(self):
        output = io.open(self.ps1file, mode="w", encoding="utf-8")
        output.write("param (")
        output.write("\n")
        output.write(
            "\t[String]$SubscriptionID = (Get-AzContext).Subscription.id,\n")
        output.write("\t[String]$ResourceGroupName = '" +
                     self.resGrp+"',\n")
        noi = len(self.items)
        for key, value in self.items:
            if "defaultValue" in value:
                param = (t_default.substitute(
                    type=value["type"], key=key, defaultValue=value["defaultValue"]))
            else:
                param = (t_nodefault.substitute(type=value["type"], key=key))
            # print(param)
            output.write(param)
            noi = noi - 1
            if(noi > 0):
                output.write(",")
            output.write("\n")
            # for pkey, pvalue in value.items():
            #    print("\t", pkey, ":", pvalue)

        output.write(")")
        output.close()

    def appendCommand(self):
        output = io.open(self.ps1file, mode="a", encoding="utf-8")
        output.write("\n")
        output.write("New-AzResourceGroupDeployment -TemplateFile ./" +
                     os.path.basename(self.arm_template_file)+" `\n")
        output.write("\t-ResourceGroupName $ResourceGroupName `\n")
        for key, value in self.items:
            output.write("\t-"+key+" $"+key+" `\n")
        output.close()
        print('Done with '+self.ps1file)
