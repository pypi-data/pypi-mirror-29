# ndarray-listener

[![Travis](https://img.shields.io/travis/limix/ndarray-listener.svg?style=flat-square&label=linux%20%2F%20macos%20build)](https://travis-ci.org/limix/ndarray-listener) [![AppVeyor](https://img.shields.io/appveyor/ci/Horta/ndarray-listener.svg?style=flat-square&label=windows%20build)](https://ci.appveyor.com/project/Horta/ndarray-listener) [![Read the Docs (version)](https://img.shields.io/readthedocs/ndarray-listener/stable.svg?style=flat-square)](http://ndarray-listener.readthedocs.io/)

Implementation of the [Observer pattern](https://en.wikipedia.org/wiki/Observer_pattern) for NumPy arrays.

## Example

```python
from numpy import array
from ndarray_listener import ndarray_listener as ndl

a = ndl(array([-0.5, 0.1, 1.1]))

class Observer(object):
  def __init__(self):
    self.called_me = False

  def __call__(self, _):
    self.called_me = True

o = Observer()
a.talk_to(o)
print(o.called_me)
a[0] = 1.2
print(o.called_me)
```

The output should be

```
False
True
```

## Install

From command line, enter

```bash
pip install ndarray-listener
```

## Running the tests

Install dependencies

```bash
pip install -U pytest pytest-pep8
```

then run

```python
python -c "import ndarray_listener; ndarray_listener.test()"
```

## Authors

* [Danilo Horta](https://github.com/horta)


## License

This project is licensed under the [MIT License](https://raw.githubusercontent.com/limix/ndarray-listener/master/LICENSE.md).
