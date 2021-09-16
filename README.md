# CANDO+P
## All scripts for CANDO+P bioreactor operation and analysis

---

### operation
float level switch
- python and arduino code for float level switch
- approach and code based on tutorials and code from [RobotGeek](https://create.arduino.cc/projecthub/robotgeek-projects-team/aquarium-auto-refill-with-arduino-f16cd2) and [Maker Portal](https://makersportal.com/blog/2018/2/25/python-datalogger-reading-the-serial-output-from-arduino-to-analyze-data-using-pyserial)

### parsing
Parsing data logs
hachprobeparse.py - parses Hach probe logs and saves them as csv files

### analysis
cycle_results.Rmd: produces plots for in-cycle nutrient and carbon storage data
reactor_performance.Rmd: daily/weekly reactor performance
