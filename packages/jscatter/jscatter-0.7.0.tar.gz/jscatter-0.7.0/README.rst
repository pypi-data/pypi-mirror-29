**The aim of jscatter is handling of experimental data and models**:



* Reading and analyzing experimental data with associated attributes as temperature, wavevector, comment, ....
* Multidimensional fitting taking the attributes (as fixed parameters) into account.
* Providing useful models (mainly for neutron and xray scattering), but there is no limitation.
* Plotting with paper ready quality (preferred in xmgrace, matplotlib possible ).
* Easy model building for non programmers.
* Python scripts to document data evaluation and used modelling.

`<http://jscatter.readthedocs.io>`_

.. image:: http://jscatter.readthedocs.io/en/latest/_images/Jscatter.jpeg
   :width: 200px
   :align: left
   :alt: Jscatter Logo

**Main concept**

 Link data from experiment, analytical theory or simulation with attributes as .temperature, .wavevector, .pressure,....
 Methods for fitting, filter, merging,... using attributes by name.
 A extensible library with common theories for fitting or simulation.

**1  Data organisation**

 Multiple measurements are stored in a *dataList* (subclass of list) of *dataArray*.
 dataArray is a subclass of **numpy** ndarray but with attributes and more.
 Full numpy ndarray functionality is preserved.
 Special attributes are .X,.Y, .eY...- for convenience and easy reading.
 Thus dataList represents e.g. a temperature series (as dataList) with measurements (dataArray) as list elements.

**2  Read/Write data**

 The intention is to read everything in the file to use it later and not ignore it as in numpy.loadtxt.
 Multiple measurement files can be read at once and then filtered according to attributes to get subsets.
 An ASCII file may consist of multiple sets of data with optional attributes or comments.
 Data are a matrix of values in a file. Attribute lines have a name in front.
 Everything else is a comment.
 Thus the first two words (separated by whitespace or other) decide about assignment of a line:

 * string + value     -> **attribute** with attribute name + list of values
 * value  + value     -> **data line** as sequence of numbers
 * string + string    -> **comment**
 * single words       -> **comment**
 * string+\@unique_name-> **link** to other dataArray with a unique_name

 Even complex ASCII files can be read with a few changes given as options.
 The ASCII file is still human readable and can be edited.
 Attributes can be generated from content of the comments (attributes which are text and not numbers).

**3  Fitting**

 Multidimensional attribute dependent fitting
 (least square Levenberg-Marquardt, differential evolution, .... from scipy.optimize).
 Attributes are used automatically as fixed fit parameters but can be overwritten.
 See dataList.fit for detailed description.

**4  Plotting**

 We use an adaption of xmgrace for 2D plots (a wrapper; see GracePlot) as it allows
 interactive publication ready output in high quality for 2D plots.
 The plot is stored as ASCII (.agr file) with original data and not as non-editable image as png or jpg.
 This allows a later change of the plot layout without recalculation, because data are stored as data and not as image.
 Imagine the boss/reviewer asking for a change of colors/symbol size.
 Nevertheless a small `matplotlib <https://matplotlib.org/>`_ interface is there and matplotlib can be used as it is (e.g. for 3D plots).

**5  Models**

 A set of models/theories is included see module e.g. formel, form factor and structure factor.
 User defined models can be used (e.g. as lambda function) just within a script or in interactive session of (i)python.
 By intention the user should write own models (to include e.g. a background, instrument resolution, ...) or to add different contributions.
 Contribution by new models is welcome. Please give a publication as reference as in the provided models.


 **some special functions**::

  formel.scatteringLengthDensityCalc -> electron density, coh and inc neutron scattering length, mass
  formel.sedimentationProfile        -> approximate solution to the Lamm equation of sedimenting particles
  formel.waterdensity                -> temperature dependent density of water (H2O/D2O) with inorganic subtstances
  structurefactor.RMSA               -> rescaled MSA structure factor for dilute charged colloidal dispersions
  structurefactor.hydrodynamicFunct  -> hydrodynamic function from hydrodynamic pair interaction
  formfactor.multiShellSphere        -> formfactor of multi shell spherical particles
  formfactor.multiShellCylinder      -> formfactor of multi shell cylinder particles
  formfactor.orientedCloudScattering -> 2D scattering of an oriented cloud of scatterers
  dynamic.finiteZimm                 -> Zimm model with internal friction -> intermediate scattering function
  dynamic.diffusionHarmonicPotential -> diffusion in harmonic potential-> intermediate scattering function
  sas.smear                          -> smearing for SANS (Pedersen), SAXS (line collimation) or by explicit Gaussian
  sas.desmear                        -> desmearing according to the Lake algorithm for the above
  sas.waterXrayScattering            -> Absolute scattering of water with components (salt, buffer)

**6  Examples & Documentation**

 A number of examples how to use jscatter is provided and can be run from jscatter.
 Documantation located at `<http://jscatter.readthedocs.io>`_.
 The html documentation can be opened in browser (for dev versions) ::

  import jscatter as js
  js.showDoc()                     # open html documentation
  js.examples.showExampleList()    # show list of examples
  js.examples.runExample(1)        # run example by number of filename
  js.examples.showExample(1)       # show example source code


 A short example how to use jscatter::


    import jscatter as js

    i5=js.dL(js.examples.datapath+'/iqt_1hho.dat')     # read the data (16 sets) with attributes
    # define a model for the fit
    diffusion=lambda A,D,t,wavevector,elastic=0:A*np.exp(-wavevector**2*D*t)+elastic

    # do the fit
    i5.fit(model=diffusion,                     # the fit function
           freepar={'D':[0.08],'A':0.98},       # start parameters, "[]" -> independent fit
           fixpar={'elastic':0.0},              # fixed parameters
           mapNames={'t':'X','wavevector':'q'}) # map names from the model to names from the data

    p=js.grace(1.2,0.8)                         # open a plot
    p.plot(i5,symbol=[-1,0.4,-1],legend='Q=$q') # plot with Q values in legend
    p.plot(i5.lastfit,symbol=0,line=[1,1,-1])   # plot fit as lines
    p.save('test.agr')



** Released under the GPLv3 **

