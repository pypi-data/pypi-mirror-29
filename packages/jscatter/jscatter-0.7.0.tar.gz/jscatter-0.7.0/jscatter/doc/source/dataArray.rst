dataArray
=========

.. currentmodule:: jscatter.dataarray

.. include:: ../../dataarray.py
    :start-after: **dataArray**
    :end-before:  **dataList**


Attributes
----------
Array columns can be accessed as automatic generated attributes like .X,.Y,.eY (see protectedNames).

Corrsponding column indices are set by :py:meth:`dataArray.setColumnIndex` (default X,Y,eY = 0,1,2).

Attributes can be set like:  data.aName= 1.2345

.. autosummary::
        protectedNames

.. autosummary::

        dataArray.showattr
        dataArray.attr
        dataArray.getfromcomment
        dataArray.extract_comm
        dataArray.resumeAttrTxt
        dataArray.setattr
        dataArray.setColumnIndex
        dataArray.name
        dataArray.array
        dataArray.argmax
        dataArray.argmin

Fitting
-------
.. autosummary::

        dataArray.fit
        dataArray.modelValues
        dataArray.setlimit
        dataArray.has_limit
        dataArray.makeErrPlot
        dataArray.makeNewErrPlot
        dataArray.killErrPlot
        dataArray.detachErrPlot
        dataArray.showlastErrPlot
        dataArray.savelastErrPlot

Housekeeping
------------
.. autosummary::

        dataArray.savetxt
        dataArray.isort
        dataArray.where
        dataArray.prune
        dataArray.merge
        dataArray.concatenate
        dataArray.interpolate
        dataArray.interpAll
        dataArray.interp
        dataArray.polyfit
        dataArray.addZeroColumns
        dataArray.addColumn

Convenience
-----------
.. autosummary::
    
        zeros
        ones
        fromFunction

-----

.. autodata:: jscatter.dataarray.protectedNames

.. autoclass:: jscatter.dataarray.dataArray
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

.. automethod:: jscatter.dataarray.zeros
.. automethod:: jscatter.dataarray.ones
.. automethod:: jscatter.dataarray.fromFunction

