# CANDO+P in-cycle sampling visualizations

# change these parameters
start_time <- "2022-03-02 08:22:00"
end_time <- "2022-03-02 14:30:00"
file_path <- "C:/Users/mckyf/Northwestern University/Wells Research Group - CANDO+P and N2O/CANDO+P Reactor/Operation and Logs"

sheet_name <- "22.03.02"

in_hach <- "./Sensor logs/Hach/hach_dl_220303.csv"
in_n2o <- "./Sensor logs/Unisense/n2o_220303.xlsx"

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
data_n2o <- bind_rows(lapply(in_n2o,read_excel,na="NA"))

# clean up data for merging later
data_hach <- subset(data_hach,select=-c(temp_c))
data_n2o <- subset(data_n2o,select=-c(date,time))

data_hach <- data_hach[!duplicated(data_hach),] # remove overlapping data
data_n2o <- data_n2o[!duplicated(data_n2o),]

data_hach$date_time <- ymd_hms(data_hach$date_time, tz="GMT")  # date time
data_n2o$date_time <- ymd_hms(data_n2o$date_time, tz="GMT")

data_n2o$N2O_mgNL_raw <- as.numeric(data_n2o$N2O_mgNL_raw) # numeric
data_n2o$temp <- as.numeric(data_n2o$temp)

# subsetting n2o
data_n2o <- data_n2o %>%
  mutate(N2O_mgNL_temp = N2O_mgNL_raw/(1.033^(21-temp))) %>%
  filter(row_number() %% 60 == 0) %>%
  rename(N2O_mgNL=N2O_mgNL_temp) %>%
  subset(select=-c(temp,N2O_mgNL_raw))

cycle_hach <- data_hach %>%
  filter(date_time >= as.POSIXct(start_time, tz="GMT") 
         & date_time <= as.POSIXct(end_time, tz="GMT"))

cycle_hach$hour <- as.numeric(difftime(cycle_hach$date_time, start_time, units="hours")) + 6

cycle_n2o <- data_n2o %>%
  filter(date_time >= as.POSIXct(start_time, tz="GMT") 
         & date_time <= as.POSIXct(end_time, tz="GMT"))

# merge cycle sampling and hach data into one dataframe
cycle_nitrogen <- merge(cycle_nitrogen, cycle_n2o, by="date_time", all=TRUE)
cycle_nitrogen$N2O_corr <- cycle_nitrogen$N2O_mgNL - 7

# cycle_nitrogen[2:ncol(cycle_nitrogen)] <- cycle_nitrogen[2:ncol(cycle_nitrogen)]*5
cycle_nitrogen$hour <- as.numeric(difftime(cycle_nitrogen$date_time, 
                                              ymd_hms(start_time, tz="GMT"), units="hours"))

cycle_skalar$Ace_mgCODL_scale <- cycle_skalar$Ace_mgCODL/(1/.17)

# plotting --------------
ylim_phos <- 20
ylim_nit <- 10

# scaling nitrogen values
ggplot() +
  geom_point(data=cycle_phosphorus,mapping=aes(hour,OP_mgPL),color="#034078",shape=15) +
  geom_point(data=cycle_nitrogen,mapping=aes(hour,NO2_mgNL),color="#AA5042",shape=19) +
  geom_point(data=cycle_nitrogen,mapping=aes(hour,NO3_mgNL),color="#EA3546",shape=17) +
  geom_point(data=cycle_nitrogen,mapping=aes(hour,N2O_corr),color="#FB5012",shape=20) +
  geom_point(data=cycle_skalar,mapping=aes(hour,Ace_mgCODL_scale),color="#2BA84A",shape=5) +
  xlab("Hours") +
  ylab("Concentration mgN/L or mgP/L") +
  scale_y_continuous(sec.axis=sec_axis(trans=~ ./0.17,name="Concentration mgCOD/L")) +
  geom_vline(xintercept=1.81, color="grey") +
  geom_vline(xintercept=5.28, color="grey") +
  annotate("text", x=0.75, y=ylim_phos, label="anaerobic") +
  annotate("text", x=3.5, y=ylim_phos, label="anoxic") +
  annotate("text", x=5.9, y=ylim_phos, label="aerobic") +
  theme_classic() +
  ggtitle("In-cycle sampling 3/2/22")
ggsave("220302_cycle.tiff",units="px",height=900,width=1500)
