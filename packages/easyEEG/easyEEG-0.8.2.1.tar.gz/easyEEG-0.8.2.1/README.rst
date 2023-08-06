# Overview
EasyEEG provides simple, flexible and powerful methods that can be used to directly test neural and psychological hypotheses based on topographic responses. These multivariate methods can investigate effects in the dimensions of response magnitude and topographic patterns separately using data in the sensor space, therefore enable assessing neural sources and its dynamics without sophisticated localization. Python based algorithms provide concise and extendable features of EasyEEG. Users of all levels can benefit from EasyEEG and obtain a straightforward solution to efficiently handle and process EEG data and a complete pipeline from raw data to publication.  


---
## Documentation
See http://easyeeg.readthedocs.io/en/latest/ for introduction, tutorials, and reference manual.

---
# Installation instructions

EasyEEG has been tested on Python3.X 64bit.
(Current it might be unfit for older versions like Python2.7. But since Python2 will become obsolete in the years to come, why not drop it anyaway and take Python3 instead?)

The simplest way to install EasyEEG is through the Python Package Index (PyPI), which ensures that all required dependencies are established. This can be achieved by executing the following command:

```
pip install easyEEG
```
or:
```
sudo pip install easyEEG
```

###*Required Dependencies*

- numpy
- pandas
- scipy
- matplotlib
- statsmodels
- seaborn
- mne
- permute
- tqdm
