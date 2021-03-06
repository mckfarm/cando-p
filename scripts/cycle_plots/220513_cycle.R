## ---------------------------
## Script name: 220513_cycle.R
## Purpose of script: Cycle plots for in-cycle sampling
## Author: McKenna Farmer
## Date Created: 2022-05-13
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

# data read in -------
file_path <- "C:/Users/mckyf/Northwestern University/Wells Research Group - CANDO+P Reactor/Operation and Logs/Performance logs"
file_name <- "cycle_results_2022.xlsx"
sheet_name <- "22.05.06"

cycle <- read_excel(file.path(file_path,file_name),sheet=sheet_name)

# basic cleaning ---------
cycle <- cycle %>%
  select(-c(date,time,"NO2+NO3_mgNL")) %>%
  melt(id.vars=c("hour","date_time","phase"))

cycle$variable <- factor(cycle$variable,levels=c("OP_mgPL","NO2_mgNL","NO3_mgNL","NH3_mgNL","Ace_mgCODL"))

# plotting -----------

nutrients <- ggplot(data=cycle,aes(x=hour,y=value)) +
  geom_point(data=subset(cycle,variable %in% c("OP_mgPL","NO2_mgNL","NO3_mgNL","NH3_mgNL")),
             aes(color=variable,shape=variable),size=2) +
  scale_color_manual(name="Constituent",
                     values=met.brewer("Juarez",4),
                     labels=c("OP","NO2","NO3","NH3")) +
  scale_shape_manual(name="Constituent",
                     values=c(15,16,17,18),
                     labels=c("OP","NO2","NO3","NH3")) +
  geom_vline(xintercept=2.65,color="grey") +
  geom_vline(xintercept=4.13,color="grey") +
  theme_half_open() + 
  ylim(0,30) +
  labs(y="Concentration [mgP/L or mgN/L]",x="Hour") +
  theme(legend.position="none")

acetate <- ggplot(data=cycle,aes(x=hour,y=value)) +
  geom_point(data=subset(cycle,variable %in% c("Ace_mgCODL")),
             aes(color=variable,shape=variable),size=2) +
  scale_color_manual(name="Constituent",
                     values=met.brewer("Cross",1),
                     labels=c("Acetate")) +
  scale_shape_manual(name="Constituent",
                     values=c(1),
                     labels=c("Acetate")) +
  geom_vline(xintercept=2.65,color="grey") +
  geom_vline(xintercept=4.13,color="grey") +
  theme_half_open() + 
  scale_y_continuous(limits=c(0,200),position="right") +
  labs(y="Concentration [mgCOD/L]",x="Hour")  +
  theme(legend.position="none")


aligned_plots <- align_plots(nutrients, acetate, align="hv", axis="tblr")
ggdraw() + draw_plot(aligned_plots[[1]]) + draw_plot(aligned_plots[[2]])
ggsave("220506_cycle.png",width=7,height=4,dpi=300,units="in")

