# Deep Teaching Commons

This Python module is part of the [deep.TEACHING](http://www.deep-teaching.org) project and provides common
functionality across Jupyter notebooks and teaching materials.

## Installation

Option 1: Install in user's home directory

```bash
pip3 install --user deep-teaching-commons
```

Option 2: Install in a virtual environment

```bash
pip3 install --user virtualenv
# create virtual environment called venv
virtualenv venv
source venv/bin/activate
pip install deep-teaching-commons
```

Option 3: Install from source
```bash
git clone https://gitlab.com/deep.TEACHING/deep-teaching-commons.git
pip3 install --user ./deep-teaching-commons/
```

## Developer Documentation

Distribute on PyPI:

```bash
# get code
git clone https://gitlab.com/deep.TEACHING/deep-teaching-commons.git
cd deep-teaching-commons
# make code changes and update setup.py
vi setup.py
# create tarball
python3 setup.py sdist
# upload tarball
pip3 install --user twine
twine upload dist/deep-teaching-commons-0.1
```

## License

[MIT](/LICENSE)

## Acknowledgements

The Deep Teaching Commons software is developed at HTW Berlin - University of Applied Sciences.

The work is supported by the German Ministry of Education and Research (BMBF).
