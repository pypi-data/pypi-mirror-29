**The aim of jscatter is handling of experimental data and models**:

.. image:: ../../examples/Jscatter.jpeg
    :width: 200px
    :align: right
    :height: 200px
    :alt: Jscatter Logo

* Reading and analyzing experimental data with associated attributes as temperature, wavevector, comment, ....
* Multidimensional fitting taking the attributes (as fixed parameters) into account.
* Providing useful models (mainly for neutron and xray scattering), but there is no limitation.
* Simplified plotting with paper ready quality (preferred in xmgrace).
* Easy model building for non programmers.
* Python scripts to document data evaluation and modelling.

**Main concept**

| Link data from experiment, analytical theory or simulation with attributes as .temperature, .wavevector, .pressure,....
| Methods for fitting, filter, merging,... using attributes by name.
| An extensible library with common theories for fitting.

1. **Data organisation**

| Multiple measurements are stored in a :py:class:`~.dataList` (subclass of list) containing :py:class:`~.dataArray` ´s.
| dataArray is a subclass of **numpy** ndarray but with attributes and more.
| Full numpy ndarray functionality is preserved.
| Special attributes are .X,.Y,.eY...- for convenience and easy reading.
| Thus dataList represents e.g. a temperature series (as dataList) with measurements (dataArray) as list elements.

2. **Read/Write data**

| The intention is to read everything in the file to use it later and not ignore it as in numpy.loadtxt.
| Multiple measurement files can be read at once and then filtered according to attributes to get subsets.
| An ASCII file may consist of multiple sets of data with optional attributes or comments.
| Data are a matrix of values in a file. Attribute lines have a name in front.
| Everything else is a comment.
| Thus the first two words (separated by whitespace) decide about assignment of a line:
| 
| - string + value     -> **attribute** with attribute name + list of values
| - value  + value     -> **data line** as sequence of numbers 
| - string + string    -> **comment** 
| - single words       -> **comment**
| - string+\@unique_name-> **link** to other dataArray with a unique_name
|
| Even complex ASCII files can be read with a few changes given as options.
| The ASCII file is still human readable and can be edited.
| Attributes can be generated from content of the comments (attributes which are text and not numbers).

3. **Fitting**

| Multidimensional attribute dependent fitting (least square Levenberg-Marquardt, differential evolution, ...from scipy.optimize).
| Attributes are used automatically as fixed fit parameters.
| See :py:meth:`~.dataarray.dataList.fit` for detailed description.
| Simulation with changed parameters (e.g. to observe change within error limits).

4. **Plotting**

| We use an adaption of xmgrace for 2D plots (a wrapper; see :ref:`GracePlot`) as it allows
| interactive publication ready output in high quality for 2D plots.
| The plot is stored as ASCII (.agr file) with original data and not as non-editable image as png or jpg.
| This allows a later change of the plot layout without recalculation, because data are stored as data and not as image.
| Imagine the boss/reviewer asking for a change of colors/symbol size.
| Nevertheless a small `matplotlib <https://matplotlib.org/>`_ interface is there and matplotlib can be used as it is (e.g. for 3D plots).

5. **Models**

| A set of models/theories is included see module e.g. :ref:`formel`, :ref:`formfactor (ff)` and :ref:`structurefactor (sf)`.
| User defined models can be used (e.g. as lambda function) just within a script or in interactive session of (I)python.
| By intention the user should write own models (to include e.g. a background, instrument resolution, ...) or to add different contributions.
| Contribution by new models is welcome (but not trivial ones). Please give a publication as reference as in the provided models.


 **some special functions**:

 | :py:func:`~.formel.scatteringLengthDensityCalc` -> electron density, coh and inc neutron scattering length, mass
 | :py:func:`~.formel.waterdensity` -> temperature dependent density of water (H2O/D2O) with inorganic subtstances
 | :py:func:`~.formel.sedimentationProfile` -> approximate solution to the Lamm equation of sedimenting particles
 | :py:func:`~.structurefactor.RMSA` -> rescaled MSA structure factor for dilute charged colloidal dispersions
 | :py:func:`~.structurefactor.hydrodynamicFunct` -> hydrodynamic function from hydrodynamic pair interaction
 | :py:func:`~.formfactor.multiShellSphere` -> formfactor of multi shell spherical particles
 | :py:func:`~.formfactor.multiShellCylinder` -> formfactor of multi shell cylinder particles with caps
 | :py:func:`~.formfactor.orientedCloudScattering` -> 2D scattering of an oriented cloud of scatterers
 | :py:func:`~.dynamic.finiteZimm` -> Zimm model with internal friction -> intermediate scattering function
 | :py:func:`~.dynamic.diffusionHarmonicPotential` -> diffusion in harmonic potential-> intermediate scattering function
 | :py:func:`~.smallanglescattering.smear` -> smearing for SANS (Pedersen), SAXS (line collimation) or by explicit Gaussian
 | :py:func:`~.smallanglescattering.desmear` -> desmearing according to the Lake algorithm for the above
 | :py:func:`~.smallanglescattering.waterXrayScattering` -> Absolute scattering of water with components (salt, buffer)

**Example** see example_simple_diffusion.py and other :ref:`label_Examples`


.. literalinclude:: ../../examples/example_simple_diffusion.py
    :language: python
    :lines: 3-39
.. image:: ../../examples/DiffusionFit.jpg
    :align: center
    :height: 300px
    :alt: Picture about diffusion fit


**Shortcuts**::

    import jscatter as js
    js.showDoc()                  # Show html documentation in browser
    exampledA=js.dA('test.dat')   # shortcut to create dataArray from file
    exampledL=js.dL('test.dat')   # shortcut to create dataList from file
    p=js.grace()                  # create plot
    p.plot(exampledL)             # plot the read dataList

----------------

| if not otherwise stated in the files:
|
| written by Ralf Biehl at the Forschungszentrum Jülich ,
| Jülich Center for Neutron Science 1 and Institute of Complex Systems 1
|    jscatter is a program to read, analyse and plot data
|    Copyright (C) 2015  Ralf Biehl
|
|    This program is free software: you can redistribute it and/or modify
|    it under the terms of the GNU General Public License as published by
|    the Free Software Foundation, either version 3 of the License, or
|    (at your option) any later version.
|
|    This program is distributed in the hope that it will be useful,
|    but WITHOUT ANY WARRANTY; without even the implied warranty of
|    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
|    GNU General Public License for more details.
|
|    You should have received a copy of the GNU General Public License
|    along with this program.  If not, see <http://www.gnu.org/licenses/>.


**Intention and Remarks**

**Genesis**

This package was programmed because of my personal need to fit multiple datasets together which differ
in attributes defined by the measurements. A very common thing that is not included in numpy/scipy or
most other fit programs. What i wanted is a numpy ndarray with its matrix like functionality
for evaluating my data, but including attributes related to the data e.g. from a measurement.
For multiple measurements i need a list of these. ==> dataArray and dataList.

As the used models are repeatedly the same a module with physical models was growing.
A lot of these models are used frequently in small angle scattering programs like SASview or SASfit.
For my purpose the dynamic models as diffusion, ZIMM, ROUSE and other things like protein dynamics were missing.

Some programs (under open license) are difficult to extend as the models are hidden in classes,
or the access/reusage includes a special designed interface to get parameters instead of simple function calls.
Here simple Python functions are easier to use for the non-programmers as most PhD-students are.
Models are just python functions (or one line lambda functions) with the arguments accessed by their name (keword arguments).
Scripting in Python with numpy/scipy is easy to learn even without extended programming skills.


**Scripting over GUI**

Documentation of the evaluation of scientific data is difficult in GUI based programs
(sequence of clicking buttons ???). Script oriented evaluation (MATLAB, Python, Jupyter,....)
allow easy repetition with stepwise improvement and at the same time document what was done.

Complex models have multiple contributions, background contribution, ... which can easily be defined in
a short script including a documentation.
I cannot guess if the background in a measurement is const linear, parabolic or whatever and
each choice is also a limitation.
Therefore the intention is to supply not obvious and complex models (with a scientific reference)
and allow the user to adopt them to their needs e.g. add background and amplitude or resolution convolution.
Simple models are fast implemented in one line as lambda functions or more complex things in scripts.
The mathematical basis as integration or linear algebra can be used from scipy/numpy.

**Plotting**

`Matplotlib <https://matplotlib.org/>`_ seems to be the standard for numpy/scipy users. You can use it if you want.
If you try to plot fast and live (interactive) it is complicated and slow (in my opinion).
Another good plotting tool is `gr <http://gr-framework.org/>`_.

Frequently i run scripts that show results of different datasets and i want to keep these
for comparison open and be able to modify the plot. Some of this is possible in matplotlib but not the default.
As i want to think about physics and not plotting i like more xmgrace, with a GUI interface
after plotting. A simple one line command should result in a 90% finished plot,
final 10% fine adjustment can be done in the GUI if needed or from additional commands.
I adopted the original Graceplot module (python interface to XmGrace) to my needs and added
dataArray functionality. For the errorPlot of a fit a simple matplotlib interface is included.

The nice thing about Xmgrace is that it stores the plot as ASCII text instead of the JPG or PDF.
So its easy to reopen the plot and change the plot later if your supervisor/boss/reviewer asks
for log-log or other colors or whatever. For data inspection zoom, hide of data, simple fitting
for trends and else are possible on WYSIWYG/GUI basis.
If you want to retrieve the data (or forgot to save your results separatly) they are accessible
in the ASCII file. Export in scientific paper quality is possible.
A simple interface for annotations, lines, .... is included.
Unfortunately its only 2D but this is 99% of my work.

**Speed/Libraries**

The most common libraries for scientific computing in python are NUMPY and SCIPY and these are the
only obligatory dependencies for jscatter. Python in combination with numpy can be quite fast if the
ndarrays methods are used consequently instead of explicit for loops. E.g. the numpy.einsum function immediately
uses compiled C to do the computation. (`See this <http://ipython-books.github.io/featured-01/>`_
and look for "Why are NumPy arrays efficient"). SCIPY offers all the math needed and optimized
algorithms, also from blas/lapack. To speed up if needed on a multiprocessor machine the
module :ref:`parallel` offers an easy interface to the standard python module *multiprocessing*
within a single command. If your model needs long computing time and needs speed up the common
methods as Cython, Numba or f2py should be used in your model.
As these are more difficult the advanced user may use it in their models.
A nice blog about possible speedups is found at
`Julia vs Python <https://www.ibm.com/developerworks/community/blogs/jfp/entry/Python_Meets_Julia_Micro_Performance?lang=en>`_.
Nevertheless the critical point in these cases is the model and not the small overhead in
dataArray/dataList or fitting.

As some models depend on f2py and fortran code an example is provided how to use f2py and finally contribute
a function in jscatter. :ref:`Extending/Contributing/Fortran`

Some resources :

 - `python-as-glue <https://docs.scipy.org/doc/numpy-1.10.1/user/c-info.python-as-glue.html>`_
 - `Julia vs Python <https://www.ibm.com/developerworks/community/blogs/jfp/entry/Python_Meets_Julia_Micro_Performance?lang=en>`_
 - `Getting the Best Performance out of NumPy <http://ipython-books.github.io/featured-01/>`_

**Development environment/ Testing**

The development platform is mainly current Linux (Linux Mint/CentOs).
I regularly use jscatter on macOS. I regularly use it on 12 core Linux machines on our cluster.
I tested the main functionallity (e.g. all examples) on Python 3.5 and try to write 2.7/3.5 compatible code.
I never use Windows (only if a manufacturer of an instrument forces me...)
Basically everything should work under Windows, except things that rely on pipes as the
connection to XmGrace and the DLS module which calls CONTIN through a pipe.


