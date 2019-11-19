# ARM2PS1

Generate a Powershell script from one ARM template

## Run

### Simple file

This command generates `mytemplate.ps1` prompting for overwrite.

* `arm_template_file` is mandatory
* `resourceGroup` and `overwrite` are optional, both defaults to `None` or `False`

```bash
psf = Powershellfest('./mytemplate.json', resourceGroup = None, overwrite = False)
psf.generate()
```

### Crawl all subdirectories searching for templates

Run using environment variable

```bash
TEMPLATEPATH2CRAWL=./templates/network python3 ./crawler.py
```

Run using argument

```bash
python3 ./crawler.py ./templates/network
```
