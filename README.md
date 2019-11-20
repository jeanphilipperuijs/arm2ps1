# ARM2PS1
![alt text](arm2psi.png "title")
Generate a Powershell script from one ARM template to deploy the resources in a resource group `New-AzResourceGroupDeployment`

## HowTo

### Template file

This python code takes an *ARM template* (eg. `mytemplate.json`) as input and generates `mytemplate.ps1`.

#### Parameters

* `arm_template_file` is mandatory
* `resourceGroup` and `overwrite` are optional, both defaults to `None` or `False`

```bash
psf = ARM2Powershellfest('./mytemplate.json', resourceGroup = None, overwrite = False)
psf.init()
```

### Batch
| ENV VAR               | desc                                    | default       |
|-----------------------|-----------------------------------------|---------------|
| ARMTEMPLATEPATH2CRAWL | path to crawl                           | none          |
| RESOURCEGROUP         | default ResourceGroup to use in scripts | none          |
| ARM2PS1LOGFILE        | target log output                       | ~/arm2ps1.log |
| ARM2PS1LOGLEVEL       | logging level                           | 20 (info)     |

`crawler.py` is an example script which crawls a given directory for template files.

**NB** By default  the parameter is set to `overwrite = 'a'` which overwrites existing files.

Run using environment variable

```bash
TEMPLATEPATH2CRAWL=./templates python3 ./crawler.py
```

Run using argument which ovrerrides path set in environment

```bash
python3 ./crawler.py ./templates
```
