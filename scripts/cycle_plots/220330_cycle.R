# CANDO+P in-cycle sampling visualizations

# change these parameters
start_time <- "2022-03-30 08:22:00"
end_time <- "2022-03-30 14:10:00"
file_path <- "C:/Users/mckyf/Northwestern University/Wells Research Group - CANDO+P and N2O/CANDO+P Reactor/Operation and Logs"

sheet_name <- "22.03.30"

in_hach <- "./Sensor logs/Hach/all_hach.csv"
in_n2o <- "./Sensor logs/Unisense/all_n2o_2022.csv"

# set up ------------
# packages
library(readxl)
library(ggplot2)
library(tidyverse)
library(zoo)
library(lubridate)
library(cowplot)

setwd(file_path)

# data read in - skalar ---------  
# import
in_skalar <- "./Performance logs/cycle_results_2022.xlsx"
cycle_skalar <- read_excel(in_skalar, sheet=sheet_name)

# clean
cycle_skalar <- subset(cycle_skalar,select=-c(date,time,phase)) # remove date,time,phase columns
cycle_skalar$date_time <- ymd_hms(cycle_skalar$date_time, tz="GMT")

# only keeping phosphorus for plotting on another axis
cycle_phosphorus <- cycle_skalar[, c("hour","OP_mgPL")]
cycle_nitrogen <- subset(cycle_skalar,select=-c(OP_mgPL,hour,NH3_mgNL))
# need to remove hour column temporarily until we can combine with n2o sensor data

# data read in - sensors ---------  
data_hach <- bind_rows(lapply(in_hach,read.csv))
data_n2o <- bind_rows(lapply(in_n2o,read.csv))

# clean up data for merging later
data_hach <- subset(data_hach,select=-c(temp_sc200))

data_hach <- data_hach[!duplicated(data_hach),] # remove overlapping data
data_n2o <- data_n2o[!duplicated(data_n2o),]

data_hach$date_time <- ymd_hms(data_hach$date_time, tz="GMT")  # date time
data_n2o$date_time <- ymd_hms(data_n2o$date_time, tz="GMT")

data_n2o$n2o <- as.numeric(data_n2o$n2o) # numeric
data_n2o$temp <- as.numeric(data_n2o$temp)

# subsetting n2o
data_n2o <- data_n2o %>%
  mutate(N2O_mgNL_temp = n2o/(1.033^(21-temp))) %>%
  filter(row_number() %% 60 == 0) %>%
  rename(N2O_mgNL=N2O_mgNL_temp) %>%
  subset(select=-c(temp,N2O_mgNL))

cycle_hach <- data_hach %>%
  filter(date_time >= as.POSIXct(start_time, tz="GMT") 
         & date_time <= as.POSIXct(end_time, tz="GMT"))

cycle_hach$hour <- as.numeric(difftime(cycle_hach$date_time, start_time, units="hours")) + 6

cycle_n2o <- data_n2o %>%
  filter(date_time >= as.POSIXct(start_time, tz="GMT") 
         & date_time <= as.POSIXct(end_time, tz="GMT"))

# merge cycle sampling and hach data into one dataframe
cycle_nitrogen <- merge(cycle_nitrogen, cycle_n2o, by="date_time", all=TRUE)

# cycle_nitrogen[2:ncol(cycle_nitrogen)] <- cycle_nitrogen[2:ncol(cycle_nitrogen)]*5
cycle_nitrogen$hour <- as.numeric(difftime(cycle_nitrogen$date_time, 
                                              ymd_hms(start_time, tz="GMT"), units="hours"))

cycle_skalar$Ace_mgCODL_scale <- cycle_skalar$Ace_mgCODL/(1/.2)

# plotting --------------
ylim_phos <- 20

ggplot() +
  geom_point(data=cycle_phosphorus,mapping=aes(hour,OP_mgPL),color="#034078",shape=15) +
  geom_point(data=cycle_nitrogen,mapping=aes(hour,NO2_mgNL),color="#AA5042",shape=19) +
  geom_point(data=cycle_nitrogen,mapping=aes(hour,n2o),color="#FB5012",shape=20) +
  geom_point(data=cycle_nitrogen,mapping=aes(hour,NO3_mgNL),color="#EA3546",shape=17) +
  geom_point(data=cycle_skalar,mapping=aes(hour,Ace_mgCODL_scale),color="#2BA84A",shape=5) +
  xlab("Hours") +
  ylab("Concentration [mgN/L or mgP/L]") +
  scale_y_continuous(sec.axis=sec_axis(trans=~ ./0.2,name="Concentration [mgCOD/L]")) +
  geom_vline(xintercept=1.81, color="grey") +
  geom_vline(xintercept=4.3, color="grey") +
  annotate("text", x=0.75, y=ylim_phos, label="anaerobic") +
  annotate("text", x=3, y=ylim_phos, label="anoxic") +
  annotate("text", x=5.2, y=ylim_phos, label="aerobic") +
  theme_classic() +
  ggtitle("In-cycle sampling 3/30/22")
ggsave("220330_cycle.tiff",units="px",height=1200,width=2000)
