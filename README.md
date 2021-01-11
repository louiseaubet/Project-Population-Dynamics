# Project on Population Dynamics


### Description

This project's aim is to model the evolution of world population through the McKendrick-von Foester equation. More particularly, the age structure of the population and its evolution over time is studied.


### Getting Started

This version was designed for python 3.6.6 or higher. To run the model's calculation, it is only needed to execute the file `run.py`. On the terminal, the command is `python run.py`. The code should return some figures that illustrate the evolution of the population repartition, in the folder `outputs`.


### Prerequisites

#### Libraries
The following librairies are used:
* [numpy](http://www.numpy.org/) 1.14.3, can be obtained through [anaconda](https://www.anaconda.com/download/)
* [pandas](https://pandas.pydata.org/), also available through anaconda
* [scipy](https://www.scipy.org/): `python -m pip install --user scipy`


#### Code

To launch the code `run.py` in the folder `Numerical_model` use the following codes and pickle files:
* `main.py` : Contains the main part of the code, call the functions and run the model
* `helpers.py` : Deal with loading of `.csv` files and interpolation functions
* `scheme.py` : Contains the definition of the class Scheme
* `fluxes/births.py` : Contains the definition of the class Births
* `fluxes/deaths.py`: Contains the definition of the class Deaths
* `fluxes/population.py`: Contains the definition of the class Population
* `fluxes/totalpop.py`: Contains the definition of the class Totalpop

The `data` folder is also needed to store the data from the UN database. The following CSV files are used : `fertility_indicators.csv`, `life_table.csv`, `period_indicators.csv`, `population_by_age.csv`, `total_population.csv`. The list of all indicators contained in these files and their definition can be found [here](https://population.un.org/wpp/Download/Standard/Population/).


### Additional content

The folder `Numerical_model/fluxes` contains python code that defines the classes used by the numerical model. Those files are run into the main code, which is `run.py`.

The folder `Data_analysis` contains some Python Notebooks that allow to better visualize the fluxes : `ASFR.ipynb`, `Death.ipynb`, `Population.ipynb` and `TFR.ipynb`. Also, `NetMigration.ipynb` and `Population_MW.ipynb` allow to check if the hypothesis of the model are verified. 

The file `Convergence_analysis.ipynb` contains a code that test the convergence of the numerical scheme on an analytical solution. The file `Schem_RK2.ipynb` contains the implementation of the alternative model. It is not successul in the sense that the results are not realistic.

The file `report.pdf` contains further informations on the mathematical definition of the model, the numerical implementation as well as the analysis of the results.


### Documentation

* [Ressources](https://population.un.org/wpp/Download/Standard/Population/) : UN database, Department of Economics and Social Affairs


### Authors

Aubet Louise, louise.aubet@epfl.ch


### Project Status

The project was submitted on the 1st of June 2020, as a semester project.
