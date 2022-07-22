## ---------------------------
## Script name: performance_summary
## Purpose of script: CANDO+P summarizing overall reactor performance results
## Author: McKenna Farmer
## Date Created: 2022-05-24
## ---------------------------
## Notes:
##
##
## ---------------------------

library(tidyverse)
library(readxl)
library(ggplot2)
library(MetBrewer)
library(lubridate)
library(reshape2)
library(cowplot)

file_path <- "C:/Users/mckyf/Northwestern University/Wells Research Group - CANDO+P Reactor/Operation and Logs/Performance logs"
file_name <- "cod_nutrients.xlsx"
sheet_skalar <- "nutrients_skalar"
sheet_hach <- "nutrients_hach"
sheet_cod <- "COD"

phases <- data.frame(x1=ymd("2021-05-26"),x2=ymd("2021-08-06"),
                     x3=ymd("2021-12-3"),x4=ymd("2022-04-04"),
                     x5=ymd("2022-05-24"),
                     y1=21,y2=10)

# nutrients read in and parsing  ---------
nutrients <- read_excel(file.path(file_path,file_name),sheet=sheet_skalar)
hach <- read_excel(file.path(file_path,file_name),sheet=sheet_hach)
nutrients <- rbind(nutrients,hach)

nutrients$date <- ymd(nutrients$date)
nutrients <- nutrients %>%
  mutate(phase=ifelse(date<=phases$x2,"Start up",
                      ifelse(date<=phases$x3,"I",
                      ifelse(date<=phases$x4,"II","III"))))
phos <- nutrients %>%
  subset(nutrient=="phosphate") %>%
  mutate(eff=ifelse(date<=phases$x3,(21.5-reading)*100/21.5,(10-reading)*100/8))

nox <- nutrients %>%
  subset(nutrient=="nox" | nutrient=="nitrite") %>%
  mutate(reading=ifelse(reading<0,0,reading))

# calculate NO3 - have to make wide then back to long
nox <- nox %>% dcast(date ~ nutrient, value.var="reading")
nox$nitrate <- nox$nox - nox$nitrite
nox <- nox %>% melt(id.vars="date") %>%
  rename(nutrient=variable,reading=value)

nox$nutrient <- as.factor(nox$nutrient)


# COD read in and parsing -----------
cod <- read_excel(file.path(file_path,file_name),sheet=sheet_cod)
cod$date <- ymd(cod$date)
# adding phase then parsing out values BDL
cod <- cod %>%
  mutate(phase=ifelse(date<=phases$x2,"Start up",
                      ifelse(date<=phases$x3,"I",
                      ifelse(date<=phases$x4,"II","III")))) %>%
  filter(!str_detect(reading1,"<") | !str_detect(reading2,"<")) %>%
  filter(reading1>=0)
cod$reading1 <- as.numeric(cod$reading1)
cod$reading2 <- as.numeric(cod$reading2)
cod$average <- rowMeans(cod[,3:4],na.rm=TRUE)

# plotting ----------
## OP
plt_phos <- ggplot(data=phos,aes(x=date,y=reading)) +
  geom_line(color="gray") +
  geom_point() +
  scale_x_date(breaks="2 months",date_labels="%b-%y",limits=c(phases$x1,phases$x5)) +
  theme_classic() +
  labs(y="OP [mgP/L]",x="") +
  geom_segment(data=phases,aes(x = x1, y = y1, xend = x3, yend = y1),
               color="orange",linetype="dashed") +
  geom_segment(data=phases,aes(x = x3, y = y2, xend = x5, yend = y2),
               color="darkorange3",linetype="dashed") +
  geom_vline(xintercept=phases$x2,color="chocolate4") +
  geom_vline(xintercept=phases$x3,color="chocolate4") +
  geom_vline(xintercept=phases$x4,color="chocolate4")
plt_phos
ggsave("op.tiff",height=2.5,width=6,unit="in")

## NOx
plt_nox <- ggplot(data=subset(nox,nutrient!="nitrate"),aes(x=date,y=reading,color=nutrient)) +
  geom_point() +
  geom_line(alpha=0.1) +
  scale_x_date(breaks="2 months",date_labels="%b-%y",limits=c(phases$x1,phases$x5)) +
  theme_classic() +
  labs(y="Nitrogen [mgN/L]",x="Date") +
  ylim(0,20) +
  geom_vline(xintercept=phases$x2,color="chocolate4") +
  geom_vline(xintercept=phases$x3,color="chocolate4") +
  geom_vline(xintercept=phases$x4,color="chocolate4") +
  scale_color_manual(values=met.brewer("Greek",2)) +
  theme(legend.position="none")
plt_nox
ggsave("nox_all.tiff",height=2.5,width=6,unit="in")

plt_nox_I <- ggplot(data=subset(nox,nutrient=="nitrite" & phase=="I"),aes(x=date,y=reading)) +
  geom_point() +
  geom_line(alpha=0.1) +
  scale_x_date(breaks="1 month",date_labels="%b-%y") +
  theme_classic() +
  labs(y="Nitrogen [mgN/L]",x="Date") +
  scale_color_manual(values=met.brewer("Greek",1)) +
  ylim(0,6)
plt_nox_I
ggsave("nox_I.tiff",height=2.5,width=6,unit="in")

plot_grid(plt_phos,plt_nox,nrow=2,align="hv",axis="tblr")
ggsave("phos_nox.tiff",height=4,width=6,unit="in")

## COD
plt_cod <- ggplot(data=cod,aes(x=date,y=average,color=sample)) +
  geom_point() +
  geom_line(alpha=0.1) +
  scale_x_date(breaks="2 months",date_labels="%b-%y",limits=c(phases$x1,phases$x5)) +
  theme_classic() +
  labs(y="COD [mg/L]",x="Date") +
  geom_vline(xintercept=phases$x2,color="chocolate4") +
  geom_vline(xintercept=phases$x3,color="chocolate4") +
  geom_vline(xintercept=phases$x4,color="chocolate4") +
  scale_color_manual(values=met.brewer("Greek",2)) +
  theme(legend.position="none")
plt_cod

# statistics ----------
nox %>% group_by(nutrient,phase) %>%
  summarise(median(reading,na.rm=TRUE),mean(reading,na.rm=TRUE),sd(reading,na.rm=TRUE))
phos %>% group_by(phase) %>%
  summarise(median(reading,na.rm=TRUE),mean(reading,na.rm=TRUE),sd(reading,na.rm=TRUE)) %>% as.data.frame
cod %>% group_by(sample,phase) %>%
  summarise(median(average,na.rm=TRUE),mean(average,na.rm=TRUE),sd(average,na.rm=TRUE)) %>% as.data.frame

phos %>% filter(date > ymd("2021-07-01") & date <= phases$x2) %>% summarise(median(eff))
