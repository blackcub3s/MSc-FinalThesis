# REPOSITORY DESCRIPTION

This repository contains my MSc's final thesis and the the most important programs that I made, which were key to arrive to its end. These are the most important files and folders, explained:

- [TFM_FINAL_santiagosanchez.pdf](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/TFM_FINAL_santiagosanchez.pdf): the final thesis as was handed in to the university.
- [Writing](https://github.com/blackcub3s/MSc-FinalThesis/tree/main/Writing): Contains the LaTeX files and figures that were put together in order to compile * *TFM_FINAL_santiagosanchez.pdf* *
- [DataAnalysis](https://github.com/blackcub3s/MSc-FinalThesis/tree/main/DataAnalysis): this folder contains the most important programs I made in Python to do the analysis. Within the sub folder [inContext](https://github.com/blackcub3s/MSc-FinalThesis/tree/main/DataAnalysis/inContext) you'll find the same programs, but in context with some of the raw data behind (and other files that contributed to the development of the final thesis)[^1]. The most important files are linked here and you can look into them:


    * [mira_dades.py](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/mira_dades.py): In this script the most important functions are these:
        1. Merge two datasets with complementary information: see `IMPORTANT_depura_ADNI_MERGE_i_ARXIU_fMRIs()`
        2. See which subjects convert to alzheimer's and which do not: see `temps_de_conversio(SUBMODALITAT_fMRI)` 
    * [a. fes_merge_en_tensor_3d (obte l'array 3d).py](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/a.%20fes_merge_en_tensor_3d%20(obteArray3d).py): In this file the most important snippet of code is the funcion `fes_merge(n_timeseries)` (see down below). 
        https://github.com/blackcub3s/MSc-FinalThesis/blob/bd8e13d5ad14fc7103469cd7c6f38da0e5008288/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/a.%20fes_merge_en_tensor_3d%20(obteArray3d).py#L39-L114

        On the one hand, this function went to each folder name of syntax *"SUBJECTID__UID"* and got the *"SUBJECTID"* (identifier for subject) and *"LLUID"* (identifier for scanner type made to a given subject) to save them in list objects and finally store them in respective .txt files (`__subjectes.txt` and `__uids.txt`). On the other hand, the function also went into each subject folder to find `total.txt` a file that contained fMRI data extracted from .NIFTI files *after* registering that information to Shen's atlas[^3] via FSL. The information inside each subject's `total.txt` was structured as shape `(214,140)` (the first dimension being the Regions of interest (ROIs[^4]) of Shen's atlas -214- and the second one was the number of time series data points available -140 time series data points for each ROI-) and finally I stacked together all these matrices as a numpy ndarray object (*.npy*) to have it all within one single file ([__arr_ADNI_3d_preprocessada.npy](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/__arr_ADNI_3d_preprocessada.npy)) of shape `(93,214,140)`[^5]. 

    * [b. analisisfinal.py](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/b.%20analisisfinal.py): The most important functions of this file are:
        `fes_dataframe_despres_dels_3_criteris_dinclusio(d)`: This function narrowed down the subjects that went into the machine learning models according to inclusion criteria of the methods section of my final thesis. 

        https://github.com/blackcub3s/MSc-FinalThesis/blob/3cfe02d11977db9d5d736267c5d6f6114fe82039/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/b.%20analisisfinal.py#L48-L243

        The most important inclusion criteria within that function was how I decided to filter out the subjects who would not convert to Alzheimer's (see the footnote to understand the reasoning that was to be followed[^6]). The idea was to choose the criterion of considering those who wouldn't turn to alzheimer's (MCI-nc) as those subjects who hadn't turn to alzheimers above the time period $t$, such that:

        
        $$ t > μ + n*ρ $$
       
            
        Where  
        
            μ = 2.3 years (average time of turning to alzheimers for those who turn)
            ρ = standard deviation of those who turned to AD
            n = 1.85 (arbitrary number, but if we consider the distribution of time for MCIc to be normal, that would way above the central tendency of the data).

        In the following code, you can see I stored the subjects I would finally analyse within the `df_MCInc` dataframe, by writing this:

        https://github.com/blackcub3s/MSc-FinalThesis/blob/a2479224491c308d72a412e4dc2724107a830fe0/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/b.%20analisisfinal.py#L108-L111

        `mat_corr_labels_i_pipeline()`: This function took the numpy ndarray `arr_TS` with shape *(57,214,140)* (57 subjects with 214 ROIs each and 140 Time Series per ROI) applied the Functional Connectivity definition. The Functional Connectivity (*FC*) is a construct that tells how well connected a brain is. Here, the *FC* of one given subject was defined as all possible correlations between the time series of the subject's ROIs, vectorized in a single line. Namely, for each matrix  *(n,m) = (214,140)* we would get a *(n,n) = (214,214)* pearson correlation matrix (or the adjacency matrix of a complete graph with 214 nodes) called `arr_cor` and stored as [out_FC(57 subjectes).npy](https://github.com/blackcub3s/MSc-FinalThesis/blob/3cfe02d11977db9d5d736267c5d6f6114fe82039/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/out_FC%20(74%20subjectes).npy)[^7] as obtained in this lines of code:



        https://github.com/blackcub3s/MSc-FinalThesis/blob/3cfe02d11977db9d5d736267c5d6f6114fe82039/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/b.%20analisisfinal.py#L305-L321

        And after that, we would take the [out_FC(57 subjectes).npy](https://github.com/blackcub3s/MSc-FinalThesis/blob/3cfe02d11977db9d5d736267c5d6f6114fe82039/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/out_FC%20(74%20subjectes).npy)[^7] and obtain the `ll_ROIxROI_flattened` with shape $ \dfrac{1/2} \cdot n\cdot(n-1) $

        https://github.com/blackcub3s/MSc-FinalThesis/blob/a2479224491c308d72a412e4dc2724107a830fe0/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/b.%20analisisfinal.py#L374-L379

        And the auxiliary function call that allows us to do it is as follows:

        https://github.com/blackcub3s/MSc-FinalThesis/blob/7592ad1c1d86a1427c29db471564e236368d259b/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/funcions_auxiliars.py#L29

    * [aux__ploteja_matrius_correlacions.py](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/aux__ploteja_matrius_correlacions.py): **lorem  asd asd asd asdasd**
    * [aux__reduccio_dimensions.py](https://github.com/blackcub3s/MSc-FinalThesis/blob/main/DataAnalysis/inContext/DADES_PREPROCESSADES_FINALS/aux__reduccio_dimensions.py): This file was done in order to implement a graphical interpretation for the explained variance of a principal components analysis (i.e it plots the eigenvalues of each component for the previously chosen number of components). The scree plot is a graphical way of seeing whether each component of a PCA adds value to what we are trying to model in terms of parsimony. Softwares such as SPSS or R have the possibility of getting a Scree plot easily, but python doesn't (at least, not while I was doing this thesis). So I coded this program to get the scree plot.
    

The packages I've used in this thesis are [sklearn](https://scikit-learn.org/stable/) for machine learning, [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/) for graph generation and visualization, [pandas](https://pandas.pydata.org/) for data analysis, [numpy](https://numpy.org/) for treating the multidimensional arrays that came out of the NIFTI files that came out of the fMRIs[^2].


[^1]: Lots of files are missing as github has limited space, so this is a simplification of the directories of my final thesis, not an exhaustive tour to it!
[^2]: the fMRIs came from a neuroimaging project called ADNI. The [ADNI](https://adni.loni.usc.edu/)(Alzheimer's disease neuroimaging iniciative) gathered together high quality, free to use data on the alzheimer's disease, an without this data this thesis wouldn't have been possible.
[^3]: NIFTI files are not here, as they occupy several Gigabytes of data. This is just for showcasing purposes.
[^4]: Region of Interest (ROI).
[^5]: `(93,214,140) --> (SUBJECTS, ROIs,TIME SERIES)`
[^6]: In my final thesis I took subjects that were at risk of developing Alzheimer's disease but didn't have the disease (these are what are called *Mild Cognitive Impairment* or MCI). At the moment of diagnosis as MCI, they had to undergo a brain fMRI scan. Then time went on and after some years some of them became Alzheimer's disease (MCI-c), and some didn't (MCI-nc). The ones who I labeled as MCI-c are clear to label, but the ones who are MCI-nc are not clear (because there might be not enough longitudinal data because the patient might die, get discontinued from the study). So it was important to choose a criterion to decide how many years of follow up are *enough* for a patient to be considered free of Alzheimer's. 
[^7]: The actual code got 74 subjects, as changes in the inclusion criteria (MCI-nc cutoff time point) varied.
# FINAL THESIS ABSTRACT

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