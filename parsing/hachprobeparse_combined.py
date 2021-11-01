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
    

# %% 10/28/21 data logs

date = "21.10.28"

sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw logs\Hach\21.10.28\sc1000"
sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw logs\Hach\21.10.28\sc200"

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

# %% 9/23/21 data logs

# date = "21.9.23"

# sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.23\sc1000"
# sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.23\sc200"

# out_sc1000_el = "sc1000_el_" + date + ".csv"
# out_sc200_el = "sc200_el_" + date + ".csv"

# out_hach = "hach_dl_" + date + ".csv"

# dir_sc1000_dl = sc1000_path + "\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = sc1000_path + "\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = sc200_path + "\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = sc200_path + "\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = sc200_path + "\SC200_1409C0118449_0_39_EL_*.csv"

# sc1000 = hach_sc1000_dl(dir_sc1000_dl)

# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# sc200 = hach_sc200_dl(ph,orp)

# hach_dl(sc200, sc1000, out_hach)

# sc1000_el = hach_sc1000_el(dir_sc1000_el, out_sc1000_el)
# hach_sc200_el(dir_sc200_el,out_sc200_el)

# %% 9/16/21 data logs

# date = "21.9.16"

# sc1000_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.16\sc1000"
# sc200_path = r"C:\Users\mckyf\Box\CANDO+P and N2O\CANDO+P Reactor 2021\Operation and Logs\Sensor logs\Raw reactor logs\Hach\21.09.16\sc200"

# out_sc1000_el = "sc1000_el_" + date + ".csv"
# out_sc200_el = "sc200_el_" + date + ".csv"

# out_hach = "hach_dl_" + date + ".csv"

# dir_sc1000_dl = sc1000_path + "\LDO2_142700000011_0_42_DL*.csv"
# dir_sc1000_el = sc1000_path + "\LDO2_142700000011_0_42_EL*.csv"

# dir_sc200_dl_orp = sc200_path + "\PH_ORP_1406C1046936_0_34_DL_*.xml"
# dir_sc200_dl_ph = sc200_path + "\PH_ORP_1406C1046183_0_34_DL_*.xml"
# dir_sc200_el = sc200_path + "\SC200_1409C0118449_0_39_EL_*.csv"

# sc1000 = hach_sc1000_dl(dir_sc1000_dl)

# orp = hach_sc200_orp(dir_sc200_dl_orp)
# ph = hach_sc200_ph(dir_sc200_dl_ph)
# sc200 = hach_sc200_dl(ph,orp)

# hach_dl(sc200, sc1000, out_hach)

# sc1000_el = hach_sc1000_el(dir_sc1000_el, out_sc1000_el)
# hach_sc200_el(dir_sc200_el,out_sc200_el)
