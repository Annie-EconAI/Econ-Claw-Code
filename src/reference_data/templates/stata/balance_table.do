/*==============================================================================
  Balance Table: Treatment vs. Control
  Requires: iebaltab (from ietoolkit: ssc install ietoolkit)
==============================================================================*/

use "${data}/${DATASET}.dta", clear

* ── Balance Table ────────────────────────────────────────────────────────────
iebaltab ${BALANCE_VARS}, ///
    grpvar(${TREATMENT}) ///
    save("${tables}/balance_table.tex") replace ///
    rowvarlabels ///
    pttest starsnoadd ///
    tblnote("Notes: Column (1) reports means for control group, Column (2) for treatment group. Column (3) reports the difference. Standard errors in parentheses. *** p<0.01, ** p<0.05, * p<0.1.")
