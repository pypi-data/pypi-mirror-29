# dfgen

CLI tool for generating CD related templates like Dockerfiles

### CLI options
```
dfgen [OPTIONS] COMMAND [ARGS]...

  A little tool to generate commonly used ci/cd templates like Dockerfiles.

Options:
  -v, --verbose        enable/disable verbose messages
  -w, --write-to-file  write generated template to file
  -h, --help           Show this message and exit.

Commands:
  docker      Docker mode, this will create a Dockerfile
```

## Development
Gener8 uses Python3, it will break in python2.
Using a virtual environment is recommended.

## installing locally
```
pip install . --upgrade
```

### testing
Basic unittests can be run by:
```
pytest
```

### linting
Just running pylint will break on new python3 syntax, instead use:
```
python3 -m pylint <path>
```

or with reporting:
```
python3 -m pylint --reports=yes <path>
```

For pep8 compliance use: 
```
pycodestyle --show-source --show-pep8
```

## Wishlist

* kubernetes template(s)
* automated tests for dockerfile
* security checks

* auto detect dominant programming language in repository and generate useable dockerfile
