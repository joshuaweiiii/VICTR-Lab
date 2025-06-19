import pandas as pd
import re

#The Real Seconds given to us by the Main Dataframe

mother_df = pd.read_csv("/Users/joshuawei/Downloads/VICTR Lab/Stereotype Threat Analysis/PA378 Test Data/PA378_Male_Bruce.csv")
list_secs = list(mother_df["Sec"])

realSecs = mother_df.iloc[:,[0,5]].copy()
realSecs.rename(columns = {"ID...1" : "ID", "Sec" : "Real Sec"}, inplace = True)

realSecs = realSecs.dropna(subset=["Real Sec"]).reset_index(drop=True)


#Seconds taken from the data (possibly inaccurate)

AP378 = pd.read_csv("/Users/joshuawei/Downloads/VICTR Lab/Stereotype Threat Analysis/PA378 Test Data/PA378_b_data.csv")
observedSecs = AP378.groupby("ID")['Seconds'].last().reset_index()

def extract_numeric_id(id_str):
    match = re.search(r'(\d+)', id_str)
    return int(match.group(1)) if match else None

observedSecs['Numeric_ID'] = observedSecs['ID'].apply(extract_numeric_id)
observedSecs = observedSecs[['Numeric_ID', 'Seconds']]
observedSecs.sort_values(by='Numeric_ID', inplace=True)
observedSecs.reset_index(drop=True, inplace=True)
observedSecs.rename(columns={'Numeric_ID' : 'ID','Seconds' : 'Observed Sec'}, inplace=True)

#Merge the two together removing any NAs, prioritizing Real Sec

df = pd.merge(observedSecs, realSecs, on='ID', how='left')

b_output_file_path = "/Users/joshuawei/Downloads/VICTR Lab/Stereotype Threat Analysis/PA378 Test Data/PA378b_sec_data.csv"

df.to_csv(b_output_file_path, index=False)