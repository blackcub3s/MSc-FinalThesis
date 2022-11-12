
*Activate the dataset!
**THESE ARE THE ONLY COMPUTATIONS MADE WITH SPSS. ALTHOUGH OUR COMMITMENT WITH USING FREE SOFTWARE I WAS NOT ABLE
** TO USE THE CHISQUARE TEST WITH CONFIDENCE USING SCYPY.STATS chi square
** function ( https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html ).

** Thus, hypothesis contrasts for cathegorical variables vs cathegorical variables, are made with SPSS.

DATASET ACTIVATE DataSet1.


*is there a difference between the EMCI/LMCI ratio between the MCI-c and MCI-nc categories ? Pearson Chi Square = 9.421 (p = .002) --> Answer is YES!!

CROSSTABS
  /TABLES=BL.dx BY s_CONVER
  /FORMAT=AVALUE TABLES
  /STATISTICS=CHISQ 
  /CELLS=COUNT
  /COUNT ROUND CELL.


*is there a difference between the Male/female ratio between the MCI-c and MCI-nc categories? Pearson Chi Square = .009 (p = .924) --> Answer is NO!!


CROSSTABS
  /TABLES=PTGENDER BY s_CONVER
  /FORMAT=AVALUE TABLES
  /STATISTICS=CHISQ 
  /CELLS=COUNT
  /COUNT ROUND CELL.


**is there a difference between the SITE rand the ratio between MCI-c and MCI-nc categories? Pearson Chi Square = .009 (p = .924) --> Answer is NO!!


CROSSTABS
  /TABLES=SITE BY s_CONVER
  /FORMAT=AVALUE TABLES
  /STATISTICS=CHISQ 
  /CELLS=COUNT
  /COUNT ROUND CELL.
