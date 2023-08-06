# What is CoCo?

CoCo ("Complementary Coordinates") is a method for testing and potentially enriching the the variety of conformations within an ensemble of molecular structures. It was originally developed with NMR datasets in mind and the background and this application is described in:

[Laughton C.A., Orozco M. and Vranken W., COCO: A simple tool to enrich the representation of conformational variability in NMR structures, PROTEINS, 75, 206-216 (2009)](http://onlinelibrary.wiley.com/doi/10.1002/prot.22235/abstract)

CoCo, which is based on principal component analysis, analyses the distribution of an ensemble of structures in conformational space, and generates a new ensemble that fills gaps in the distribution. These new structures are not guaranteed to be valid members of the ensemble, but should be treated as possible, approximate, new solutions for refinement against the original data.
Though developed with protein NMR data in mind, the method is quite general – the initial structures do not have to come from NMR data, and can be of nucleic acids, carbohydrates, etc.

The outline of the CoCo method is as follows:

![COCO method2.gif](https://bitbucket.org/repo/bAGR4M/images/1692328909-COCO%20method2.gif)
Step 1: The input ensemble is subjected to Principal Component Analysis and the position of each structure in a low dimensional subspace identified.

Step 2: New points are placed to fill gaps in the distribution.

Step 3: The new points are converted back into new structures, which are returned to the user.


This package provides a python-based command line tool that implements the CoCo method, and also exemplifies its application within an ExTASY workflow that can be used in an iterative manner to rapidly expand the coverage of a MD-generated ensemble.

------

# Installation

## ... on Ubuntu Linux (Desktop)

The following packages need to be installed on the system (via `apt-get`) `python-dev, libblas-dev, liblapack-dev, gfortran, tcsh`, as well as `Amber`.

Having `numpy` and `scipy` is a prerequisite to the CoCo installation as well.

After making sure that the previously listed dependencies are installed, clone the CoCo repository and install:

```
git clone https://bitbucket.org/extasy-project/coco.git
cd coco
python setup.py install --user
```

## ... on XSEDE's Stampede Cluster

First, we need to load the appropriate modules:

```
module load amber
module load python/2.7.3-epd-7.3.2
```

Clone the CoCo repository and install:

```
rm -r $HOME/.local/*
git clone https://bitbucket.org/extasy-project/coco.git
cd coco
easy_install --user --upgrade .
chmod +x $HOME/.local/lib/python2.7/site-packages/radical.pilot-0.20-py2.7.egg/radical/pilot/bootstrapper/*.sh
```
Ensure the executables are in your PATH:
```
export PATH=$PATH:$HOME/.local/bin
```

## ... on ARCHER

First, we need to load the appropriate modules:

```
module load amber
module load numpy/1.8.0-libsci
module load scipy
```

Clone the CoCo repository and install (Must be on /work to run on the backend):

```
export WORK=/path/to/your/work/directory
rm -r $WORK/.local
git clone https://bitbucket.org/extasy-project/coco.git
cd coco
mkdir -p $WORK/.local/lib/python2.7/site-packages
export PYTHONPATH=$PYTHONPATH:$WORK/.local/lib/python2.7/site-packages
easy_install --prefix $WORK/.local --upgrade .
```

# Using the Command Line Tool "pyCoCo"

In the ./example subdirectory is a test script to run a simple CoCo analysis. Four short trajectory files (AMBER .ncdf format) and an associated topology file for penta-alanine (penta.top) are provided. The test script analyses the ensemble and generates eight new structures, in PDB format, that represent apparent gaps in the sampling of conformational space. To run the test example type:

```
./test.sh
```
When the job completes (about a minute), you should see eight new pdb files (coco0.pdb - coco7.pdb), and a log file (test.log).
The log file should look like this:
```
*** pyCoCo ***

Trajectory files to be analysed:
md0.dcd: 10 frames
md1.dcd: 10 frames
md2.dcd: 10 frames
md3.dcd: 10 frames

Total variance in trajectory data: 97.51

Conformational sampling map will be generated in
3 dimensions at a resolution of 30 points
in each dimension.

8 complementary structures will be generated.

Sampled volume: 11.4286389744 Ang.^3.

Coordinates of new structures in PC space:
   0 -12.37   9.31  -7.29
   1  15.03   6.45  -7.29
   2   1.81  -7.27   8.44
   3  15.03   9.31   5.19
   4  15.03  -7.27  -7.29
   5 -12.37   9.31   8.44
   6   2.75   9.31   8.44
   7 -12.37  -7.27  -7.29

RMSD matrix for new structures:
  0.00  2.63  3.46  3.24  3.38  1.99  3.15  2.19
  2.63  0.00  2.80  1.69  1.69  3.44  2.81  3.73
  3.46  2.80  0.00  2.60  2.43  2.76  2.49  2.77
  3.24  1.69  2.60  0.00  2.82  3.64  1.82  3.56
  3.38  1.69  2.43  2.82  0.00  3.45  3.60  3.62
  1.99  3.44  2.76  3.64  3.45  0.00  2.43  3.11
  3.15  2.81  2.49  1.82  3.60  2.43  0.00  3.70
  2.19  3.73  2.77  3.56  3.62  3.11  3.70  0.00

```

pyCoCo accepts most of the most widely-used trajectory and topology file formats (AMBER, CHARMM, GROMACS, NAMD, etc.). For a full guide to pyCoCo see [here](http://bitbucket.org/extasy-project/coco/wiki/Home).


# Running the Workflow Example
The examples/workflow directory illustrates how pyCoCo can be used as part of workflow to perform enhanced sampling. In this case, we begin by running eight independent short MD simulations on alanine pentapeptide. The combined trajectory data is fed into a CoCo analysis to identify poorly sampled regions and generate eight new starting structures that populate these. These structures are then used in a new cycle of eight MD simulations, the new trajectory data is combined with the old data for a second CoCo analysis, etc. In this case ten cycles of MD/CoCo are run.

**NOTE:** This workflow requires you to have AMBER (or AMBERTOOLS) installed on your machine and have the commands *tleap* and *sander* in your path.

(CoCo workflow diagram here)

## Sequentially / Locally 

Change into the examples directory:
```
cd examples/workflow
```

Then run the example:

```
python penta_coco.py
```

The output should look like this:

```
running md cycle 0
Running CoCo...
creating new crd files...
running md cycle 1
[...]
```
After the job has completed you will see that many files have been created. In the current directory 
you will see a series of files *coco_cycle\*.log*; these are the log files from each CoCo run. In the individual rep0?/ directories are the input and
output files from each cycle of MD. The growing ensemble of structures is thus the growing set of trajectory
files (\*.ncdf).

To see how the CoCo process has performed, you can type:
```
% grep Total coco_cycle*.log
coco_cycle1.log:Total variance in trajectory data: 91.16
coco_cycle2.log:Total variance in trajectory data: 129.50
coco_cycle3.log:Total variance in trajectory data: 178.80
coco_cycle4.log:Total variance in trajectory data: 219.20
coco_cycle5.log:Total variance in trajectory data: 241.58
coco_cycle6.log:Total variance in trajectory data: 256.77
coco_cycle7.log:Total variance in trajectory data: 267.05
coco_cycle8.log:Total variance in trajectory data: 280.75
coco_cycle9.log:Total variance in trajectory data: 291.82
```
Note that the exact numbers you see will be different from these, due to variability in the MD.

To see how CoCo improves the rate of sampling, you can run the script 'penta_nococo.py'.
This runs the same workflow, but at the end of each MD cycle, instead of generating new start points by CoCo, the next MD runs just start from the final points from the last cycle:

```
% python penta_nococo.py
running md cycle 0
creating new crd files...
running md cycle 1
creating new crd files...
running md cycle 2
[...]
```
If you then run that 'grep' command again you should get
something like:
```
% grep Total nococo_cycle*.log
nococo_cycle1.log:Total variance in trajectory data: 130.92
nococo_cycle2.log:Total variance in trajectory data: 131.31
nococo_cycle3.log:Total variance in trajectory data: 130.82
nococo_cycle4.log:Total variance in trajectory data: 134.61
nococo_cycle5.log:Total variance in trajectory data: 143.01
nococo_cycle6.log:Total variance in trajectory data: 144.25
nococo_cycle7.log:Total variance in trajectory data: 156.13
nococo_cycle8.log:Total variance in trajectory data: 168.07
nococo_cycle9.log:Total variance in trajectory data: 174.18
```

Illustrating how CoCo enhances the rate at which conformational space is sampled.


## Concurrently via RADICAL-Pilot on HPC clusters

For information on how to run the CoCo workflow in the context of the ExTASY tools using HPC resources such as ARCHER and STAMPEDE see [here](https://github.com/radical-cybertools/ExTASY/tree/devel#usage).


# Developing Coco

You can directly work with the source files in the `src/extasy/` directory. However, in order for the changes to take effect, you need to run the installer before you run your test / example code:

```
easy_install --upgrade .
```

For example, if you are in the examples directory and you want to see if your latest code changes to, let's say `src/extasy/coco.py` work, you can simply run:

```
easy_install --upgrade .. && python penta_coco.py