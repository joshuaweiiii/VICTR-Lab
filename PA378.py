import pandas as pd
import os
import re

def file_list(directory_path:str) -> list:
    list_of_names = os.listdir(directory_path)
    filtered_names = []
    for name in list_of_names:
        if name.endswith('.csv') and name.startswith("ID"):
            filtered_names.append(name)
    return filtered_names

def file_path(list_of_names: list, directory_path: str):
    list_paths = []
    for filename in list_of_names:
        filepath = os.path.join(directory_path, filename)
        list_paths.append(filepath)

    def extract_id(filename):
        match = re.search(r'IDM(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    return sorted(list_paths, key=lambda x: extract_id(os.path.basename(x)))

def into_df(list_paths:list, file_num:int):
    if file_num >= 0:
        filepath = list_paths[file_num]
        df = pd.read_csv(filepath, skiprows= 10, header = None)

        df = df.iloc[:,:3]

        filename = os.path.basename(filepath)
        id = filename[:7]

        df["Name"] = id

        return df

def name_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.insert(0, "Seconds", df.index)
    df.columns = ["Seconds", "Y-axis", "X-axis", "Z-axis", "ID"]
    return df

def main():
    directory_path = "/Users/joshuawei/Downloads/VICTR Lab/Stereotype Threat Analysis/PA378 Test Data"
    list_names = file_list(directory_path)
    list_paths = file_path(list_names, directory_path)

    a_df = []
    b_df = []

    for i in range(len(list_paths)):
        filename = os.path.basename(list_paths[i])

        if filename[6] == "a" or filename[5] == "a":
            df = into_df(list_paths, i)
            df = name_cols(df)
            a_df.append(df)
        elif filename[6] == "b" or filename[5] == "b":
            df = into_df(list_paths, i)
            df = name_cols(df)
            b_df.append(df)

    a_combined_df = pd.concat(a_df, ignore_index=True)
    b_combined_df = pd.concat(b_df, ignore_index=True)

    a_output_file_path = "/Users/joshuawei/Downloads/VICTR Lab/Stereotype Threat Analysis/PA378 Test Data/PA378_a_data.csv"
    b_output_file_path = "/Users/joshuawei/Downloads/VICTR Lab/Stereotype Threat Analysis/PA378 Test Data/PA378_b_data.csv"

    a_combined_df.to_csv(a_output_file_path, index=False)
    b_combined_df.to_csv(b_output_file_path, index=False)
main()


