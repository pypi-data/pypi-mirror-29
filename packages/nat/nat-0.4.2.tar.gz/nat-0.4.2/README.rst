`Getting Started <#getting-started>`__ \| `Releases <#releases>`__ \|
`Status <#status>`__

NeuroAnnotation Toolbox (NAT)
=============================

Python module to use the annotations created with
`NeuroCurator <https://github.com/BlueBrain/neurocurator>`__, for
example in a `Jupyter <https://jupyter.org/>`__ notebook.

This framework has been described in details in the following
open-access paper: https://doi.org/10.3389/fninf.2017.00027.

NAT provides the necessary functions and utilities to: - reliably
annotate the neuroscientific literature, - curate published values for
modeling parameters, - save them in reusable corpora.

--------------

Getting Started
---------------

**Requirements:**

System side:

-  `Git 1.7.0+ <https://git-scm.com/downloads>`__
-  `ImageMagick
   6 <http://docs.wand-py.org/en/latest/guide/install.html>`__

Python side:

-  `Beautiful Soup 4 <https://www.crummy.com/software/BeautifulSoup/>`__
-  `GitPython <https://gitpython.readthedocs.io>`__
-  `lxml <http://lxml.de>`__
-  `NumPy <http://www.numpy.org>`__
-  `pandas <https://pandas.pydata.org>`__
-  `parse <https://pypi.python.org/pypi/parse>`__
-  `Pyzotero <https://pyzotero.readthedocs.io>`__
-  `quantities <https://python-quantities.readthedocs.io>`__
-  `SciPy <https://www.scipy.org/scipylib/index.html>`__
-  `Wand <http://docs.wand-py.org>`__

**Installation:**

.. code:: bash

    pip install nat

Releases
--------

Versions and their notable changes are listed in the `releases
section <https://github.com/BlueBrain/nat/releases/>`__.

Releases are synchronized with the ones of NeuroCurator.

Status
------

Created during 2016.

Ongoing stabilization and reengineering in the branch
*refactor-architecture*.

The branch *refactor-architecture* is **not** intended to be used by
end-users.

New features, bug fixes and improvements are done on the reengineered
code sections.

When a reengineered code section is stable, it’s merged into the branch
*master* and a release is published.
