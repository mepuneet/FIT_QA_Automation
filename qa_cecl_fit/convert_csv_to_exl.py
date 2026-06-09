from const import ALL_FILES,CommonPaths,BANK_ID
import glob

import os
import pandas as pd

import os
import pandas as pd

def Convert_csv2excel(bank_id):
    # Get the file path (folder containing the CSV files)
    file_path = CommonPaths.get_skq_path(bank_id)

    # Define the output folder for raw Excel files
    raw_excel_folder = os.path.join(file_path, 'raw_excel')

    # Create the raw_excel folder if it doesn't exist
    if not os.path.exists(raw_excel_folder):
        os.makedirs(raw_excel_folder)
    
    # Check if the file path exists
    if not os.path.exists(file_path):
        print(f"Path {file_path} does not exist.")
        return
    
    # Loop through all files in the folder
    for file_name in os.listdir(file_path):
        full_file_path = os.path.join(file_path, file_name)

        # Make sure to skip directories and process only files
        if os.path.isfile(full_file_path):
            try:
                # Attempt to read the file assuming it's in CSV format
                df = pd.read_csv(full_file_path)

                # Save the Excel file in the raw_excel folder with the same name as the CSV file
                excel_file_name = os.path.splitext(file_name)[0] + '.xlsx'
                excel_file_path = os.path.join(raw_excel_folder, excel_file_name)

                # Convert the file to Excel
                df.to_excel(excel_file_path, index=False)

                print(f"Converted: {full_file_path} -> {excel_file_path}")
            except Exception as e:
                # If there's an error in reading the file, log it
                print(f"Failed to convert {file_name}: {e}")

if __name__ == "__main__":
    bank_id = input("Bank No: ")
    bank_id = BANK_ID if len(bank_id) < 3 else bank_id
    Convert_csv2excel(bank_id)


