=======
Vampire
=======

To install Vampire, execute::

  cd package
  python setup.py build
  python setup.py install

The "install" phase may need to be done as "root", using the "sudo"
command or other means as may be appropriate for your system.

Make sure you read the PATCHES_ file to see if you may need to patch the
version of mod_python you are using. The patches are recommended if you
are working with a multithread MPM for Apache.

The package is being made available under a BSD style license, the details
of which can be found in the LICENSE_ file.

Online documentation for Vampire can be found at:

  http://www.dscpl.com.au/projects/vampire

The source code for the current working copy of Vampire, including some
examples not included with the actual release, can be viewed at:

  http://svn.dscpl.com.au/vampire/trunk

If you have any questions, it is suggested you subscribe to the mod_python
mailing list and ask your question there. Alternatively, you can contact
the author directly at "grahamd@dscpl.com.au".

.. _PATCHES: PATCHES.html
.. _LICENSE: LICENSE.html
