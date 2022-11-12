# REPOSITORY DESCRIPTION

This repository contains 
- /TFM_FINAL_santiagosanchez.pdf: the final thesis as was handed in to the university. You can find its abstract down below
- ./Writing: Contains the LaTeX files and figures that were put together in order to compile /TFM_FINAL_santiagosanchez.pd.
- ./DataAnalysis: this folder contains the most important programs I made in Python to do the analysis. Within the folder ./DataAnalysis/inContext you'll find the same programs as before, but now in context, with some of the raw data behind (and other files that contributed to the development of the final thesis). Lots of files are missing as github has limited space, so this is a simplification of the directories of my final thesis, not an exhaustive tour to it!

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

## ./Writing:

lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet 

## ./DataAnalysis

lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet lorem ipsum sit amet  asd
