from dotenv import load_dotenv
import os
load_dotenv()
BANK_ID = "3279"
ALL_FILES = [
    {"file_name": "Executive-Summery.xlsx","html_id":"summary_tbl","asset_type":"loans"},    
    {"file_name": "Executive-GroupLoan.xlsx","html_id":"group_summary_tbl","asset_type":"loans"},
    # {"file_name": "Executive-GroupLoanDdetail.xlsx","html_id":"tb2hover_data","asset_type":"loans","parent_id":"group_summary_tbl"},
    
    {"file_name": "Executive-GroupUnfunded.xlsx","html_id":"group_summary_tbl","asset_type":"unfunded"},
    # {"file_name": "executive-overview-unfunded-detail-1.csv","html_id":"tb2hover_data","asset_type":"unfunded","parent_id":"group_summary_tbl"},
    
    {"file_name": "Executive-GroupHTM.xlsx","html_id":"group_summary_tbl","asset_type":"htm"},
    # {"file_name": "executive-overview-htm-detail-1.csv","html_id":"tb2hover_data","asset_type":"htm","parent_id":"group_summary_tbl"},

    {"file_name": "Adjustment-Balance&Reserve.xlsx","html_id":"adjustsments_tbl","asset_type":"loans"},
    {"file_name": "Adjustment-Before-After.xlsx","html_id":"div_adjs_bef_after","asset_type":"loans"},

    {"file_name": "Qfactor","html_id":"div_qfactor_results","asset_type":"loans"},

    {"file_name": "Forwardlook","html_id":"div_forwardlook_bafter_tbody","asset_type":"loans"},

    # {"file_name": "override-orignal-values.csv","html_id":"div_orgnl_val","asset_type":"loans"},
    # {"file_name": "override-grade-and-balance.csv","html_id":"div_ovrride_val","asset_type":"loans"},
    {"file_name": "Override-Account.xlsx","html_id":"div_before_aftr_accnt_val","asset_type":"loans"},
    {"file_name": "Override-Group.xlsx","html_id":"div_before_aftr_accnt_val","asset_type":"loans"},

    {"file_name": "Exclude-Account.xlsx","html_id":"excludes_account_colm","asset_type":"loans"},

    {"file_name": "Select-Method_Top_Table.xlsx","html_id":"sel_met_colm","asset_type":"loans"},
    {"file_name": "Select-MethodReserveTable.xlsx","html_id":"res_bal_tabl","asset_type":"loans"},

    # {"file_name": "report-download","html_id":"res_bal_tabl","asset_type":"loans"},
]

# ALL_EXECUTIVE_FILES = [x for x in ALL_FILES]
ALL_EXECUTIVE_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("Executive")]
ALL_ADJUSTMENT_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("Adjustment")]
ALL_QFACTOR_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("Qfactor")]
ALL_FORWARDLOOK_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("Forwardlook")]
ALL_OVERRIDE_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("Override")]
ALL_EXCLUDE_ACC_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("Exclude")]
ALL_SELECT_METHOD_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("Select")]

def validator(all_config):
    required_keys = ['file_name','report_id','asset_type','html_id']
    for r_c in all_config:
        for req in required_keys:
            if req not in r_c:
                print(f"{req} required",r_c)

        if "detail" in r_c.get('file_name') and 'parent_id' not in r_c:
            print("parent id required",r_c)

# validator(ALL_FILES)

class CommonPaths:
    RAW_FILE_PATH = os.getenv("RAW_FILE_PATH")

    @classmethod
    def get_cecl_path(cls,bank_id):    
        before_after = input("Do you want data for Before or After, If Before then press 1 : ")
        if before_after == '1': 
            return f"{cls.RAW_FILE_PATH}{bank_id}/initial_data/"
        else:
            return f"{cls.RAW_FILE_PATH}{bank_id}/after_change/"
    
    @classmethod
    def raw_file_path(cls,bank_id):
        return f"{cls.RAW_FILE_PATH}{bank_id}/raw_excel/"
    