# BENMO|Simulation Model

**BENMO|Simulation: A computationally efficient and biologically enhanced model for nutrient dynamics in coastal bays**

*Authors:* Zhehan Huang, Shaobin Li, Wenyan Tang, Pan Yang, Nengwang Chen

_________________________________________________________________________________________________

## Introduction

This package provides a model to simulate the nutrient dynamics in coastal bays. The calculation module in the package can be divided into several parts:

* **[Automatic Zoning.py](/Automatic_Zoning.py) is to read the output data from Delft3D and divide the coastal bay into several zones.**

* **[BENMO_20.py](/BENMO_20.py) and [main_20.py](/main_20.py) are the main part of the simulation model which simulate the nutriwnt dynamics.** 

* **All the codes in [Analysis](/Analysis) are afterwards analysis of kthe model, including [Figure_Plot](/Analysis/figure_plot_d3d.py), [Sensitivity_Analysis](/Analysis/sensitivity_analysis_parallel.py), and [Contribuation_Analysis](/Analysis/Contribuation_Analysis.py).** 

## Acknowlegments

Shaobin Li and Zhehan Huang received the he financial support from the National Natural Science Foundation of China (42361144862), Environmental Protection Science and Technology Program Project of Fujian (2025R020), and State Key Laboratory of Hydraulics and Mountain River Engineering (SKHL2319).

## Contact

In case of any questions, please contact <a href="mailto:shaobinli@xmu.edu.cn">Shaobin Li</a> (shaobinli@xmu.edu.cn).
