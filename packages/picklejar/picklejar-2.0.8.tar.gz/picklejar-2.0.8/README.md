## Overview

[picklejar][] is a python module that allows you to work with multiple pickles while reading/writing them to a single file/jar.

## License

[picklejar][] is released under the [GNU Lesser General Public License v3.0][],
see the file LICENSE and LICESE.lesser for the license text.

## Compatibility

As of version 2.0, picklejar is compatible with the latest versions of Python2 and Python3!

## Installation

The most straightforward way to get the picklejar module working for you is:

> pip install picklejar

or

> python setup.py install

This will ensure that all the requirements are met.

### Development Installation

To install the packages required to build the Sphinx Documenation simply:

> pip install -U -r requirements.txt

This will install all the requirements to work on picklejar and build the docs!

### Automated Testing

Picklejar uses [Tox] to support automated testing across multiple versions of Python.  To run the tox tests after installing
the `requirements.txt` file, run:

> tox

At the time of this writing, we are testing the following versions of Python:

* Python2.7
* Python3.5
* Python3.6
* PyPY 5.7.0

**NOTE:** You must have the versions of Python installed that you wish to test against or your tox will fail!

## Documentation

All documentation for using picklejar can be found at http://picklejar.readthedocs.io/

## Contributing

Comments and enhancements are very welcome.

Report any issues or feature requests on the [BitBucket bug
tracker](https://bitbucket.org/isaiah1112/picklejar/issues?status=new&status=open). Please include a minimal
(not-) working example which reproduces the bug and, if appropriate, the
 traceback information.  Please do not request features already being worked
towards.

Code contributions are encouraged: please feel free to [fork the
project](https://bitbucket.org/isaiah1112/picklejar) and submit pull requests to the develop branch.


[GNU Lesser General Public License v3.0]: http://choosealicense.com/licenses/lgpl-3.0/ "LGPL v3"

[picklejar]: https://bitbucket.org/isaiah1112/picklejar "picklejar Module"

[tox]: https://tox.readthedocs.io/en/latest/index.html
