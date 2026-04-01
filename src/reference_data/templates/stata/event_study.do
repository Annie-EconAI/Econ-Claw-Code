/*==============================================================================
  Event Study Estimation with Leads and Lags
==============================================================================*/

* ── Setup ────────────────────────────────────────────────────────────────────
* Requires: reghdfe, coefplot

* Generate event-time indicators
* Assume: event_time = year - treatment_year (already in data)
* Reference period: event_time == -1

forvalues k = ${LEADS_MAX}(-1)1 {
    gen lead`k' = (event_time == -`k')
}
forvalues k = 0/${LAGS_MAX} {
    gen lag`k' = (event_time == `k')
}

* Drop lead1 (reference period = t-1)
drop lead1

* ── Estimation ───────────────────────────────────────────────────────────────
reghdfe ${DEPVAR} lead* lag*, absorb(${FE1} ${FE2}) cluster(${CLUSTER})

* ── Event Study Plot ─────────────────────────────────────────────────────────
coefplot, ///
    keep(lead* lag*) ///
    vertical ///
    yline(0, lcolor(gs8) lpattern(dash)) ///
    xline(${LEADS_MAX}, lcolor(red) lpattern(dash)) ///
    xtitle("Event Time") ///
    ytitle("Coefficient Estimate") ///
    title("Event Study: Effect on ${DEPVAR}") ///
    ciopts(recast(rcap) lcolor(navy)) ///
    mcolor(navy) ///
    graphregion(color(white)) ///
    plotregion(margin(b=0))

graph export "${figures}/event_study_${DEPVAR}.pdf", replace
