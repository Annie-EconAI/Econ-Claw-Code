# Main regression table with fixest
# install.packages("fixest")

library(fixest)

# ── Data ─────────────────────────────────────────────────────────────────────
df <- read.csv("${DATA_PATH}")

# ── Estimation ───────────────────────────────────────────────────────────────
m1 <- feols(${DEPVAR} ~ ${TREATMENT} | ${FE1}, data = df, cluster = ~${CLUSTER})
m2 <- feols(${DEPVAR} ~ ${TREATMENT} + ${CONTROLS} | ${FE1}, data = df, cluster = ~${CLUSTER})
m3 <- feols(${DEPVAR} ~ ${TREATMENT} + ${CONTROLS} | ${FE1} + ${FE2}, data = df, cluster = ~${CLUSTER})

# ── Output ───────────────────────────────────────────────────────────────────
etable(m1, m2, m3,
       tex = TRUE,
       file = "${OUTPUT_PATH}/main_results.tex",
       replace = TRUE,
       title = "Main Results",
       dict = c(${TREATMENT} = "Treatment"),
       signif.code = c("***" = 0.01, "**" = 0.05, "*" = 0.10),
       fitstat = ~ n + r2.a)
