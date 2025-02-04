"""

PLANTILLA ADAPTADA DE : http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html#sphx-glr-auto-examples-model-selection-plot-roc-crossval-py
=============================================================
Receiver Operating Characteristic (ROC) with cross validation
=============================================================

Example of Receiver Operating Characteristic (ROC) metric to evaluate
classifier output quality using cross-validation.

ROC curves typically feature true positive rate on the Y axis, and false
positive rate on the X axis. This means that the top left corner of the plot is
the "ideal" point - a false positive rate of zero, and a true positive rate of
one. This is not very realistic, but it does mean that a larger area under the
curve (AUC) is usually better.

The "steepness" of ROC curves is also important, since it is ideal to maximize
the true positive rate while minimizing the false positive rate.

This example shows the ROC response of different datasets, created from K-fold
cross-validation. Taking all of these curves, it is possible to calculate the
mean area under curve, and see the variance of the curve when the
training set is split into different subsets. This roughly shows how the
classifier output is affected by changes in the training data, and how
different the splits generated by K-fold cross-validation are from one another.

.. note::

    See also :func:`sklearn.metrics.auc_score`,
             :func:`sklearn.model_selection.cross_val_score`,
             :ref:`sphx_glr_auto_examples_model_selection_plot_roc.py`,

"""
import os
import numpy as np
from scipy import interp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import confusion_matrix_pretty_print
from itertools import cycle
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix #IMPORTAT PER MI
from sklearn.feature_selection import RFECV

from sklearn import svm, datasets
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import brier_score_loss

import time 
import math

def IC95(p,N):
    """Inputs: p, proporcio estimada. N mida mostral. RETURNS: (li,ls,mig_interval). || Funció: calcula l'IC al 95 per cent d'una proporció. || Bib: http://davidmlane.com/hyperstat/B9168.html. Validat a: https://www.allto.co.uk/tools/statistic-calculators/confidence-interval-for-proportions-calculator/"""
    mig_interval = 1.96*math.sqrt(p*(1-p)/N)
    return p - mig_interval, p + mig_interval



def PCA_10foldCV_ROC(X,y,PCA_by_santi,rfecv,fes_violin_plot_accuracies_per_folds_i_classificador,carpeta):
    from aux__reduccio_dimensions import Analisi_components_principals as dades_acp
    """
    X = Dades d'entrada 
    y = labels
    PCA = BOOLEA sobre si vols PCA o no abans de introduir aquestes dades al model
    RFECV = BOOLEA sobre si vols aplicar Recursive Feature Elimination per a cada classificador o no
    """
    
    #n_samples, n_features = X.shape
    n_samples = X.shape[0]
    ################################## Classification and ROC analysis#########################


    #Posa els noms dels classificadors i els noms dels objectes. Aixi pots iterar en cada un d'ells i fer una 10-fold CV per a cada un.
    noms_classificadors = ["Logistic Regression",
                            "Gaussian Naive Bayes",
                            "Support Vector Machines (linear kernel)", 
                            "Nearest Neighbours",
                            "Multilayer perceptron (ANN)"]
    objectes_classificadors = [LogisticRegression(C=10000, penalty='l2', multi_class= 'multinomial', solver='lbfgs', class_weight = "balanced"),
                                GaussianNB(), 
                                svm.SVC(kernel='linear', probability=True, random_state=1, class_weight = "balanced"),
                                KNeighborsClassifier(3), 
                                MLPClassifier(alpha=1, hidden_layer_sizes=(100,), activation='relu', solver='sgd')] #PROVA ADAM

    #aqui guardo les accuracies per classificador, i en faig un violin plot després.
    #NOTA QUE AMB AIXO PUC CREAR FACILMENT UN PANDAS DATAFRAME I FER EL VIOLINPLOT DESPRÉS
    dic_acc_per_fold_i_classificador = {} #{"Logistic Regression":[FLOAT_accuracy_fold_1, FLOAT_accuracy_fold_2, [...], FLOAT_accuracy fold 10], "Gaussian Naive Bayes":[], ..., "Multilayer perceptron (ANN)":[]}

    #CREEM ELS FITXERS ON GUARDAR LES METRIQUES PER CADA MODEL (TANT LES MESURES DE DIAGNOSTIC ACCURACY COM LES BRIER SCORES)
    f1 = open("./"+carpeta+"/LATEX_acc_s_e_ppv_npv_lrmes_lrmenys_PERCADAMODEL_.txt","w"); f1.write("\n\\toprule\nclassifier&accuracy&sensibility&specificity&ppv&npv&LR+&LR-\n\midrule\\\\\n") #fes la capsalera per a latex
    f2 = open("./"+carpeta+"/LATEX_brierScores_PERCADAMODEL_.txt","w"); f2.write("\\toprule\nBrier Scores & H.L. test\\\n\midrule\n") #fes la capsalera per a latex
    f4 = open("./"+carpeta+"/intervalsConfiansaIconfusionsMatrix.txt","w")
    f_readme = open("./"+carpeta+"/README_PREDICT_PROBAS.txt","w")
    f_readme.write("L'arxiu PREDICT_PROBA_NOMMODEL conte columnes separades per espais blanc segons:\n\n'PREDICCIO' --> (0 mci-nc, 1 mci-c)\n'LABEL'--> (idem a valor predit pero el valor que prove de ADNIMERGE, el valor real)\n'P_mci_nc'--> prob de pertanyer a grup 0 o mci-nc.\n'P_mci_c' --> probabilitat de pertanyer a grup MCI-c (1-p) o grup codificat amb 1.\n'Fold' --> el fold la crossvalidation don prove el subjecte.\n\nNoteu que aquest arxiu ajunta tots els folds de la cross validation i tindra tants subjectes\ncom subjectes hi hagi a la mostra. Cal tenir en compte que l'ordre es preserva perque CV.split() -on CV es objecte Stratified k-fold-\nens permet aleatoritzar sempre de la mateixa\nmanera, perque random_state=None per defecte.\nAixo permet que aquestes dades es puguin prendre per fer un multimodal approach de late integration.")
    f_readme.close()
    matriu_violinplot_sensibEsp = []
    ############################################################################################
    #ITEREM EN CADA CLASSIFICADOR. FEM 10 FOLD CROSS VALIDATION. FEM LES ROC CURVES PER CADA CLASSIFICADOR.
    ll_sens_espe_classificador = [] #per fer violinplot sens i espec
    for i in range(len(objectes_classificadors)):
        f3 = open("./fMRI_models_finals/PREDICT_PROBA_"+noms_classificadors[i].replace(" ","_")+".csv","w") #GUARDO PREDIT, GS,
        f3.write("PREDICCIO,LABEL,P_mci_nc,P_mci_c\n")
        clf, nom_clf =  objectes_classificadors[i], noms_classificadors[i] #carrego l'objecte classificador i l'string que descriu cada classificador
        CV = StratifiedKFold(n_splits=10)
       
        #IMPLEMENT RECURSIVE FEATURE ELIMINATION [NO FUNCIONA]
        if rfecv:        
            clf = RFECV(estimator=clf, step=1, cv=CV, scoring='accuracy')
        tprs, aucs = [], []; mean_fpr = np.linspace(0, 1, 100) #COSES DE LA PLANTILLA
        
        
        #creem llistes buides per acumular els true negatives, flase positives, false negatives i true positives per a despres fer una confusion matrix final.
        suma_tn, suma_fp, suma_fn, suma_tp = 0,0,0,0
        accuracies_mitjanes_mal_procediment = 0 
        ll_acc_classificador = []  #creo llista buida


        j = 1 #per contar els folds
        #ITEREM EN ELS DIVERSOS FOLDS CREATS PER SKLEARN, DINS CADA CLASSIFICADOR
        y_certes, y_predites = [], [] #per a crear les brier scores per a cada classificador
        for train, test in CV.split(X, y): #CSEPARA ELS INDEX 
            #OJO AMB ELS EFECTES ALIAS! PER AIXO LA COPIO...
            X_entrenament = np.copy(X[train]) 
            X_test = np.copy(X[test])
            if PCA_by_santi:
                estandaritza_variables = False #POSA TRUE SI VOLS ESTANDARITZAR LES VARIABLE SPER COLUMNES. POSA FALSE EN CAS CONTRARI
                dades = dades_acp(np.array(X_entrenament,dtype = np.float64), nombre_components = None, estandaritza_variables = estandaritza_variables, llista_variables=[])
                #dades.matriu_correlacions(grafic_correlacions = False)  # ACP es basa en la matriu de corr. davant absencia de proves de esfericitat (bartlett,KMO) es importantissim mirar que la matriu de correlacions no s'apropa a la matriu identitat. Volem variables correlacionades o no te sentit aplicar PCA
                #dades.autovalors_i_variansssa(scree_plot=True)       # veure autovalors, variança explicada i screeplot. Amb això (especialment amb l'screeplot), decideix quants components retenir combinant variança explicada i parsimònia.
                #dades.carregues_factorials()                        # veure les correlacions entre cada factor i cada variable
                dades.carregues_factorials()#vaig fer un castell de naipes i cal execitar aquesta funcio si o si, o la eguent no va.
                X_entrenament, ll_mitjana_train, ll_desvest_train, carregues_factorials_train = dades.puntuacions_factorials(imprimeix_dataset_reduit = False) # METODE QUE RETONRA EL DATAET REDUIT. ndarray reduit! em prenc les mitjanes i desviacions estandar estimades per a fer la estandaritzacio des de les dades d'entrenament
                if estandaritza_variables:
                    X_test = ((X_test - ll_mitjana_train) / ll_desvest_train).dot(carregues_factorials_train) #apliquem column wise les operacions  
                else:
                    print(X_test.shape)
                    print(carregues_factorials_train.shape)
                    X_test = X_test.dot(carregues_factorials_train) # X_test * carregues_factorials_train  -->  https://stackoverflow.com/questions/24560298/python-numpy-valueerror-operands-could-not-be-broadcast-together-with-shapes
                    print(X_test.shape)
                print("###########################")
                print("X_entrenament: ",X_entrenament.shape) #(57,ncomponents)
                print(len(ll_mitjana_train))#(22791,) 
                print(len(ll_desvest_train)) #(22791,) CONTE DESVIACIONS TIPIQUES DUTES DE TRAIN
                print(carregues_factorials_train.shape) #(22791,components)
                print("X_test_post pca: ",X_test) #9,ncomp 
                print("###########################")
            print("Ara entrenant: ",nom_clf)
            ##### CREO ESTADISTIQUES PER A CADA FOLD (DIAGNOSTIC ACCURACY) I LES VAIG GUARDANT PER CREAR LA CONFUSION MATRIX FINAL  #########
            print("###### FOLD"+str(j)+" ######")
            print("#############################")
            ####################################################################
            clf.fit(X_entrenament, y[train])    #pas 1 --> entreno les dades, per a cada fold
            probas_ = clf.predict_proba(X_test) #pas 2 --> testejo el model a les dades d'entreno (TREU MATRIU PROBABILITATS [p, 1-p] per a cada fold)
            y_predits_test = np.argmax(probas_, axis=1)
            ###################################################################
            #DEFINEIXO LA CONFUSION MATRIX PER A CADA FOLD I IMPRIMEIXO ELS INDEXOS 
            tn, fp, fn, tp = confusion_matrix(y[test], y_predits_test).ravel()
            accuracies_mitjanes_mal_procediment += (tp+tn)/(tp+tn+fp+fn)
            acc, s, e = (tp+tn)/(tp+tn+fp+fn), tp/(tp+fn), tn/(fp+tn)
            imprimeix_diagnostic_accuracy_a_cada_fold = True


            for k in range(len(probas_)):
                p, u_menys_p = probas_[k]
                predit, gold_standard = y_predits_test[k], y[test][k]
                f3.write(str(predit)+","+str(gold_standard)+","+str(p)+","+str(u_menys_p)+","+str(j)+'\n')#PREDICCIO,LABEL,P_mci_nc,P_mci_c,fold
                y_certes += [gold_standard]#per calcular brier scores
                y_predites += [predit]#per calcular brier scores
            if imprimeix_diagnostic_accuracy_a_cada_fold:
                print("probabilitats  ||  y_predits_Test ||   y_labels_test")
                print(probas_,np.argmax(probas_,axis=1),y[test]) # FET PER MI_ IMPRIMEIXO PROBABILITATS, PROBABILITATS TRANSFORMADES A VALOR MAX (ARGMAX) I LABELS)
                print("\n#######################")
                print("Accuracy: {:.5f}".format(acc))
                print("Sensibilitat: {:.5f}".format(s))
                print("Especificitat: {:.5f}".format(e))
                print("Valor predictiu + (PPV): {:.5f}".format(tp/(tp+fp))) #tambe anomenat precision score. hi ha una funcio a sklearn que ho fa
                print("Valor predictiu - (NPV): {:.5f}".format(tn/(fn+tn)))
                print("LR+: {:.5f}".format(s / (1 - e)))
                print("LR-: {:.5f}".format((1 - s)/e))
                print("#######################")
                print("tn,fp,fn,tp: ",tn,fp,fn,tp)
                print("#######################\n")      
            if fes_violin_plot_accuracies_per_folds_i_classificador:
                ll_acc_classificador += [acc]
                ll_sens_espe_classificador += [[noms_classificadors[i],"sensitivity",s]] #faig llista [[clsf[i], s1, e1],[[clsf[i], s2, e2],...,[clsf[i], sk, ek]] on k es el nombre de folds. Ha de tenir dimensio (50,3) --> 10 folds * 5 CLASSIFICADORS * 2 proporcions per fold (una sens i una esp.) = 100 files | 3 variables (COMPROVAT)
                ll_sens_espe_classificador += [[noms_classificadors[i],"specificity",e]]
            

            

            #VAIG ACUMULANT ELS VALORS PER A CADA FOLD PER TAL DE TENIR UNA CONFUSION MATRIX FINAL, DESPRÉS DE LA VALIDACIÓ CREUADA
            suma_tn += tn
            suma_fp += fp
            suma_fn += fn
            suma_tp += tp


            # Compute ROC curve and area the curve
            fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1]) #PER QUE DIMONIS TREU DIVERSOS INDEXOS DE FPR i TPR PER A CADA FOLD? SI NOMÉS N'HI HA D'HAVER UN...
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            plt.plot(fpr, tpr, lw=1, alpha=0.3,
                     label='ROC fold %d (AUC = %0.2f)' % (j, roc_auc))

            j = j + 1
        
        f3.close()





        if fes_violin_plot_accuracies_per_folds_i_classificador:
            dic_acc_per_fold_i_classificador[noms_classificadors[i]] = [] #CREO LES CLAUS DEL DICCIONARI, CAL INICIALITZAR-LES PRIMER RECORDA, SINO DONA ERROR
            dic_acc_per_fold_i_classificador[noms_classificadors[i]] = ll_acc_classificador #afegeixo al diccionari una llista amb les accuracies per fold
        
        #print("######################################");print("######################################",file=f4)
        #print("Accuracy mitjana (mitjana 10 accuracies): {:.4f}".format(accuracies_mitjanes_mal_procediment/10));print("Accuracy mitjana (mitjana 10 accuracies): {:.4f}".format(accuracies_mitjanes_mal_procediment/10), file=f4)
        print("\n\n##################################################");print("\n\n\n\n##################################################",file=f4)
        print("RESULTAT DESPRES DE SUMAR ELS FP,TN,TP,FN DELS 10 FOLDs\n               ("+nom_clf+")");print("RESULTAT DESPRES DE SUMAR ELS FP,TN,TP,FN DELS 10 FOLDs\n               ("+nom_clf+")",file=f4)
        print("####################################################"); print("####################################################", file=f4)
        brier_score = brier_score_loss(y_certes, y_predites)  
        accuracy, s, e, ppv, npv = (suma_tp+suma_tn)/(suma_tp+suma_tn+suma_fp+suma_fn), suma_tp/(suma_tp+suma_fn), suma_tn/(suma_fp+suma_tn), suma_tp/(suma_tp+suma_fp), suma_tn/(suma_fn+suma_tn)
        LRmes, LRmenys = s/(1 - e), (1 - s)/e
        #faig intervals de confiansssa!
        print("\nAccuracy: {:.5f}         (IC95 % de {:.2f} A {:.2f})".format(accuracy, IC95(accuracy,n_samples)[0],IC95(accuracy,n_samples)[1]));print("\nAccuracy: {:.5f}         (IC95 % de {:.2f} A {:.2f})".format(accuracy, IC95(accuracy,n_samples)[0],IC95(accuracy,n_samples)[1]),file=f4)
        print("Sensibilitat: {:.5f}     (IC95 % de {:.2f} A {:.2f})".format(s,IC95(s,n_samples)[0],IC95(s,n_samples)[1]));print("Sensibilitat: {:.5f}     (IC95 % de {:.2f} A {:.2f})".format(s,IC95(s,n_samples)[0],IC95(s,n_samples)[1]), file=f4)
        print("Especificitat: {:.5f}   (IC95 % de {:.2f} A {:.2f})".format(e,IC95(e,n_samples)[0],IC95(e,n_samples)[1]));print("Especificitat: {:.5f}   (IC95 % de {:.2f} A {:.2f})".format(e,IC95(e,n_samples)[0],IC95(e,n_samples)[1]),file=f4)
        print("Valor pred + (PPV): {:.5f} (IC95 % de {:.2f} A {:.2f})".format(ppv,IC95(ppv,n_samples)[0],IC95(ppv,n_samples)[1]));print("Valor pred + (PPV): {:.5f} (IC95 % de {:.2f} A {:.2f})".format(ppv,IC95(ppv,n_samples)[0],IC95(ppv,n_samples)[1]), file=f4) #tambe anomenat precision score. hi ha una funcio a sklearn que ho fa#tambe anomenat precision score. hi ha una funcio a sklearn que ho fa
        print("Valor pred - (NPV): {:.5f} (IC95 % de {:.2f} A {:.2f})".format(npv,IC95(npv,n_samples)[0],IC95(npv,n_samples)[1]));       print("Valor pred - (NPV): {:.5f} (IC95 % de {:.2f} A {:.2f})".format(npv,IC95(npv,n_samples)[0],IC95(npv,n_samples)[1]),file=f4)
        print("LR+: {:.5f}".format(LRmes));print("LR+: {:.5f}".format(LRmes),file=f4)
        print("LR-: {:.5f}".format(LRmenys));print("LR-: {:.5f}".format(LRmenys),file=f4)
        print("Brier score final: {:.3f} ".format(brier_score));print("Brier score final: {:.3f} ".format(brier_score),file=f4) #calibracio & performance del model
        print("###############C O N F U S I O N   M A T R I X##############");print("###############C O N F U S I O N   M A T R I X##############",file=f4)
        print("                              alzh    no alzh");print("                              alzh    no alzh",file=f4)
        print("sumatoris (tp,fp) |  +test     {:2}     {:2}".format(suma_tp, suma_fp)); print("sumatoris (tp,fp) |  +test     {:2}     {:2}".format(suma_tp, suma_fp),file=f4)
        print("          (fn,tn) |  -test     {:2}     {:2}".format(suma_fn,suma_tn));print("          (fn,tn) |  -test     {:2}     {:2}".format(suma_fn,suma_tn),file=f4)
        print("############################################################\n");print("############################################################\n", file=f4)    

        #guardo les confusion matrix per fer un heatmap despres
        os.chdir("."+os.sep+carpeta)
        np.save("confusion_matrix__"+noms_classificadors[i], np.array([[suma_tp, suma_fp],[suma_fn, suma_tn]]))
        os.chdir("../")

        #GUARDO AL FITXER DE RESUM PER CLASSIFICADOR (QUE CREA EL TXT QUE ANIRA A LATEX A LA TAULA DE ACCURACIES)
        #accuracy&sensibility&specificity&ppv&npv&LR+&LR str(
        f1.write(noms_classificadors[i]+" & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.3f} & {:.3f}\\\\\n".format(accuracy*100, s*100, e*100, ppv*100, npv*100, LRmes, LRmenys))
        f2.write("{:.3f}".format(brier_score)+"& HOSMER SIMPSON\\\\\n") #https://www.data-essential.com/hosman-lemeshow-in-python/

        plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
                 label='Luck', alpha=.8)
        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        plt.plot(mean_fpr, mean_tpr, color='b',
                 label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
                 lw=2, alpha=.8)
        std_tpr = np.std(tprs, axis=0)
        print("\n######################################");print("\n######################################",file=f4)
        #print("mean_tpr: ",mean_tpr,"std_tpr",std_tpr)
        print("mean_auc:",mean_auc, "std_auc",std_auc);print("mean_auc:",mean_auc, "std_auc",std_auc, file=f4)
        print("######################################\n");print("######################################",file=f4)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                         label=r'$\pm$ 1 std. dev.')
        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel('False Positive Rate (1-especificity)')
        plt.ylabel('True Positive Rate (sensitivity)')
        plt.title(nom_clf)
        plt.legend(loc="lower right")
        plt.show()

    f1.write("\\bottomrule")
    f2.write("\\bottomrule")
    f4.close()
    f1.close() 
    f2.close()
    #UN COP HA ENTRENAT TOTS ELS MODELS CREO EL DATAFRAME D'ACCURACIES PER CLASSIFICADOR I EL PLOTEJO AMB SEABORN
    df_acc_per_classificador = pd.DataFrame(dic_acc_per_fold_i_classificador) #com a claus dels diccionaris hi ha els noms dels classificadors ja definits abans en la llista del principi
    sns.set(style="whitegrid")
    ax = sns.violinplot(data=df_acc_per_classificador, palette="muted", order=["Multilayer perceptron (ANN)","Logistic Regression","Support Vector Machines (linear kernel)", "Nearest Neighbours","Gaussian Naive Bayes"])
    plt.ylabel("Accuracy")
    plt.xlabel("Machine learning model (classifier)")
    #plt.ylim(0,1)
    plt.show()


    #FAIG ARA EL MATEIX AMB LES SENSIBILITATS I ESPECIFITATS PER CLASSIFICADOR
    plt.close()
    sns.set(style="whitegrid")                          #strin del model, si es Sensitivity o specificity, mesura (proporcio)
    df_sensEsp_per_classificador = pd.DataFrame(columns=["model","metric","p"], data=ll_sens_espe_classificador)

    ax = sns.violinplot(x="model", y="p", hue="metric",data=df_sensEsp_per_classificador, palette="muted",order=["Multilayer perceptron (ANN)","Logistic Regression","Support Vector Machines (linear kernel)", "Nearest Neighbours","Gaussian Naive Bayes"])
    plt.ylabel("sensibility/specificity")
    plt.xlabel("Machine learning model (classifier)")
    #plt.ylim(0,1)
    plt.show()