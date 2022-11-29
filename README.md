# project_f1_dah

Project F1 for the Data Acquisition course

IMPORTANT FILES

The Python script that does all the fitting and contains all the results is the pyroot_test.py (Requires `ROOT`, `numpy`, `matplotlib.pyplot` and freedman from funtions)

The work through for cleaning the data using transverse momenta is in data_cleaning.ipynb (Requires `numpy` and `matplotlib.pyplot`)

all histograms not made in pyroot are produced and contained within histogram_2d_ups.py and histograms.py (require `numpy` and `matplotlib.pyplot`)

`file_handle.py` should not be necessary as all numpy arrays are saved in folders wthin the repository. To check if it works you are expected to have access to one of `.bin` files provided in the DAH dropbox or a file of a similar format.

The format of the `.bin` files

Mass, Pair Transverse Momentum, Rapidity, Momentum Pair, Muon 1 Transverse Momentum, Muon 2 Transverse Momentum

LESS IMPORTANT

The files `iminuit_test.ipynb`, `iminuit_probfit_test.ipynb` and `lmfit_test.ipynb` are not relevant to the results of the project (they are just test files where I worked on learning and appluing iminuit and iminuit alongside probfit
