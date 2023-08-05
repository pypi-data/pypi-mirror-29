Collider -- a software experimenting toolbox

Purpose
=======

Collider is a framework that makes software experimenting less stressful, easier to define and generally simpler to perform.

Rationale
=========

Suppose you are performing experiments in silico (say, performance tests but not only) with a range of variable parameters and a specific workflow that includes generating test cases, running an analysis binary and tracking the time spent on analysis depending on the instance. Usually, this kind of problem is solved by writing a script that loops over the parameter ranges and does the aforementioned task. This solution has several more or less obvious downsides:

- Code duplication by copying and pasting, even in for-loops
- Boilerplate code that tracks progress and saves intermediate results
- Restricted restart and progress tracking capabilities
- Limited many-core usage

After having written a bunch of such scripts (and being over-the-top frustrated with Matlab and shell scripts, copying/pasting of code snippets, rerunnning hour-long experiments/simulations), I have decided to construct a fully general solution.

Usage
=====

collider can be used as an executable or as a library. The executable requires a _config file_ which defines the stages of the experiment and the parameter space. Each stage defines an executable that is called and the call format in Python _format_ convention. The results of each stage are saved into files and, additionally, saved in a machine-readable form.

As a library, collider allows for more flexibility with respect to the definition of experiment stages. That is, one can define custom Python code which will be run as a stage of the experiment. The rationale behind this is to provide maximal flexibility with the library, and coverage of the most common use caes with the executable.

The different parameters of the executable can be seen by executing

`$ collider --help`

The documentation of the configuration file format and the library is work in progress.