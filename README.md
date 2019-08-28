# VisibleHuman3D

This project is part of a master thesis aims at creating a 3D model from the CT slices of the Visible Human Project
in such a way that free navigation in medical Virtual Reality - with proper collision detection against
the organs.

## Getting Started

The project is divided in two main categories, the firs one is the generation of the 3D model and the second one is the generation of the simulation. The former is implemented by using Python and the later by using C#.

### Python Dependencies 

The project has the following required dependencies:

* [Python](https://www.python.org/) v3.x.
* [NumPy](http://www.numpy.org/) v1.8 or higher
* [SciPy](http://www.scipy.org/) v0.13 or higher
* [pydicom](https://pydicom.github.io/)
* [skimage](https://scikit-image.org/)
* [sklearn](https://scikit-learn.org/stable/)
* [mcubes](https://github.com/pmneila/PyMCubes)
* [collada](https://github.com/pycollada/pycollada)
* [Blender](https://www.blender.org/) Python module (bpy)


#### Installing

The easiest way to install Python on Windows is to use [Anaconda](https://docs.anaconda.com/anaconda/install/windows/).
Then most of the above dependencies can be install via the line : 

```
conda install dependency_package_name
```
or by installing [pip](https://pip.pypa.io/en/stable/installing/) and then using the line : 
```
pip install dependency_package_name
```
A step by step installation of Blender Python module can be found [here](https://blog.machinimatrix.org/building-blender/) and [here](https://cobertos.com/2017/07/19/compiling-blender-as-a-python-module-for-windows-10-x64/). 
For the other the installation steps are describe in their github project site.


### C# Dependencies

* [Bullet](https://pybullet.org/wordpress)

## Authors

* **François ADAM** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

