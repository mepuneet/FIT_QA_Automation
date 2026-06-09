from const import ALL_FILES,CommonPaths,BANK_ID
import pandas as pd
import glob

raw_path = CommonPaths.RAW_FILE_PATH
all_files = glob.glob(raw_path)
ff = f"{raw_path}*/fitqa/*.csv"
fq_files = glob.glob(ff)
df = pd.DataFrame({"fq":fq_files})
new_df =  df['fq'].str.split("\\",expand=True)
new_df.to_excel("fq_files1.xlsx")