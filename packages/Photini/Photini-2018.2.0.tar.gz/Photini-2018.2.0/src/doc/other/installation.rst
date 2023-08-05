.. This is part of the Photini documentation.
   Copyright (C)  2012-18  Jim Easterbrook.
   See the file DOC_LICENSE.txt for copying conditions.

Installation
============

There are three ways to install Photini.
On Windows you can use an all-in-one installer.
On some Linux distributions you might be able to use your package manager to install everything, or you may be able to use the package manager to install Photini's dependencies and pip_ to install Photini.
On other platforms you need to install several dependencies before installing Photini.

All-in-one installer (Windows)
------------------------------

The Windows installer creates a standalone Python installation with all the dependencies needed to run Photini.
The standalone Python interpreter is only used to run Photini, and should not conflict with any other Python version installed on your computer.

You can download the latest Windows installer from the `GitHub releases`_ page.
Look for the most recent release with a ``.exe`` file listed in its downloads.
This is a Windows installer for the latest version of Photini, even if it's listed under an older release.
The installer is suitable for 32 bit and 64 bit Windows, and should work on any version since Windows XP.

When you run the installer you will probably get a security warning because the installer is not signed by a recognised authority.
This is unavoidable unless I purchase a certificate with which to sign the installer.
As I don't make any money from Photini this is unlikely to happen!

The installer should finish by running the Photini program.
If this works then you have successfully installed Photini and can ignore the rest of these instructions.
If not, see the troubleshooting_ section below.

Upgrading all-in-one installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before upgrading Photini you should check the `GitHub releases`_ page to see if a new Windows installer has been released since you last downloaded it.
If it hasn't, then you can use the "upgrade Photini" command in the start menu.
This needs to be run as administrator.
Click on the "Start" icon, then select "All Programs", then "Photini", then right-click on "upgrade Photini" and choose "Run as administrator" from the context menu.

If there is a new installer available then you should download it and use it to create a fresh installation, after using the "Programs and Features" control panel item to uninstall the old version of Photini.

Package manager (some Linux distributions)
------------------------------------------

.. note:: These Linux packages are maintained by other people and may not install the latest version of Photini.
   You may also need to install missing dependencies, as described below.

Ubuntu and derived systems
^^^^^^^^^^^^^^^^^^^^^^^^^^

Dariusz Duma (https://launchpad.net/~dhor) has added Photini to his PPA (personal package archive).
See the instructions at http://linuxg.net/how-to-install-photini-15-01-1-on-ubuntu-14-10-ubuntu-14-04-and-derivative-systems/.

Pascal Mons (https://launchpad.net/~anton+) also has a PPA with many photo applications, including Photini.
See https://launchpad.net/~anton+/+archive/ubuntu/photo-video-apps/.

OpenSUSE 42.2 or newer
^^^^^^^^^^^^^^^^^^^^^^

Photini is available from the Packman community repository.
It can be installed by clicking on this link: http://packman.links2linux.org/install/Photini

OpenSUSE and Fedora
^^^^^^^^^^^^^^^^^^^

Togan Muftuoglu (https://build.opensuse.org/user/show/toganm) has created a python-photini package.
See https://build.opensuse.org/package/show/home:toganm:photography/python-photini for more information.

Dependencies package (some Linux distributions)
-----------------------------------------------

This is the easiest way to install Photini's dependencies and the latest release of Photini.
You use your package manager to install the non-Python dependencies, then use pip_ to install the latest versions of all the Python packages.

OpenSUSE (and other Red Hat derived distributions?)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Photini project includes a ``.spec`` file that lists the required dependencies.
Download the ``.spec`` file and use it to build a ``.rpm`` file::

   wget https://raw.githubusercontent.com/jim-easterbrook/Photini/master/src/linux/python3-photini-meta.spec
   rpmbuild -ba python3-photini-meta.spec

Note where ``rpmbuild`` wrote its output file, then install that file. For example::

   sudo zypper install /home/jim/rpmbuild/RPMS/noarch/python3-photini-meta-1-0.noarch.rpm

Now you can :ref:`install Photini <installation-photini>` using pip_ as described below.

Piecemeal installation
----------------------

This is the hardest way to install Photini, mainly because of the libraries required to access photographs' metadata.
The installation process is different for Windows, Linux and MacOS, and there are variations with different versions of those operating systems.
If you run into problems, please let me know (email jim@jim-easterbrook.me.uk) and once we've worked out what needs to be done I'll be able to improve these instructions.

Essential dependencies
----------------------

These are all required for Photini to be usable.

Python
^^^^^^

Photini should work with all versions of `Python <https://www.python.org/>`_ from 2.6 onwards.

Python may already be installed on your computer.
To find out, open a terminal window (Windows users run ``cmd.exe``) and try running python by typing this command::

   python -V

If Python is installed this should show you the version number.

Linux users should use their system's package manager to install Python.
Windows and MacOS users can download an installer from https://www.python.org/downloads/.
Windows users should install the 32 bit version of Python, even on a 64 bit machine.
This is because some of the required libraries are not available in 64 bit builds.

PyQt
^^^^

The `PyQt <http://www.riverbankcomputing.co.uk/software/pyqt/>`_ application framework provides the graphical user interface elements used by Photini.
Version 4 or 5 is required.

You can check if PyQt is already installed with one of these commands::

   python -c "import PyQt5"

or ::

   python -c "import PyQt4"

If PyQt is installed then one of these will run without generating any error message.

Linux users should use their package manager to install ``python-qt4`` or ``python-qt5``.
On some Linux systems you may also need to install the Qt WebKit package, e.g. ``qt5-webkit``.
Windows users can download a binary installer from http://www.riverbankcomputing.co.uk/software/pyqt/download5 (make sure you choose the installer for your version of Python).

gexiv2
^^^^^^

Several libraries are needed to access photograph metadata from Python.
`Exiv2 <http://www.exiv2.org/>`_ is the core "C" library.
`gexiv2 <https://wiki.gnome.org/Projects/gexiv2>`_ is a GObject wrapper around the Exiv2 library.
It has extra "introspection bindings" that allow it to be used by other languages.
`PyGObject <https://wiki.gnome.org/Projects/PyGObject>`_ (also known as PyGI) provides a Python interface to the introspection bindings of the GObject wrapper around the Exiv2 library.
Got that?

Linux users should use their package manager to install these, but note that the package names may not be obvious.
The core gexiv2 wrapper is probably called ``libgexiv2`` or similar, but on my OpenSUSE system the introspection bindings are called ``typelib-1_0-GExiv2-0_4`` whereas on Ubuntu systems they are called ``gir1.2-gexiv2-0.4``.
The PyGObject interface probably appears in the package manager as ``python-gobject`` or ``python-gi``.

Windows users should download and run the latest "pygi-aio" (PyGI all-in-one) installer from http://sourceforge.net/projects/pygobjectwin32/files/.
You should install the "Base packages" & "GExiv2" packages, and the "Enchant-extra-dicts" non-GNOME library.

pip
^^^

The remaining dependencies are Python packages that are easily installed with `pip <https://pip.pypa.io/en/latest/>`_.
You may already have pip installed on your computer.
You can check with the ``pip list`` command::

   pip list

Linux users should use their package manager to install ``python-pip``.
Windows and MacOS users can use the installer from https://pip.pypa.io/en/latest/installing.html#install-pip.
All users should then `upgrade pip <https://pip.pypa.io/en/latest/installing.html#upgrade-pip>`_.

.. _installation-photini:

Installing Photini
------------------

The easiest way to install the latest release of Photini is with the pip_ command::

   sudo pip install photini

This will install Photini and any Python packages it requires.
You can also use pip to install the optional dependencies when you install Photini::

   sudo pip install photini[flickr,google,facebook,importer,spelling]

If you prefer to install the development version you can use git to clone the `GitHub repository <https://github.com/jim-easterbrook/Photini>`_ or download it as a zip file and then unpack it.
Either way, you then need to build and install Photini::

   python setup.py build
   sudo python setup.py install

You will also need to install the remaining Python packages.

Essential Python packages
^^^^^^^^^^^^^^^^^^^^^^^^^

There are two small Python packages needed to run Photini.
They can be installed with one command::

   sudo pip install six appdirs

Note that ``sudo`` is not required on Windows, or if you have root privileges.
In this case you just run ``pip install six appdirs``.

Optional Python packages
^^^^^^^^^^^^^^^^^^^^^^^^

Some of Photini's features are optional - if you don't install these libraries Photini will work but the relevant feature will not be available.

Spelling
""""""""

`PyEnchant <http://pythonhosted.org/pyenchant/>`_ is a Python interface to the `Enchant <http://www.abisource.com/projects/enchant/>`_ spell-checking library.
If it is installed then spell checking is available for some of Photini's text entry fields.
Use pip_ to install it::

   sudo pip install pyenchant

.. _installation-flickr:

Flickr
""""""

Photini's Flickr uploader requires `python-flickrapi <https://pypi.python.org/pypi/flickrapi/>`_ and `python-keyring <https://pypi.python.org/pypi/keyring/>`_.
These are easily installed with pip::

   sudo pip install flickrapi keyring

.. _installation-picasa:

Google Photos / Picasa
""""""""""""""""""""""

The Google Photos / Picasa uploader requires `requests <https://github.com/kennethreitz/requests>`_, `requests-oauthlib <https://github.com/requests/requests-oauthlib>`_ and `python-keyring <https://pypi.python.org/pypi/keyring/>`_.
These are also installed with pip::

   sudo pip install requests requests-oauthlib keyring

.. _installation-facebook:

Facebook
""""""""

The Facebook uploader requires `requests <https://github.com/kennethreitz/requests>`_, `requests-oauthlib <https://github.com/requests/requests-oauthlib>`_, `requests-toolbelt <https://toolbelt.readthedocs.io/>`_ and `python-keyring <https://pypi.python.org/pypi/keyring/>`_.
These are also installed with pip::

   sudo pip install requests requests-oauthlib requests-toolbelt keyring

The ``Optimise image size`` option requires the `Python Imaging Library <http://pillow.readthedocs.io/>`_, which is also installed with pip::

   sudo pip install Pillow

.. _installation-thumbnail:

Thumbnail creation
""""""""""""""""""

If the Python Imaging Library (see above) is installed then Photini can make good quality thumbnails.
Otherwise it uses Qt's image resizing which may produce rather soft results.

Creating a thumbnail image from a video requires the `OpenCV <http://opencv.org/>`_ image processing library (including its Python interface) and the `NumPy <http://www.numpy.org/>`_ "numerical Python" package.
These should both be installed with your system's package manager, as they depend on C libraries that cannot be installed with pip.

You may still find that Photini can't read image data from video files.
Running it from the command line (see troubleshooting_) may show why.
(The OpenCV library writes messages to the console rather than raise a Python exception.)

.. _installation-importer:

Importer
""""""""

Photini can import pictures from any directory on your computer (e.g. a memory card) but on Linux and MacOS systems it can also import directly from a camera.
This requires `libgphoto2 <http://www.gphoto.org/proj/libgphoto2/>`_, which is often already installed, and its `python-gphoto2 <https://pypi.python.org/pypi/gphoto2/>`_ Python bindings, version 0.10 or greater::

   sudo pip install -v gphoto2

Installation of python-gphoto2 will require the "development headers" versions of Python and libgphoto2.
You should be able to install these with your system package manager.

pgi
"""

If you find the PyGObject bindings to be unreliable (I found they sometimes crash when using Python 3) you can use `pgi <https://pypi.python.org/pypi/pgi/>`_ instead::

   sudo pip install pgi

Note that pgi may also have problems.
If you need to go back to using PyGObject you should uninstall pgi::

   sudo pip uninstall pgi

Running Photini
---------------

If the installation has been successful you should be able to run Photini from the "Start" menu (Windows) or application launcher (Linux).

.. _installation-troubleshooting:

Troubleshooting
^^^^^^^^^^^^^^^

If Photini fails to run for some reason you may be able to find out why by trying to run it in a command window.
On Windows you need to open the folder where Photini is installed (probably ``C:\Program Files (x86)\Photini``) and run the ``WinPython Command Prompt.exe`` program.
On Linux you can run any terminal or console program.

Start the Photini program as follows.
If it fails to run you should get some diagnostic information::

   python -m photini.editor

If you need more help, please email jim@jim-easterbrook.me.uk.
It would probably be helpful to copy any diagnostic messages into your email.
I would also find it useful to know what version of Photini and some of its dependencies you are running.
You can find out with the ``--version`` option::

   python -m photini.editor --version

Some versions of PyQt may fail to work properly with Photini, even causing a crash at startup.
If this happens you may be able to circumvent the problem by editing the :ref:`Photini configuration file <configuration-pyqt>` before running Photini.

Mailing list
------------

For more general discussion of Photini (e.g. release announcements, questions about using it, problems with installing, etc.) there is an email list or forum hosted on Google Groups.
You can view previous messages and ask to join the group at https://groups.google.com/forum/#!forum/photini.

.. _installation-documentation:

Photini documentation
---------------------

If you would like to have a local copy of the Photini documentation, and have downloaded or cloned the source files, you can install `Sphinx <http://sphinx-doc.org/index.html>`_ and use setup.py to "compile" the documentation::

   sudo pip install sphinx
   python -B setup.py build_sphinx

Open ``doc/html/index.html`` with a web browser to read the local documentation.

.. _GitHub releases: https://github.com/jim-easterbrook/Photini/releases
