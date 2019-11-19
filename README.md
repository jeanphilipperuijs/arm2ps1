# ARM2PS1

## Run

### Generate a Powershell script from one ARM template

```bash
psf = Powershellfest('./mytemplate.json', overwrite = False)
psf.generate()
```

This command generates `mytemplate.ps1` prompting for overwrite

### crawling all subdirectories

Run using environment variable

```bash
TEMPLATEPATH2CRAWL=./templates/network python3 ./crawler.py
```

Run using argument

```bash
python3 ./crawler.py ./templates/network
```
