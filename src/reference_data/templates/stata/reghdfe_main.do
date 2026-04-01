/*==============================================================================
  Project:        ${PROJECT}
  Do-file:        ${FILENAME}
  Author:         ${AUTHOR}
  Created:        ${DATE}
  Last modified:  ${DATE}
  Purpose:        ${PURPOSE}
  Input:          ${INPUT}
  Output:         ${OUTPUT}
==============================================================================*/

clear all
set more off
set matsize 10000

* ── Globals ──────────────────────────────────────────────────────────────────
global root     "${ROOT}"
global data     "${root}/data"
global code     "${root}/code"
global output   "${root}/output"
global tables   "${output}/tables"
global figures  "${output}/figures"

* ── Main ─────────────────────────────────────────────────────────────────────
use "${data}/${DATASET}.dta", clear

* --- Main Results Table ---
eststo clear

eststo m1: reghdfe ${DEPVAR} ${TREATMENT}, absorb(${FE1}) cluster(${CLUSTER})
eststo m2: reghdfe ${DEPVAR} ${TREATMENT} ${CONTROLS1}, absorb(${FE1}) cluster(${CLUSTER})
eststo m3: reghdfe ${DEPVAR} ${TREATMENT} ${CONTROLS1}, absorb(${FE1} ${FE2}) cluster(${CLUSTER})

esttab m1 m2 m3 using "${tables}/main_results.tex", replace ///
    label star(* 0.10 ** 0.05 *** 0.01) ///
    se(3) b(3) ///
    title("Main Results") ///
    keep(${TREATMENT}) ///
    stats(N r2_a mean_depvar, ///
        labels("Observations" "Adj. R-squared" "Mean Dep. Var.") ///
        fmt(%9.0fc %9.3f %9.3f)) ///
    nomtitles ///
    addnotes("Standard errors clustered at ${CLUSTER} level.")
