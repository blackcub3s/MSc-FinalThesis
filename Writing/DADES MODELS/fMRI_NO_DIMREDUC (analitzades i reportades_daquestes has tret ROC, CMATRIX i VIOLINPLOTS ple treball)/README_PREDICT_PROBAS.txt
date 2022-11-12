L'arxiu PREDICT_PROBA_NOMMODEL conte columnes separades per espais blanc segons:

'PREDICCIO' --> (0 mci-nc, 1 mci-c)
'LABEL'--> (idem a valor predit pero el valor que prove de ADNIMERGE, el valor real)
'P_mci_nc'--> prob de pertanyer a grup 0 o mci-nc.
'P_mci_c' --> probabilitat de pertanyer a grup MCI-c (1-p) o grup codificat amb 1.
'Fold' --> el fold la crossvalidation don prove el subjecte.

Noteu que aquest arxiu ajunta tots els folds de la cross validation i tindra tants subjectes
com subjectes hi hagi a la mostra. Cal tenir en compte que l'ordre es preserva perque CV.split() -on CV es objecte Stratified k-fold-
ens permet aleatoritzar sempre de la mateixa
manera, perque random_state=None per defecte.
Aixo permet que aquestes dades es puguin prendre per fer un multimodal approach de late integration.