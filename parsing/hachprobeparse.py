'''
CANDO+P
Parsing through Hach probe logs - daily readings and event logs
Outputs combined log of sc200 and sc1000 readings, individual event logs
9/16/21
'''
# %% set up and function definition
def hach_sc1000_dl(in_file):
    '''
    sc1000 data processing
    inputs:
        in_file - input csv directory and file name
    '''
    import csv
    import glob
    import pandas as pd

    alldata_list = [] # empty list to save results to
    header = ["date_time","do_ppm","temp_c"] # dl header
    skip_range = 21
    
    filenames = glob.glob(in_file)

    for name in filenames:
        with open(name) as f:
            reader = csv.reader(f)
            for skip in range(skip_range):
                next(reader)
            data_list = list(reader)
        for entry in data_list:
            entry = list(filter(None,entry))
            alldata_list.append(entry)
            
    df = pd.DataFrame(alldata_list,columns=header)
    
    return df

def hach_sc1000_el(in_file, out_file):
    '''
    sc1000 data processing
    inputs:
        in_file - input csv directory and file name
        out_file - output directory and file name

    '''
    import csv
    import glob
    

    alldata_list = [] # empty list to save results to
    header = ["date","event","info1","info2"] # el header
    skip_range = 18
    
    filenames = glob.glob(in_file)

    for name in filenames:
        with open(name) as f:
            reader = csv.reader(f)
            for skip in range(skip_range):
                next(reader)
            data_list = list(reader)
        for entry in data_list:
            alldata_list.append(entry)

    with open(out_file, "w", newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(header)
        writer.writerows(alldata_list)


def hach_sc200_orp(directory):
    '''
    sc200 data processing
    inputs:
        directory - input directory with *.xml specified
    outputs:
        list of lists with orp data
    '''
    import xml.etree.ElementTree as ET
    import glob

    filenames = glob.glob(directory)

    alldata_list = []

    for name in filenames:
        with open(name) as f:
            tree=ET.parse(f)

        root = tree.getroot()

        # time
        time = []
        for i in root.findall("Entry"):
            value = i.find("Time")
            time.append(value.text)
        time.pop(0) # have to remove first row because it comes up as column name
        time = [x.lstrip().rstrip() for x in time]

        # orp
        orp = []
        for child in root.findall(".//CH1"):
            value = child.find(".//Data")
            orp.append(value.text)
        orp.pop(0)
        orp = [x.lstrip().rstrip() for x in orp]

        rows = list(zip(time,orp)) # turning columns into rows for csv writing

        alldata_list.extend(rows)

    return alldata_list


def hach_sc200_ph(directory):
    '''
    sc200 data processing
    inputs:
        directory - input directory with *.xml specified
    outputs:
        list of lists with ph data
    '''
    import xml.etree.ElementTree as ET
    import glob

    filenames = glob.glob(directory)

    alldata_list = []

    for name in filenames:
        with open(name) as f:
            tree=ET.parse(f)

        root = tree.getroot()

        # time
        time = []
        for i in root.findall("Entry"):
            value = i.find("Time")
            time.append(value.text)
        time.pop(0) # have to remove first row because it comes up as column name
        time = [x.lstrip().rstrip() for x in time]

        # ph
        ph = []
        for child in root.findall(".//CH1"):
            value = child.find(".//Data")
            ph.append(value.text)
        ph.pop(0)
        ph = [x.lstrip().rstrip() for x in ph]

        temp = []
        for child in root.findall(".//CH2"):
            value = child.find(".//Data")
            temp.append(value.text)
        temp.pop(0)
        temp = [x.lstrip().rstrip() for x in temp]

        rows = list(zip(time,ph,temp)) # turning columns into rows for csv writing

        alldata_list.extend(rows)

    return alldata_list


def hach_sc200_dl(ph, orp):
    '''
    sc200 data processing
    inputs:
        directory - ph and orp list of lists from functions
    '''
    import pandas as pd

    df_ph = pd.DataFrame(ph,columns=["date_time","ph","temp"])
    df_orp = pd.DataFrame(orp,columns=["date_time","orp"])

    df = pd.merge(df_orp,df_ph)
    
    return df


def hach_sc200_el(directory, out_file):
    '''
    sc200 outlog - same base script as sc1000, skip and header built-in since its set
    inputs:
        directory - where sc200 outlog csvs are saved
        out_file - output directory and file name
    '''
    import glob
    import csv

    alldata_list = [] # empty list to save results to

    filenames = glob.glob(directory)

    for name in filenames:
        with open(name) as f:
            reader = csv.reader(f)
            for skip in range(2):
                next(reader)
            data_list = list(reader)
        for entry in data_list:
            alldata_list.append(entry)

    header = ["date_time","event","event_code","info1","info2","info3","info4"]
    with open(out_file, "w", newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerow(header)
        writer.writerows(alldata_list)

def hach_dl(sc200,sc1000,out_file):
    '''
    sc200 data processing
    inputs:
        sc200 - sc200 dataframe
        sc1000 - sc1000 dataframe
        out_file - output directory and name
    '''
    import pandas as pd

    sc200["date_time"] = sc200["date_time"].astype(str)
    sc1000["date_time"] = sc1000["date_time"].astype(str)

    df = pd.merge(sc1000,sc200,on="date_time",how="left")
    df.to_csv(out_file,index=False)     
    

# %% 9/16/21 data logs

date = "21.9.16"

sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.16\sc1000"
sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.16\sc200"

out_sc1000_el = "sc1000_el_" + date + ".csv"
out_sc200_el = "sc200_el_" + date + ".csv"

out_hach = "hach_dl_" + date + ".csv"

dir_sc1000_dl = sc1000_path + "\LDO2_142700000011_0_42_DL*.csv"
dir_sc1000_el = sc1000_path + "\LDO2_142700000011_0_42_EL*.csv"

dir_sc200_dl_orp = sc200_path + "\PH_ORP_1406C1046936_0_34_DL_*.xml"
dir_sc200_dl_ph = sc200_path + "\PH_ORP_1406C1046183_0_34_DL_*.xml"
dir_sc200_el = sc200_path + "\SC200_1409C0118449_0_39_EL_*.csv"

sc1000 = hach_sc1000_dl(dir_sc1000_dl)

orp = hach_sc200_orp(dir_sc200_dl_orp)
ph = hach_sc200_ph(dir_sc200_dl_ph)
sc200 = hach_sc200_dl(ph,orp)

hach_dl(sc200, sc1000, out_hach)

sc1000_el = hach_sc1000_el(dir_sc1000_el, out_sc1000_el)
hach_sc200_el(dir_sc200_el,out_sc200_el)
    
# %% 9/10/21 data logs

# date = "21.9.10"
# out_sc1000_dl = "sc1000_dl_" + date + ".csv"
# out_sc200_dl = "sc200_dl_" + date + ".csv"

# out_sc1000_el = "sc1000_el_" + date + ".csv"
# out_sc200_el = "sc200_el_" + date + ".csv"

# out_hach = "hach_dl_" + date + ".csv"

# sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.10\sc1000"
# sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.10\sc200"

# dir_sc1000_dl = sc1000_path + "\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = sc1000_path + "\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = sc200_path + "\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = sc200_path + "\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = sc200_path + "\SC200_1409C0118449_0_39_EL_*.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)
      
# %% 9/3/21 data logs

# date = "21.9.3"
# out_sc1000_dl = "sc1000_dl_" + date + ".csv"
# out_sc200_dl = "sc200_dl_" + date + ".csv"

# out_sc1000_el = "sc1000_el_" + date + ".csv"
# out_sc200_el = "sc200_el_" + date + ".csv"

# out_hach = "hach_dl_" + date + ".csv"

# sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.03\sc1000"
# sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.03\sc200"

# dir_sc1000_dl = sc1000_path + "\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = sc1000_path + "\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = sc200_path + "\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = sc200_path + "\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = sc200_path + "\SC200_1409C0118449_0_39_EL_*.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)
  
        
# %% 8/27/21 data logs

# date = "21.8.27"
# out_sc1000_dl = "sc1000_dl_" + date + ".csv"
# out_sc200_dl = "sc200_dl_" + date + ".csv"

# out_sc1000_el = "sc1000_el_" + date + ".csv"
# out_sc200_el = "sc200_el_" + date + ".csv"

# out_hach = "hach_dl_" + date + ".csv"

# sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.08.27\sc1000"
# sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.08.27\sc200"

# dir_sc1000_dl = sc1000_path + "\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = sc1000_path + "\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = sc200_path + "\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = sc200_path + "\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = sc200_path + "\SC200_1409C0118449_0_39_EL_*.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)

    
# %% 8/20/21 data logs

# date = "21.8.20"
# out_sc1000_dl = "sc1000_dl_" + date + ".csv"
# out_sc200_dl = "sc200_dl_" + date + ".csv"

# out_sc1000_el = "sc1000_el_" + date + ".csv"
# out_sc200_el = "sc200_el_" + date + ".csv"

# out_hach = "hach_dl_" + date + ".csv"

# sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.08.20\sc1000"
# sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.08.20\sc200"

# dir_sc1000_dl = sc1000_path + "\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = sc1000_path + "\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = sc200_path + "\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = sc200_path + "\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = sc200_path + "\SC200_1409C0118449_0_39_EL_*.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)


# %% 8/13/21 data logs

# date = "21.8.13"
# out_sc1000_dl = "sc1000_dl_" + date + ".csv"
# out_sc200_dl = "sc200_dl_" + date + ".csv"

# out_sc1000_el = "sc1000_el_" + date + ".csv"
# out_sc200_el = "sc200_el_" + date + ".csv"

# out_hach = "hach_dl_" + date + ".csv"

# sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.08.13\sc1000"
# sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.08.13\sc200"

# dir_sc1000_dl = sc1000_path + "\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = sc1000_path + "\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = sc200_path + "\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = sc200_path + "\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = sc200_path + "\SC200_1409C0118449_0_39_EL_*.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)
    
# %% 8/6/21 data logs

# date = "21.8.06"
# out_sc1000_dl = "sc1000_dl_" + date + ".csv"
# out_sc200_dl = "sc200_dl_" + date + ".csv"

# out_sc1000_el = "sc1000_el_" + date + ".csv"
# out_sc200_el = "sc200_el_" + date + ".csv"

# out_hach = "hach_dl_" + date + ".csv"

# sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.08.06\sc1000"
# sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.08.06\sc200"

# dir_sc1000_dl = sc1000_path + "\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = sc1000_path + "\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = sc200_path + "\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = sc200_path + "\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = sc200_path + "\SC200_1409C0118449_0_39_EL_*.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)
   
# %% 7/30/21 data logs
# out_sc1000_dl = "sc1000_dl_21.7.30.csv"
# out_sc200_dl = "sc200_dl_21.7.30.csv"

# out_sc1000_el = "sc1000_el_21.7.30.csv"
# out_sc200_el = "sc200_el_21.7.30.csv"

# out_hach = "hach_dl_21.7.30.csv"

# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.30\sc1000\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.30\sc1000\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.30\sc200\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.30\sc200\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.30\sc200\SC200_1409C0118449_0_39_EL_*.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)

# %% 7/23/21 data logs
# out_sc1000_dl = "sc1000_dl_21.7.23.csv"
# out_sc200_dl = "sc200_dl_21.7.23.csv"

# out_sc1000_el = "sc1000_el_21.7.23.csv"
# out_sc200_el = "sc200_el_21.7.23.csv"

# out_hach = "hach_dl_21.7.23.csv"

# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.23\sc1000\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.23\sc1000\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.23\sc200\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.23\sc200\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.23\sc200\SC200_1409C0118449_0_39_EL_*.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)

    
# %% 7/16/21 data logs
# out_sc1000_dl = "sc1000_dl_21.7.16.csv"
# out_sc200_dl = "sc200_dl_21.7.16.csv"

# out_sc1000_el = "sc1000_el_21.7.16.csv"
# out_sc200_el = "sc200_el_21.7.16.csv"

# out_hach = "hach_dl_21.7.16.csv"

# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.16\sc1000\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.16\sc1000\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.16\sc200\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.16\sc200\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.16\sc200\SC200_1409C0118449_0_39_EL_*.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)


# %% 7/9/21 data logs
# out_sc1000_dl = "sc1000_dl_21.7.9.csv"
# out_sc200_dl = "sc200_dl_21.7.9.csv"

# out_sc1000_el = "sc1000_el_21.7.9.csv"
# out_sc200_el = "sc200_el_21.7.9.csv"

# out_hach = "hach_dl_21.7.9.csv"

# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.09\sc1000\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.09\sc1000\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.09\sc200\PH_ORP_1406C1046936_0_34_DL_ 210627_ 000000.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.09\sc200\PH_ORP_1406C1046183_0_34_DL_ 210627_ 000000.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.09\sc200\SC200_1409C0118449_0_39_EL_ 210627_ 000000.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)

# %% 7/2/21 data logs
# out_sc1000_dl = "sc1000_dl_21.7.2.csv"
# out_sc200_dl = "sc200_dl_21.7.2.csv"

# out_sc1000_el = "sc1000_el_21.7.2.csv"
# out_sc200_el = "sc200_el_21.7.2.csv"

# out_hach = "hach_dl_21.7.2.csv"

# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.02\sc1000\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.02\sc1000\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.02\sc200\PH_ORP_1406C1046936_0_34_DL_ 210620_ 000000.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.02\sc200\PH_ORP_1406C1046183_0_34_DL_ 210620_ 000000.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.07.02\sc200\SC200_1409C0118449_0_39_EL_ 210620_ 000000.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)

# %% 6/25/21 data logs
# out_sc1000_dl = "sc1000_dl_21.6.25.csv"
# out_sc200_dl = "sc200_dl_21.6.25.csv"

# out_sc1000_el = "sc1000_el_21.6.25.csv"
# out_sc200_el = "sc200_el_21.6.25.csv"

# out_hach = "hach_dl_21.6.25.csv"

# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.25\sc1000\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.25\sc1000\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.25\sc200\PH_ORP_1406C1046936_0_34_DL_ 210613_ 000000.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.25\sc200\PH_ORP_1406C1046183_0_34_DL_ 210613_ 000000.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.25\sc200\SC200_1409C0118449_0_39_EL_ 210613_ 000000.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)


# %% 6/18/21 data logs
# out_sc1000_dl = "sc1000_dl_21.6.18.csv"
# out_sc200_dl = "sc200_dl_21.6.18.csv"

# out_sc1000_el = "sc1000_el_21.6.18.csv"
# out_sc200_el = "sc200_el_21.6.18.csv"

# out_hach = "hach_dl_21.6.18.csv"

# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.18\sc1000\MID00000_IID00042_SN142700000011\LDO2_142700000011_0_42_DL_210611_210618.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.18\sc1000\MID00000_IID00042_SN142700000011\LDO2_142700000011_0_42_EL_210611_210618.csv"

# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.18\sc200\PH_ORP_0_34_ORP COMBO\PH_ORP_1406C1046936_0_34_DL_ 210606_ 000000.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.18\sc200\PH_ORP_0_34_pH COMBO\PH_ORP_1406C1046183_0_34_DL_ 210606_ 000000.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.18\sc200\SC200_0_39_SC200_0000000000\SC200_1409C0118449_0_39_EL_ 210606_ 000000.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)

# %% 6/11/21 data logs
# out_sc1000_dl = "sc1000_dl_21.6.11.csv"
# out_sc200_dl = "sc200_dl_21.6.11.csv"
#
# out_sc1000_el = "sc1000_el_21.6.11.csv"
# out_sc200_el = "sc200_el_21.6.11.csv"
#
# out_hach = "hach_dl_21.6.11.csv"
#
# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.11\sc1000\MID00000_IID00042_SN142700000011\LDO2_142700000011_0_42_DL_210604_210611.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.11\sc1000\MID00000_IID00042_SN142700000011\LDO2_142700000011_0_42_EL_210604_210611.csv"
#
# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.11\sc200\PH_ORP_0_34_ORP COMBO\PH_ORP_1406C1046936_0_34_DL_ 210530_ 000000.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.11\sc200\PH_ORP_0_34_pH COMBO\PH_ORP_1406C1046183_0_34_DL_ 210530_ 000000.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.11\sc200\SC200_0_39_SC200_0000000000\SC200_1409C0118449_0_39_EL_ 210530_ 000000.csv"
#
# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)
#
# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)
#
# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)

# %% 6/4/21 data logs
# out_sc1000_dl = "sc1000_dl_21.6.4.csv"
# out_sc200_dl = "sc200_dl_21.6.4.csv"

# out_sc1000_el = "sc1000_el_21.6.4.csv"
# out_sc200_el = "sc200_el_21.6.4.csv"

# out_hach = "hach_dl_21.6.4.csv"

# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.04\sc1000\MID00000_IID00042_SN142700000011\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.04\sc1000\MID00000_IID00042_SN142700000011\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.04\sc200\PH_ORP_0_34_ORP COMBO\PH_ORP_1406C1046936_0_34_DL_ 210523_ 000000.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.04\sc200\PH_ORP_0_34_pH COMBO\PH_ORP_1406C1046183_0_34_DL_ 210523_ 000000.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.06.04\sc200\SC200_0_39_SC200_0000000000\SC200_1409C0118449_0_39_EL_ 210523_ 000000.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)

#%% 5/28/21 data logs
# out_sc1000_dl = "sc1000_dl_21.5.28.csv"
# out_sc200_dl = "sc200_dl_21.5.28.csv"

# out_sc1000_el = "sc1000_el_21.5.28.csv"
# out_sc200_el = "sc200_el_21.5.28.csv"

# out_hach = "hach_dl_21.5.28.csv"

# dir_sc1000_dl = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Raw reactor logs\21.28.5\sc1000\MID00000_IID00042_SN142700000011\LDO2_142700000011_0_42_DL_210428_210528.csv"
# dir_sc1000_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Raw reactor logs\21.28.5\sc1000\MID00000_IID00042_SN142700000011\LDO2_142700000011_0_42_EL_210428_210528.csv"

# dir_sc200_dl_orp = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Raw reactor logs\21.28.5\sc200\PH_ORP_0_34_ORP COMBO\PH_ORP_1406C1046936_0_34_DL_ 210401_ 000000.xml"
# dir_sc200_dl_ph = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Raw reactor logs\21.28.5\sc200\PH_ORP_0_34_pH COMBO\PH_ORP_1406C1046183_0_34_DL_ 210401_ 000000.xml"
# dir_sc200_el = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Raw reactor logs\21.28.5\sc200\SC200_0_39_SC200_0000000000\PH_ORP_1406C1046183_0_34_EL_ 210401_ 000000.csv"

# hach_sc1000(dir_sc1000_dl, out_sc1000_dl, 21, ["date_time","do_ppm","temp_c"])
# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# hach_sc200_dl(ph,orp,out_sc200_dl)

# hach_sc1000(dir_sc1000_el, out_sc1000_el, 18, ["date_time","event","info1","info2"])
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# hach_dl(out_sc200_dl,out_sc1000_dl, out_hach)
