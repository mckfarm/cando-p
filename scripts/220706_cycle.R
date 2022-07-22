## ---------------------------
## Script name: 220513_cycle.R
## Purpose of script: Cycle plots for in-cycle sampling
## Author: McKenna Farmer
## Date Created: 2022-07-07
## ---------------------------
## Notes:
## Re-do of previous scripts, hopefully this is cleaner
## No sensor data, just nutrients and acetate
## ---------------------------


# set up ------------
# packages
library(readxl)
library(ggplot2)
library(tidyverse)
library(reshape2)
library(lubridate)
library(cowplot)
library(MetBrewer)
library(zoo)

setwd("~/GitHub/cando-p")

# data read in -------
path_cycle <- "C:/Users/mckyf/Northwestern University/Wells Research Group - CANDO+P Reactor/Operation and Logs/Performance logs"
name_cycle <- "cycle_results_2022.xlsx"
sheet_name <- "22.07.06"

path_n2o <- "C:/Users/mckyf/Northwestern University/Wells Research Group - CANDO+P Reactor/Operation and Logs/Sensor logs/Unisense"
name_n2o <- "n2o_2022_all.csv"

cycle <- read_excel(file.path(path_cycle,name_cycle),sheet=sheet_name)
n2o <- read_csv(file.path(path_n2o,name_n2o))

# output prep
path_out <- file.path("./results/cycle_plots")

# basic cleaning ---------
## cycle cleaning
cycle <- cycle %>%
  select(-c(date,time,"NO2+NO3_mgNL")) %>%
  melt(id.vars=c("hour","date_time","phase")) # make long for plotting

# order the variables
cycle$variable <- factor(cycle$variable,levels=c("OP_mgPL","NO2_mgNL","NO3_mgNL","NH3_mgNL","Ace_mgCODL"))

## n2o cleaning
# select time frame of in-cycle sampling
time_min <- min(cycle$date_time)
time_max <- max(cycle$date_time)

n2o <- n2o %>% filter(date_time>=time_min & date_time<=time_max)
n2o$hour <- as.double(difftime(n2o$date_time,time_min,units="hours"))


# plotting -----------
## acetate and nutrients
nutrients <- ggplot(data=cycle,aes(x=hour,y=value)) +
  geom_point(data=subset(cycle,variable %in% c("OP_mgPL","NO2_mgNL","NO3_mgNL")),
             aes(color=variable,shape=variable),size=2) +
  scale_color_manual(name="Constituent",
                     values=met.brewer("Juarez",4),
                     labels=c("OP","NO2","NO3","NH3")) +
  scale_shape_manual(name="Constituent",
                     values=c(15,16,17,18),
                     labels=c("OP","NO2","NO3","NH3")) +
  theme_half_open() +
  ylim(0,50) +
  labs(y="Concentration [mgP/L or mgN/L]",x="Hour",title="7/6/22 in-cycle sampling")  +
  theme(legend.position="top")

acetate <- ggplot(data=cycle,aes(x=hour,y=value)) +
  geom_point(data=subset(cycle,variable %in% c("Ace_mgCODL")),
             aes(color=variable),size=2,shape=7) +
  scale_color_manual(name="Constituent",
                     values=met.brewer("Cross",1),
                     labels=c("Acetate")) +
  scale_shape_manual(name="Constituent",
                     values=c(1),
                     labels=c("Acetate")) +
  geom_vline(xintercept=1.65,color="grey") +
  geom_vline(xintercept=4.13,color="grey") +
  theme_half_open() +
  scale_y_continuous(limits=c(0,250),position="right") +
  labs(y="Concentration [mgCOD/L]",x="") +
  theme(legend.position="none",
        axis.title.y=element_text(color=met.brewer("Cross",1)),
        axis.text.y=element_text(color=met.brewer("Cross",1)))

aligned_plots <- align_plots(nutrients, acetate, align="hv", axis="tblr")
ggdraw() + draw_plot(aligned_plots[[1]]) + draw_plot(aligned_plots[[2]])
ggsave(filename= path_out %>% file.path("220706_cycle.png"),
       width=7,height=4,dpi=300,units="in")

# n2o
ggplot(data=n2o,aes(x=hour,y=N2O_mgNL_raw)) +
  geom_line(aes(y=rollmean(N2O_mgNL_raw, 120, na.pad=TRUE))) +
  theme_classic() +
  ylim(1,2) +
  geom_vline(xintercept=1.65,color="grey") +
  geom_vline(xintercept=4.13,color="grey") +
  labs(y="N2O [mgN/L]",x="Hour",title="220706 N2O in-cycle sampling")
ggsave(filename= path_out %>% file.path("220706_n2o.png"),
       width=7,height=4,dpi=300,units="in")
