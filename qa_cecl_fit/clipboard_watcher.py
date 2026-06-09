from utils import write_file,get_data_from_clipboard,get_files_config
import const

def copy_data_from_clipboard(files_path):
    copied_count = 0
    for file_config in get_files_config(files_path):
        file_path = file_config.get('full_path')
        print("-"*100)
        user_input = input(f"Waiting for file: {file_path} : ")
        if user_input.lower() in ('y','1'):
            data = get_data_from_clipboard()
            if not data:
                input(f"Retry {file_config} : ")
                data = get_data_from_clipboard()
            write_file(file_path,data)
            print("Sample:\n",data[:1000])
            copied_count +=1
        else:
            print(f"Data skipped for ..{file_path}")

        print(f"Files Generated: {copied_count}")

if __name__ == "__main__":
    bank_id = input("Bank No: ")
    bank_id = const.BANK_ID if len(bank_id) < 3 else bank_id
    qa_path = const.CommonPaths.get_fit_path(bank_id)
    copy_data_from_clipboard(qa_path)