# kinetic rate values and plots for CANDO+P in-cycle sampling data

# packages
library(readxl)
library(tidyverse)
library(zoo)
library(reshape2)
library(purrr)


#---------------------------------
# data import

setwd("C:/Users/mckyf/Box/CANDO+P and N2O/CANDO+P Reactor 2021/Operation and Logs/Performance logs")
sheet_name <- "master"
in_skalar <- "cycle_results.xlsx"
cycle_skalar <- read_excel(in_skalar, sheet=sheet_name)
start_time <- as.POSIXct("1899-12-31 08:22:00", tz="GMT")

#---------------------------------
# cleaning

cycle_skalar <- cycle_skalar %>% select(-c(date_time))

# time value
cycle_skalar$time_diff <- as.numeric(difftime(cycle_skalar$time, start_time, units="hours"))

# split by nutrient - only OP
df_op <- cycle_skalar %>%                                         # Apply filter & is.na
  filter(!is.na(OP_mgPL))

# split data by phase and date, drop empty dataframes
split_op <- split(df_op,list(df_op$phase,df_op$date), drop=TRUE)

#---------------------------------
# Estimating rate for each date and phase
## Note - In this script, I am estimating the bulk rate over time for the entire phase. I'm not looking at max rate or subsetting the phase at all.
## Entire code from this stackoverflow response :,)
## https://stackoverflow.com/questions/49043166/r-how-do-you-loop-an-linear-model-over-a-list-of-data-frames

# OP rates
lms_op <- lapply(split_op, function(a) coef(lm(OP_mgPL~time_diff, data=a)))
rates_op <- do.call(rbind, lms_op)

# export
write.csv(rates_op, "rates_op.csv")

