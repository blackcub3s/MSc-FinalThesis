#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:50:53 2017

@author: andrea insabato
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import ShuffleSplit
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def funcio_ml_by_andrea(X,y):
    # load data and build data matrix X and labels y
    #movFC = np.load(nom_arxiu)  # [subj, sess, timelag, roi, roi]  #[22,5,3,66,66] 
    #print(movFC.shape) #--> #[22,5,3,66,66]

    #fcM = np.reshape(movFC[:,:,0, np.tril_indices(66, k=-1)[0], np.tril_indices(66, k=-1)[1]], [movFC.shape[0], movFC.shape[1], int((66*66-66)/2)])
    #print(fcM.shape) #--> [22,5,2145] --> Què es time lag? Només pren el primer i perd la dimensió.

    #X = np.reshape(fcM, [fcM.shape[0]*fcM.shape[1], fcM.shape[2]])  # stack all sessions from all subjects to build X
    #print(X.shape) #--> [110,2145] --> [110 sessions (22 subjectes * 5 sesssions per subjecte)]
    
    #min_num_sessM = np.shape(fcM)[1]
    
    #num_subjM = np.shape(fcM)[0]


    #y = np.array([0 if sess_id<2 else 1 for i in range(num_subjM) for sess_id in range(min_num_sessM)])  # labels
    #print(y.shape) #--> [110,] --> vector columna de 110 files (tantes com matrius de correlacions vectoritzades hi ha)


    # classifier: logistic regression
    

    # corresponding pipeline: zscore and pca can be easily turned on or off
    pipe_z_pca_mlr = Pipeline([('zscore', StandardScaler()), 
    			 ('pca', PCA()),
                             ('clf', clf)])
    pipe_pca_mlr = Pipeline([('pca', PCA()),
                             ('clf', clf)])
    pipe_mlr = Pipeline([('clf', clf)])
    repetitions = 100  # number of times the train/test split is repeated
    # shuffle splits for validation test accuracy
    shS = ShuffleSplit(n_splits=repetitions, test_size=None, train_size=.8, random_state=0)

    score_z_pca_mlr = np.zeros([repetitions])
    score_pca_mlr = np.zeros([repetitions])
    score_mlr = np.zeros([repetitions])
    i = 0  # counter for repetitions
    for train_idx, test_idx in shS.split(X):  # repetitions loop
        data_train = X[train_idx, :]
        y_train = y[train_idx]
        data_test = X[test_idx, :]
        y_test = y[test_idx]
        pipe_z_pca_mlr.fit(data_train, y_train)
        score_z_pca_mlr[i] = pipe_z_pca_mlr.score(data_test, y_test)
        pipe_pca_mlr.fit(data_train, y_train)
        score_pca_mlr[i] = pipe_pca_mlr.score(data_test, y_test)
        pipe_mlr.fit(data_train, y_train)
        score_mlr[i] = pipe_mlr.score(data_test, y_test)
        i+=1
            
    # plot comparison as violin plots
    fig, ax = plt.subplots()
    sns.violinplot(data=[score_z_pca_mlr, score_pca_mlr, score_mlr], cut=0, orient='h', scale='width')
    ax.set_yticklabels(['z+PCA+MLR', 'PCA+MLR', 'MLR'])

#funcio_ml_by_andrea('FC_emp_movie.npy')