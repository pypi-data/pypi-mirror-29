# Simplified GPG exchange wrapper

[![PyPI](https://img.shields.io/pypi/v/gpg-exchange.svg)](https://pypi.python.org/pypi/gpg-exchange)

This module abstracts some of the data types and operations performed by the
[GPG Made Easy](https://pypi.python.org/pypi/gpg) library in order to provide 
a single means of key generation,
public key exchange, encryption and decryption using 
[GnuPG](https://www.gnupg.org/)/PGP.

## Features

- Retrieve passphrase via callback
- Key generation
- Key search and deletion
- Key import and export
- Encryption and decryption using normal string types or open files

## Requirements

The expression parser has been tested to work on Python 2.7 and 3.6. This 
package depends on the [gpg](https://pypi.python.org/pypi/gpg) library, which 
itself depends on [SWIG](http://www.swig.org/) and recent versions of the
[GPGME](https://www.gnupg.org/software/gpgme/index.html) library plus 
associated development headers. GPGME then depends on GnuPG 2.1+ and its 
libraries. You can install some of these packages through your package manager 
if it is recent enough (search for `gpg2`). Even then you may still need a more 
recent version of libgpg-error, for example.

You can install the missing or outdated packages from source using the [latest 
tarballs](https://www.gnupg.org/download/index.html).
Start with the library packages, then make sure you have GnuPG and finally 
install GPGME for the easiest workflow. Each time, use `./configure`, `make` 
and finally `sudo make install`. If the first two steps fail then the output 
will usually indicate which packages are missing. GPGME may fail its tests if 
you are using an older version of GnuPG, which can be overcome by running only 
`./configure` and `sudo make install` or by `sed -i 's/gpgconf --kill 
all/gpgconf --kill gpg-agent scdaemon/' tests/gpg/Makefile tests/gpgsm/Makefile 
lang/python/tests/Makefile lang/qt/tests/Makefile` when the compilation fails.

For GnuPG 2.1, you may need to add `allow-loopback-pinentry` to 
`$HOME/.gnupg/gpg-agent.conf` in order to use passphrase callbacks. This is no 
longer required in GnuPG 2.2. Key generation must provide a passphrase in GnuPG 
2.2+.

## Installation

Install the latest version from PyPI using:

```
pip install gpg-exchange
```

## License

The GPG wrapper library is licensed under the GNU General Public License.
