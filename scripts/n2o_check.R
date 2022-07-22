## ---------------------------
## Script name: N2O quick checks
## Purpose of script:
## Author: McKenna Farmer
## Date Created: 2022-07-21
## ---------------------------
## Notes:
## 
## 
## ---------------------------

library(tidyverse)
library(lubridate)
library(ggplot2)
library(zoo)

path_n2o <- "C:/Users/mckyf/Northwestern University/Wells Research Group - CANDO+P Reactor/Operation and Logs/Sensor logs/Unisense"
name_n2o <- "n2o_2022_all.csv"
n2o <- read_csv(file.path(path_n2o,name_n2o))

time_min <- ymd("2022-07-06")
time_max <- ymd("2022-07-07")

n2o_filt <- n2o %>% filter(date_time>=time_min & date_time<=time_max)

ggplot(data=n2o_filt,aes(x=date_time,y=N2O_mgNL_raw)) +
  geom_point(aes(y=rollmean(N2O_mgNL_raw, 120, na.pad=TRUE)))
