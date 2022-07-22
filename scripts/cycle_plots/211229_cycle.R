# CANDO+P in-cycle sampling visualizations

# change these parameters
start_time <- "2021-12-28 08:20:00"
end_time <- "2021-12-28 15:00:00"
file_path <- "C:/Users/mckyf/OneDrive - Northwestern University/CANDO+P and N2O/CANDO+P Reactor 2021/Operation and Logs"

sheet_name <- "21.12.28"

in_hach <- "./Sensor logs/Hach/hach_dl_21.12.29.csv"
in_n2o <- "./Sensor logs/Unisense/n2o_211229.xlsx"

# set up ------------
# packages
library(readxl)
library(ggplot2)
library(tidyverse)
library(zoo)
library(lubridate)
library(cowplot)

setwd(file_path)

# custom scale color and labels so all plots are uniform
scale_color_cycle <- function(...){
  ggplot2:::manual_scale("color", values = setNames(c("#AA5042","#EA3546","#FB5012","#034078","#2BA84A"),
                                                    c("NO2_mgNL","NO3_mgNL","N2O_mgNL","OP_mgPL","do_ppm")),
                         labels = setNames(c("NO2 mgNL","NO3 mgNL","N2O mgNL","OP mgPL","DO mgO2L"),
                                           c("NO2_mgNL","NO3_mgNL","N2O_mgNL","OP_mgPL","do_ppm")),
                         ...
  )
}

shape_values = setNames(c(19,17,20,15,6),
                        c("NO2_mgNL","NO3_mgNL","N2O_mgNL","OP_mgPL","do_ppm"))


# data read in - skalar ---------  
# import

in_skalar <- "./Performance logs/cycle_results.xlsx"
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
cycle_nitrogen[2:ncol(cycle_nitrogen)] <- cycle_nitrogen[2:ncol(cycle_nitrogen)]*4
cycle_nitrogen$hour <- as.numeric(difftime(cycle_nitrogen$date_time, 
                                              ymd_hms(start_time, tz="GMT"), units="hours"))


# plotting --------------
ylim_phos <- 20
ylim_nit <- 5

ggplot() +
  geom_point(data=cycle_phosphorus,mapping=aes(hour,OP_mgPL),color="#034078",shape=15) +
  geom_point(data=cycle_nitrogen,mapping=aes(hour,NO2_mgNL),color="#AA5042",shape=19) +
  geom_point(data=cycle_hach,mapping=aes(hour,do_ppm),color="#2BA84A",shape=6) +
  geom_point(data=cycle_nitrogen,mapping=aes(hour,NO3_mgNL),color="#EA3546",shape=17) +
  geom_point(data=cycle_nitrogen,mapping=aes(hour,N2O_mgNL),color="#FB5012",shape=20) +
  xlab("Hours") +
  ylab("Concentration OP and O2") +
  scale_y_continuous(sec.axis=sec_axis(trans=~ ./4,name="Concentration nitrogen")) +
  geom_vline(xintercept=1.78, color="grey") +
  geom_vline(xintercept=5.28, color="grey") +
  annotate("text", x=0.75, y=ylim_phos, label="anaerobic") +
  annotate("text", x=3.5, y=ylim_phos, label="anoxic") +
  annotate("text", x=6, y=ylim_phos, label="aerobic") +
  theme_classic()


