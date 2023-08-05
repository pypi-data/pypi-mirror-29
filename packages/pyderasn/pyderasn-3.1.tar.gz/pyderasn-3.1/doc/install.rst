Install
=======

Preferable way is to :ref:`download <download>` tarball with the
signature from `official website <http://pyderasn.cypherpunks.ru/>`__::

    % wget http://pyderasn.cypherpunks.ru/pyderasn-3.0.tar.xz
    % wget http://pyderasn.cypherpunks.ru/pyderasn-3.0.tar.xz.sig
    % gpg --verify pyderasn-3.0.tar.xz.sig pyderasn-3.0.tar.xz
    % xz -d < pyderasn-3.0.tar.xz | tar xf -
    % cd pyderasn-3.0
    % python setup.py install
    # or copy pyderasn.py (+six.py) to your PYTHONPATH

PyDERASN depends on `six <https://pypi.python.org/pypi/six>`__ package
for keeping compatibility with Py27/Py35. It is included in the tarball.
You can also find it mirrored on :ref:`download <download>` page.

You could use PIP (**no** authentication is performed!)::

    % pip install pyderasn

You have to verify downloaded tarballs integrity and authenticity to be
sure that you retrieved trusted and untampered software. `GNU Privacy
Guard <https://www.gnupg.org/>`__ is used for that purpose.

For the very first time it is necessary to get signing public key and
import it. It is provided below, but you should check alternative
resources.

::

    pub   rsa2048/0x04A933D1BA20327A 2017-09-20
          2ED6 C846 3051 02DF 5B4E  0383 04A9 33D1 BA20 327A
    uid   PyDERASN releases <pyderasn@cypherpunks.ru>

    % gpg --keyserver hkp://keys.gnupg.net/ --recv-keys 0x04A933D1BA20327A
    % gpg --auto-key-locate dane --locate-keys pyderasn at cypherpunks dot ru
    % gpg --auto-key-locate wkd --locate-keys pyderasn at cypherpunks dot ru
    % gpg --auto-key-locate pka --locate-keys pyderasn at cypherpunks dot ru

.. literalinclude:: ../PUBKEY.asc
