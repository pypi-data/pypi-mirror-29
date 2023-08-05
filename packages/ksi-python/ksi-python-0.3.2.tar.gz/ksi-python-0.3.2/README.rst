KSI Python SDK
==============

This is a thin wrapper on top of KSI C SDK. Experimental, non-supported code.

Synopsis
--------

.. code-block:: python

    import ksi
    import hashlib

    # Instantiate service parameters from the environment
    KSI = ksi.KSI(**ksi.ksi_env())

    # Sign a text string
    sig = KSI.sign_hash(hashlib.sha256(b"Tere!"))
    # Print some signature properties
    print(sig.get_signing_time(), sig.get_signer_id())

    # Now verify this text string, first obtaining a data hasher
    h = sig.get_hasher()
    h.update(b"Tere!")
    print(KSI.verify_hash(sig, h))

    # Obtain a binary blob which can be stored for long term
    serialized_signature = sig.serialize()

    # Some time have passed, fetch the signature and verify again
    sig2 = KSI.parse(serialized_signature)
    KSI.set_verification_policy(KSI.verification.POLICY_CALENDAR_BASED)
    print(KSI.verify_hash(sig2, h))


Install
-------

#. Requirements: Python 2.7+ or Python 3.1+. Jython, IronPython do not work.

#. Install fresh libksi aka KSI C SDK; see https://github.com/guardtime/libksi/

#. Install python-devel package

#. Run::

    > pip install ksi-python

or

    > easy_install ksi-python

Tests
-----
Specify KSI Gateway access parameters and run
::

    > python setup.py test


Documentation
-------------

http://guardtime.github.io/ksi-python/

Type::

    > pydoc ksi

to read the documentation after installation. Generating html or pdf documentation:
make sure that dependencies like sphinx (``pip install sphinx``) are installed and run::

   > cd docs
   > make html
   > make latexpdf


Limitations
-----------
  * Synchronous calls--especially signing--block green threads.
  * Advanced functions like block signing, containers, async operations, are not implemented.
  * Python's __del__ destructor is not guaranteed to execute. Please help garbage collector
    by dereferencing unnecessary signature objects with ``del``.


License
-------
Apache 2.0. Please contact Guardtime for supported options.
