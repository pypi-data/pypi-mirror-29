# Auron

Auron uses the Yuna package to generate a graph network from the layer polygons
of a superconducting circuit as given by Yuna.

## Depenencies

On Fedora install the following:

```
sudo dnf install redhat-rpm-config
sudo dnf install gcc-c++
sudo dnf install python2-devel
sudo dnf install tkinter
sudo dnf install gmsh
```

Install the package manager

```
sudo apt-get install python-pip
sudo apt-get install python3-pip
```

Make sure TKinter is installed

```
sudo apt-get install python-tk
sudo apt-get install python3-tk
```

Install GMSH on your system

```
sudo apt-get install gmsh
sudo apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran
```

## Installation

You can install Auron directly from the Python package manager *pip* using:

```
sudo pip install auron
```

To instead install Auron from source, clone this repository, *cd* into it, and run:

```
sudo pip install -r requirements.txt
sudo pip install .
sudo pip install -e .
```

## Process Details

These are the process layer assumptions made on 14 Jan 2017.

### BBN

* 40 - Nb via stud lift-off deposition
* 42 - Nb base electrode patterning
* 44 - Nb counter electrode and dielectric etch
* 45 - NbNx wiring patterning
* 50 - Nanopillar milling
* 51 - NbNx nTron patterning

## Rules

1. Watch out for device-to-wire connection discontinuities.
2. A device, like ntrons or jjs, must be included as a cell if it is
connectd to ground. And as a different cell if it is not connected to ground.
3. All ground cells must end with `_gnd`.
4. Each cell must be centered around (0, 0).
5. Wires connected to non-ground devices must be laid to connect to edges perfectly.

## Colors

TERM - Dark Blue
TEXT - Black
USER - Light Blue
LAYER - Green
GROUND - Dark Grey
VIA - Grey
JJ - Purple
NTRON - Red

42 - Light Orange
45 - Light Pink

Great read for package/module distrobution: http://amir.rachum.com/blog/2017/07/28/python-entry-points/

## Developers

Uploading package to PyPi using *twine*:

```
sudo python setup.py bdist_wheel
twine upload dist/*
```


