## ---------------------------
## Script name: N2O parsing
## Purpose of script: Concat multiple Unisense N2O records
## Author: McKenna Farmer
## Date Created: 2022-07-20
## ---------------------------
## Notes:
## ran on 7/20/22
##
## ---------------------------

# packages
library(purrr)
library(readxl)
library(dplyr)
library(lubridate)

# set working directory
path_to_files <- "C:/Users/mckyf/Northwestern University/Wells Research Group - CANDO+P Reactor/Operation and Logs/Sensor logs/Unisense"
setwd(path_to_files)

# get list of excel files in directory
files <- list.files(pattern="*.xlsx")

# use map_dfr performs a function and row binds
n2o <- files %>% map_dfr(read_excel)

# remove extra columns
n2o <- n2o %>% select(date_time,N2O_mgNL_raw,temp)

# export
write.csv(x=n2o,file="n2o_2022_all.csv",row.names=FALSE)

