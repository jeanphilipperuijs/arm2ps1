import os
from string import Template

class PowershellHelpHeader:
    def __init__(self, output, parameters, origin_file, links=None, description='Modify at own risk #autogenerated'):
        self.output = output
        self.parameters = parameters
        self.origin_file = origin_file
        self.links = links
        self.description = description

    def get_item(self,  k, v):
        return "."+k.upper()+"\n\t"+v+"\n\n"

    def get_param_item(self,  k, v):
        paramTemplate = Template(
            '''.PARAMETER\t${paramKey}\n\t${paramDescription}\n\n''')
        return paramTemplate.substitute(
            paramKey=k, paramDescription=v)

    def write_header(self):
        self.output.write('<#\n')
        self.output.write(self.get_item(
            'SYNOPSIS', 'Autogenerated from ' + os.path.basename(self.origin_file)))
        self.output.write(self.get_item(
            'DESCRIPTION', self.description))

        for key, value in self.parameters:
            desc = key + " [" + value["type"] + "]"
            try:
                for pkey, pvalue in value["metadata"].items():
                    if(pkey == "description"):
                        desc = pvalue
            except:
                pass
            self.output.write(self.get_param_item(key, desc))

        if self.links is not None:
            self.output.write(self.get_item('LINK', '\n'.join(self.links)))
    
        self.output.write("\n#>\n")
