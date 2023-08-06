DustCli
==============================================================================

Debug
-----

```
virtualenv ./env

source ./env/bin/activate

pip install -r requirements.txt

python setup.py develop

dust --help
```

Publish
-------
```
python3 setup.py sdist
python3 setup.py bdist_wheel
twine upload dist/*
```

Installation
------------

```
pip3 install -r requirements.txt

python3 setup.py install
```

iOS
-------
dust init  

dust project new --ios  
