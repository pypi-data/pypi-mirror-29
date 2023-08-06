.. -*- rst -*- -*- restructuredtext -*-

.. This file should be written using the restructure text
.. conventions.  It will be displayed on the bitbucket source page and
.. serves as the documentation of the directory.

.. |virtualenv.py| replace:: ``virtualenv.py``
.. _virtualenv.py: https://raw.github.com/pypa/virtualenv/master/virtualenv.py

.. |EPD| replace:: Enthough Python Distribution
.. _EPD: http://www.enthought.com/products/epd.php
.. _Anaconda: https://store.continuum.io/cshop/anaconda
.. _Conda: http://docs.continuum.io/conda
.. _Miniconda: http://conda.pydata.org/miniconda.html

.. _Enthought: http://www.enthought.com
.. _Continuum Analytics: http://continuum.io

.. _Spyder: https://code.google.com/p/spyderlib/
.. _Wakari: https://www.wakari.io
.. _Canopy: https://www.enthought.com/products/canopy/

.. _mercurial: http://mercurial.selenic.com/
.. _virtualenv: http://www.virtualenv.org/en/latest/
.. _IPython: http://ipython.org/
.. _Ipython notebook: \
   http://ipython.org/ipython-doc/dev/interactive/htmlnotebook.html
.. _NBViewer: http://nbviewer.ipython.org
.. |pip| replace:: ``pip``
.. _pip: http://www.pip-installer.org/
.. _git: http://git-scm.com/
.. _github: https://github.com
.. _RunSnakeRun: http://www.vrplumber.com/programming/runsnakerun/
.. _GSL: http://www.gnu.org/software/gsl/
.. _pygsl: https://bitbucket.org/mforbes/pygsl
.. _Sphinx: http://sphinx-doc.org/
.. _SciPy: http://www.scipy.org/
.. _Mayavi: http://code.enthought.com/projects/mayavi/
.. _NumPy: http://numpy.scipy.org/
.. _Numba: https://github.com/numba/numba#readme
.. _NumbaPro: http://docs.continuum.io/numbapro/
.. _Blaze: http://blaze.pydata.org
.. _Python: http://www.python.org/
.. _matplotlib: http://matplotlib.org/
.. _Matlab: http://www.mathworks.com/products/matlab/
.. _MKL: http://software.intel.com/en-us/intel-mkl
.. _Intel compilers: http://software.intel.com/en-us/intel-compilers
.. _Bento: http://cournape.github.com/Bento/
.. _pyaudio: http://people.csail.mit.edu/hubert/pyaudio/
.. _PortAudio: http://www.portaudio.com/archives/pa_stable_v19_20111121.tgz
.. _MathJax: http://www.mathjax.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _Emacs: http://www.gnu.org/software/emacs/
.. _Pymacs: https://github.com/pinard/Pymacs
.. _Ropemacs: http://rope.sourceforge.net/ropemacs.html
.. _PyPI: https://pypi.python.org/pypi

.. _FFTW: http://www.fftw.org
.. _EC2: http://aws.amazon.com/ec2/
.. _QT: http://qt.digia.com

.. |site.USER_BASE| replace:: ``site.USER_BASE``
.. _site.USER_BASE: https://docs.python.org/2/library/site.html#site.USER_BASE


.. default-role:: math

.. This is so that I can work offline.  It should be ignored on bitbucket for
.. example.

.. sidebar:: Sidebar

   .. contents::

===========
 mmf_setup
===========
This meta-project provides an easy way to install all of the python
tools I typically use.  It also serves as a fairly minimal example of
setting up a package the |pip|_ can install, and specifying
dependencies.

In particular, I structure it for the following use-cases:

1. Rapid installation and configuration of the tools I need.  For
   example, I often use [Sage Mathcloud](cloud.sagemath.com).
   Whenever I create a new project, I need to perform some
   initialization.  With this project, it is simply a matter of using
   |pip|_ to install this package, and then using some of the tools.
2. Initial setup of a python distribution on a new computer.  This is
   a little more involved since one needs to first install python (I
   recommend using Miniconda_) and then updating the tools.
3. A place to document various aspects of installing and setting up
   python and related tools.  Some of this is old, but kept here for
   reference.


====================
 Quickstart (TL;DR)
====================

1. To get the notebook initialization features without having to install the
   package, just copy `nbinit.py <nbinit.py>`_ to your project.  Importing this
   will try to execute `import mmf_setup;mmf_setup.nbinit()` but failing this,
   will manually run a similar code.

2. Install this package from the source directory, PyPI_, etc. with
   one of the following:
  
   * **Directly from PyPI**

     ``pip install --process-dependency-links --user mmf_setup[nbextensions]``

   * **From Source**

     ``pip install --process-dependency-links --user hg+https://bitbucket.org/mforbes/mmf_setup[nbextensions]``

   * **From Local Source** (*Run this from the source directory after you unpack it.*)

     ``pip install --process-dependency-links --user .[nbextnensions]``

   Note: these can be run without the ``--user`` flag if you want to
   install them system-wide rather than into |site.USER_BASE|_.

3. To get the notebook tools for Jupyter (IPython) notebooks, execute
   the following as a code cell in your notebook and then trust the
   notebook with ``File/Trust Notebook``::

       import mmf_setup; mmf_setup.nbinit()

   This will download and enable the calico extensions, as well as set
   the theme which is implemented in the output cell so it is stored
   for use online such as when rendered through NBViewer_.  One can
   specify different themes. (Presently only ``theme='default'`` and
   ``theme='mmf'`` are supported.)

4. To use the mercurial notebook cleaning tools, simply source the
   ``mmf_setup`` script::

      . mmf_setup -v

   To do this automatically when you login, add this line to your
   ``~/.bashc`` or ``~/.bash_profile`` scripts.  These can also be
   enabled manually by adding the following to your ``~/.hgrc`` file::

     [extensions]
     strip=
     mmf_setup.nbclean=$MMF_UTILS/nbclean.py


   where ``$MMF_UTILS`` expands to the install location for the
   package (which can be seen by running ``mmf_setup -v``).

   This will provide commands for committing clean notebooks such as
   ``hg cstatus``, ``hg cdiff`` and ``hg ccommit``.


==================
 Installing Tools
==================

The following code will download and install the `Calico notebook
extensions`__ from `here`__::

      import mmf_setup.notebook_configuration
      mmf_setup.notebook_configuration.install_extensions()

======================
 Mercurial (hg) Tools
======================

If you source the output of the ``mmf_setup`` script::

   . mmf_setup

then your ``HGRCPATH`` will be amended to include this projects
``hgrc`` file which does the following:

1. Adds some useful extensions.
2. Adds the following commands:

   * ``hg lga`` (or ``hg lg``): provides a nice concise graphical
     display of the repo.
   * ``hg cstatus`` (or ``hg cst``):
   * ``hg cdiff``: same for ``hg diff``
   * ``hg cediff``: same for ``hg ediff``
   * ``hg crecord``: same for ``hg record``.  Note, this does not
     function like commit - it will not record the notebooks with the
     full output.
   * ``hg ccommit`` (or ``hg ccom``): same for ``hg com`` but also
     commits the full version of the notebooks with output as a new
     node off the present node with the message ``..: Automatic commit of
     output``.  This command has two behaviours depending on the
     configuration option ``nbclean.output_branch``.  If this is not
     set::

       [nbclean]
       output_branch =

     then ``hg ccommit`` will commit a cleaned copy of your notebooks
     with the output stripped, and then will commit the full notebook
     with output (provided that the notebooks have output) as a new
     head::

       | o  4: test ...: Automatic commit with .ipynb output
       |/
       @  3: test ccommit 3
       |
       | o  2: test ...: Automatic commit with .ipynb output
       |/
       o  1: test ccommit 1
       |
       o  0: test commit 0

     The parent will always be set to the clean node so that the output
     commits can be safely stripped from your repository if you choose
     not to keep them.

     The other mode of operation can be enabled by specifying a name for
     the output branch::

       [nbclean]
       output_branch = auto_output

     This will merge the changes into a branch with the specified name::

       | o  4: test ...: Automatic commit with .ipynb output (...) auto_output
       |/|
       @ |  3: test ccommit 3
       | |
       | o  2: test ...: Automatic commit with .ipynb output (...) auto_output
       |/
       o  1: test ccommit 1
       |
       o  0: test commit 0

     This facilitates stripping the output ``hg strip 2`` for example
     will remove all output.  It also allows you to track the changes in
     the output.


Developer Notes
---------------

There are a couple of subtle points here that should be mentioned.

* I explored both ``(un)shelve`` and ``commit/strip`` versions of
  saving the current state.  While the former allows for shorter
  aliases, it can potentially trigger merges, so we use the latter.
* I sometimes write commit hook.  These should only be run on the real
  commit, so we define the alias ``_commit`` which will bypass the
  hooks as `discussed here`__.
* The list of files to strip is generated by ``hg status -man``.  This
  only includes added or modified files.  This, if a notebook was
  commited with output (using ``hg com``) then it will not be
  stripped.
* Our approach of ``. mmf_setup`` sets ``HGRCPATH`` but if this was
  not set before, then this will skip the default search.  As such, we
  insert ``~/.hgrc`` if ``HGRCPATH`` was not previously set.  This is
  not ideal, but short of sticking an ``%include`` statement in the
  users ``~/.hgrc`` file, or creating an ``hg`` alias, I do not see a
  robust solution.  Note: we only insert ``~/.hgrc`` if ``HGRCPATH``
  is not defined - I ran into problems when always inserting it since
  this can change the order of precedence.
* Chain commands with semicolons ``;`` not ``&&`` so that things are
  restored even if a command fails.  (For example, ``hg ccom`` with a
  notebook that only has output changes used to fail early.)

__ https://selenic.com/pipermail/mercurial-devel/2011-December/036480.html

Releases
++++++++

To release a new version be sure to do the following. (The examples use revision
numbers etc. for release 0.1.11.)

1. Make sure your code works and that the tests pass.  Pull any open issues
	 into the main release branch, closing those issue branches.
2. Commit all your changes. (This is an optional commit, if the changes are
	 small, this can be rolled in with the following commit.)
3. Remove the ``'dev'`` from the version in ``setup.py`` (i.e.
	 ``'0.1.11dev' -> '0.1.11'``).
4. Add a note about the changes in ``CHANGES.txt``.
5. Commit the changes.  Start the commit message with::

	   hg com -m "REL: 0.1.11 ..."

6. Create a pull request (PR) on bitbucket to pull this branch to ``default`` and
	 make sure to specify to close the branch on pull.
7. Check, approve, and merge the PR.
8. Pull the merge from bitbucket to your development machine but **do not update**.
9. Update the version in ``setup.py`` to ``'0.1.12dev'`` or whatever is relevant.
10. From the previous commit (the last commit on branch ``0.1.11`` in this case),
	  change the branch::

	    hg branch 0.1.12
			
11. Commit and optionally push.  Now you are ready to work on new changes.



Notes
=====

Various notes about python, IPython, etc. are stored in the docs folder.



__ http://jupyter.cs.brynmawr.edu/hub/dblank/public/Jupyter%20Help.ipynb#2.-Installing-extensions
__ https://bitbucket.org/ipre/calico/downloads/
