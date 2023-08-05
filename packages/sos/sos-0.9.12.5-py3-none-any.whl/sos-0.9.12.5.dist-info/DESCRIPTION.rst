Computationally intensive disciplines such as computational biology often 
requires one to exploit a variety of tools implemented in different programming
languages, and to analyze large datasets on high performance computing systems.
Although scientific workflow systems are powerful in organizing and executing
large-scale data analysis processes, there are usually non-trivial learning
curve and engineering overhead in creating and maintaining such workflows,
making them unsuitable for data exploration and prototyping. To bridge the
gap between interactive analysis and workflow systems, we developed Script
of Scripts (SoS), a system with strong emphases on readability, practicality,
and reproducibility for daily computational research. For exploratory analysis
SoS provides a multi-language file format and scripting engine that centralizes
all computations, and creates dynamic report documents for publishing and
sharing. As a workflow engine, SoS provides an intuitive syntax to create
workflows in process-oriented, outcome-oriented and mixed styles, as well as
a unified interface to executing and managing tasks on a variety of computing
platforms with automatic synchronization of files between isolated systems.
In this paper we illustrate with real-world examples the use of SoS as both
interactive analysis tool and pipeline platform for all stages of methods
development and data analysis projects. In particular we demonstrate how SoS
can easily be adopted based on existing scripts and pipelines, yet resulting
in substantial improvement in terms of organization, readability and
cross-platform computation management.

Please refer to http://vatlab.github.io/SOS/ for more details on SoS.


