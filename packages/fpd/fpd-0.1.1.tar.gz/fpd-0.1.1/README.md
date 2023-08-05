 
FPD package
===========

The fpd package provides code for the storage, analysis and visualisation
of data from fast pixelated detectors. The data storage uses the hdf5 based 
EMD file format, and the conversion currently supports the Merlin readout from 
Medipix3 detectors. Differential phase contrast imaging and several other common
data analyses, like radial distributions and virtual apertures, are also 
implemented, along with many utilities.

The package is relatively lightweight, with most of its few dependences being
standard scientific libraries. A degree of optimisation through parallelisation has
been implemented (the development environment is Linux; your mileage may vary on 
Windows). All calculations run on CPUs and many use out-of-core processing, 
allowing data to be visualised and processed on anything from very modest to
powerful hardware.


Installation
------------

The package currently supports both python versions 2.7 and 3.x. Hyperspy is
used in a few places but most of the fpd module can be used without it being 
installed (simply install the package dependences manually and ignore them when
using pip by adding ``--no-deps`` to the install command).

Installation from source:

```bash
pip3 install --user .
```

Instalation from PyPI:

```bash
pip3 install --user fpd
```

``-U`` can be added to force an upgrade / reinstall; in combination with ``--no-deps``,
only the ``fpd`` package will be reinstalled.

The package can be removed with:

```bash
pip3 uninstall fpd
```


Usage
-----
In python or ipython:

```python
import fpd
d = fpd.DPC_Explorer(-64)
```

```python
import fpd.fpd_processing as fpdp
rtn = fpdp.phase_correlation(data, 32, 32)
```
where `data` is any array-like object. For example, this can be an in-memory 
numpy array, an hdf5 object on disk, or a dask array, such as that used in 
'lazy' hyperspy signals.

All functions and classes are documented and can be read, for example, in `ipython`
by appending a `?` to the object. E.g.:

```python
import fpd
fpd.DPC_Explorer?
```

Documentation
-------------
Release: https://gwpaterson.gitlab.io/fpd/

Development version: https://gitlab.com/gwpaterson/fpd/builds/artifacts/master/file/pages_development/index.html?job=pages_development

Further documentation, notebooks and examples will be made available over time.


Related projects
----------------

https://www.gla.ac.uk/schools/physics/research/groups/mcmp/researchareas/pixstem/

http://quantumdetectors.com/stem/

https://gitlab.com/fast_pixelated_detectors/merlin_interface

https://gitlab.com/fast_pixelated_detectors/fpd_live_imaging

https://emdatasets.com/format

http://hyperspy.org/

http://gwyddion.net/

More packages will be added to the https://gitlab.com/fast_pixelated_detectors
group as they develop.

