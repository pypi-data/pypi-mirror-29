[![pipeline status](https://gitlab.gwdg.de/kevin.luedemann/curve_shortening_flow/badges/master/pipeline.svg)](https://gitlab.gwdg.de/kevin.luedemann/curve_shortening_flow/commits/master)
Curve shortening flow
=====================

This project is a preparation for calculating minimal surfaces.
The simplest case of a surface is a curve in 2D, which has no constraints.
It therefore is iterated until it collapses to a circle and converges to zero length.
The API developed is able to perform this type of iteration of any closed curve.
The use is well documented and can compiled locally or viewed [online](https://kevin.luedemann.pages.gwdg.de/curve_shortening_flow/).
Some demos are available in the demo folder in the root directory and are explained in the documentation.

Dependencies
------------

The API depends on a few packages

	numpy,
	matplotlib,
	scipy

and for the documentation on

	sphinx and 
	numpydocs. 

These dependencies are by default taken care of by pip.


Installation instructions
-------------------------

In order to install the package **pip** is required.
The usual installing is done locally

	pip install -e .

or for users without root rights

	pip install --user -e .

The option *-e* is used for a link into the API of the root directory.
By this procedure an update of the API by pulling the Repo will be automatically included.

Plotting information
--------------------

The plotting and animating features have only been tested for the backends

	qt5agg

and

	qt4agg

other backends may be working as well but have not been tested, so far.


Compiling the documentation
---------------------------

The documentation is build by sphinx to compile it the API must be installed and the command

	make html

for example executed in the *doc* directory.
Other types are supported as well like *latex*, *epup*, *man* and many more.
To see which formats are possible use

	make help.
