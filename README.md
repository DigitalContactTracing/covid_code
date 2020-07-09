# Digital Proximity Tracing in the COVID-19 Pandemic on Empirical Contact Networks
This repository contains the code for the simulations and experiments in the paper

>  G. Cencetti, G. Santin, A. Longa, E. Pigani, A. Barrat, C. Cattuto, S. Lehmann,  M. Salathe, B. Lepri,
_Digital Proximity Tracing in the COVID-19 Pandemic on Empirical Contact Network_, [DOI: 10.1101/2020.05.29.20115915](https://doi.org/10.1101/2020.05.29.20115915).

## Basic usage:
For a basic usage of this code, you may consider the following steps.

First, the simulations on the network can be launched using the notebooks:
* [Digital-Contact-Tracing on DTU](Digital-Contact-Tracing%20on%20DTU.ipynb) to run the simulation on the DTU dataset<sup>[1](#dtu_footnote)</sup>.
* [Digital-Contact-Tracing on SocioPattern](Digital-Contact-Tracing%20on%20SocioPattern.ipynb) to run the simulation on some Sociopattern datasets<sup>[2](#socio_dataset)</sup>.

Second, the simulation of the continuous model can be launched using the notebook:
* [Generate_model_predictions.ipynb](Generate_model_predictions.ipynb).

These notebooks compute outputs that are stored in [RESULTS](RESULTS) and [RESULTS_Model](RESULTS_Model). As an example, these folders already contain the outputs for the case `R_0=1.5` with `app_adoption=80%`.


Finally, the outputs of the simulations may be visualized using the notebooks:
* [Visualize effectivity.ipynb](Visualize%20effectivity.ipynb) to visualize the effect of the tracing policies and check if they contain the spread.
* [Visualize quarantines.ipynb](Visualize%20quarantines.ipynb) to visualize the temporal evolution of the number of quarantined people (both false positive and false negative).


## Documentation:
The official documentation can be found [here](https://digitalcontacttracing.github.io/covid_code/doc/site/).

## How to cite:
If you use this code in your work, please consider citing the paper

```bibtex:
@techreport{Cencetti2020,
	author = {Cencetti, Giulia and Santin, Gabriele and Longa, Antonio and Pigani, Emanuele and Barrat, Alain and Cattuto, Ciro and Lehmann, Sune and Salathe, Marcel and Lepri, Bruno},
	title = {Digital Proximity Tracing in the COVID-19 Pandemic on Empirical Contact Networks},
	elocation-id = {2020.05.29.20115915},
	year = {2020},
	doi = {10.1101/2020.05.29.20115915},
	publisher = {Cold Spring Harbor Laboratory Press},
	URL = {https://www.medrxiv.org/content/early/2020/07/02/2020.05.29.20115915},
	eprint = {https://www.medrxiv.org/content/early/2020/07/02/2020.05.29.20115915.full.pdf},
	journal = {medRxiv}
}
```

## Contacts:
If you have any question or comment, please feel free to drop us an [email](mailto:digital_contact_tracing@fbk.eu).


## Datasets used in the simulations:
<a name="dtu_footnote">1</a>: [Interaction data from the Copenhagen Networks Study](https://www.nature.com/articles/s41597-019-0325-x).

<a name="socio_footnote">2</a>: [Contact Patterns in a High School: A Comparison between Data Collected Using Wearable Sensors, Contact Diaries and Friendship Surveys](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0136497), and [Can co-location be used as a proxy for face-to-face contacts?](https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-018-0140-1).

