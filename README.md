# REPOSITORY DESCRIPTION

This repository contains 
- [TFM_FINAL_santiagosanchez.pdf](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/TFM_FINAL_santiagosanchez.pdf): the final thesis as was handed in to the university. You can find its abstract down below
- [Writing](https://github.com/blackcub3s/MSc-FinalThesis/tree/main/Writing): Contains the LaTeX files and figures that were put together in order to compile /TFM_FINAL_santiagosanchez.pd.
- [DataAnalysis](https://github.com/blackcub3s/FIB-PRO1/tree/main/DataAnalysis): this folder contains the most important programs I made in Python to do the analysis. Within the sub folder [inContext](https://github.com/blackcub3s/FIB-PRO1/tree/main/DataAnalysis/inContext) you'll find the same programs, but in contextx with some of the raw data behind (and other files that contributed to the development of the final thesis)[^1]. The most important files are:


    * [mira_dades.py](https://github.com/blackcub3s/FIB-PRO1/tree/main/DataAnalysis/inContext/mira_dades.py): **lorem ipsum sit amet**
    * [a. fes_merge_en_tensor_3d (obte l'array 3d).py](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/a.%20fes_merge_en_tensor_3d%20(obte%20l'array%203d).py)
    * [b. analisisfinal.py](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/b.%20analisisfinal.py): **lorem ipsum**

    There are also other files which have relevance:

    * [aux__ploteja_matrius_correlacions.py](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/aux__ploteja_matrius_correlacions.py): **lorem ipsum**
    * [aux__reduccio_dimensions.py](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/aux__reduccio_dimensions.py): This file was done in order to implement a graphical interpretation for the explained variance of a principal components analysis (i.e it plots the eigenvalues of each component for the previously chosen number of components). The scree plot is a graphical way of seeing whether each component of a PCA adds value to what we are trying to model in terms of parsimony. Softwares such as SPSS or R have the possibility of getting a Scree plot easily, but python doesn't (at least, not while I was doing this thesis). So I coded this program to get the scree plot.
    
[^1]: Lots of files are missing as github has limited space, so this is a simplification of the directories of my final thesis, not an exhaustive tour to it!

## ABSTRACT

In the last years scientists have tried to develop predictive models for
forecasting a future onset of Alzheimer's disease (AD) in people with Mild
Cognitive Impairment (MCI), using fluid, imaging and neuropsychological
biomarkers. To the best of our knowledge, the question of whether functional
magnetic resonance imaging (fMRI) can serve as a viable predictor for
the aforementioned disease in MCI individuals remains unanswered. We have
developed a single-subject predictive model using, for each individual, solely
a rsfMRI scan obtained at the screening visit of the ADNI and follow-up
longitudinal data about future outcomes (AD presence/absence). We included
in our model 23 MCI-c (mean time until conversion: 1.65 years) and
51 MCI-nc patients (mean time of follow-up: 4.61 years). Scan preprocessing
pipelines consisted on registering each scan to Shen's Atlas (214 ROIs),
extract functional connectivity measures and use them as predictors (either
with or without dimensionality reduction) and pair them with the future
outcomes to train and test supervised machine learning models via 10-fold
cross-validation. We found conversion from MCI to AD can be predicted
from rsfMRI with a multilayer perceptron with no dimensionality reduction
with a reasonable accuracy (77.03%, 95% CI from 67 to 87%), good ROC
AUC (0.81), very high specficity (specMLP = 90.20, 95% CI from 83 to 97%)
but weak sensitivity (47.83%, 95% CI from 36 to 59%). Logistic regression
and the Support Vector machines also obtained reasonable diagnostic accuracies
(75.68%, both of them). The models cannot be deployed to clinical
practice yet: further research is needed to increase sensitivity.

## [Writing](https://github.com/blackcub3s/MSc-FinalThesis/tree/main/Writing):

lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet 

## [DataAnalysis](https://github.com/blackcub3s/FIB-PRO1/tree/main/DataAnalysis)

lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet  asd
