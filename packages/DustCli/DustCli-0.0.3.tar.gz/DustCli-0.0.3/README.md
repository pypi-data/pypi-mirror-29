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
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
```

Installation
------------

```
$ pip install -r requirements.txt

$ python setup.py install
```

iOS
-------
dust init

dust project new --ios
dust module new --ios
dust feature new --ios
dust feature new --ios --only-view
dust feature new --ios --only-vm
dust feature new --ios --only-model

dust publish [spec path] --
dust 



