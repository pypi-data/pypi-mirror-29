## Python implementation of generateIPFColor
This repo contains a python implementation of the function [generateIPFColor](https://github.com/BlueQuartzSoftware/DREAM3D/blob/develop/Source/OrientationLib/LaueOps/HexagonalOps.cpp) from DREAM3D by BlueQuartzSoftware.
This is not a wrapper for the original code; it is written in pure python.

### Requirements
* Python 3 (Get it [here](https://www.python.org/downloads/) or create virtual environment in Anaconda using `conda create -n py36 python=3.6 anaconda`)
* Numpy `$ pip install numpy`

### Running the code
Make sure that the ipfcolor directory is in the same location as the script from which you are calling the function.
Unfortunately, due to python's lack of method overloading, the function signature has been altered slightly from the original implementation.
Be wary of the order of the input arguments, since the default ones need to come last.

```
from ipfcolor import Generator

generator = Generator()

rgb = generator.generate_ipf_color(
      phi1:       Union[float, list], # either a list of euler angles, or the first euler angle
      ref_dir_0:  Union[float, list], # either a list of ref_dir, or the first ref_dir
      deg_to_rad: bool,               # true if the euler angles are given in degrees, false if radians
      phi:        float,              # not required if phi1 is a list
      phi2:       float,              # not required if phi1 is a list
      ref_dir_1:  float,              # not required if ref_dir_0 is a list
      ref_dir_2:  float)              # not required if ref_dir_0 is a list
```

To avoid confusion, you might just want to use named parameters

```
rgb = generator.generate_ipf_color(
      phi1 = ...
      phi = ...
      phi2 = ...
      ref_dir_0 = ...
      ref_dir_1 = ...
      ref_dir_2 = ...
      deg_to_rad = ...)
```

Run the tests using `python3 -m pytest`
