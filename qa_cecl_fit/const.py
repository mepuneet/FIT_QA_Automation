BANK_ID = "3279"
ALL_FILES = [
    {"file_name": "executive-overview.csv","html_id":"summary_tbl","asset_type":"loans"},    
    {"file_name": "executive-overview-loans.csv","html_id":"group_summary_tbl","asset_type":"loans"},
    {"file_name": "executive-overview-loans-details-1.csv","html_id":"tb2hover_data","asset_type":"loans","parent_id":"group_summary_tbl"},
    
    {"file_name": "executive-overview-unfunded.csv","html_id":"group_summary_tbl","asset_type":"unfunded"},
    # {"file_name": "executive-overview-unfunded-detail-1.csv","html_id":"tb2hover_data","asset_type":"unfunded","parent_id":"group_summary_tbl"},
    
    {"file_name": "executive-overview-htm.csv","html_id":"group_summary_tbl","asset_type":"htm"},
    # {"file_name": "executive-overview-htm-detail-1.csv","html_id":"tb2hover_data","asset_type":"htm","parent_id":"group_summary_tbl"},

    {"file_name": "adjustment-balance-reserve.csv","html_id":"adjustsments_tbl","asset_type":"loans"},
    {"file_name": "adjustment-balance-reserve-before-after.csv","html_id":"div_adjs_bef_after","asset_type":"loans"},

    {"file_name": "qfactor-result.csv","html_id":"div_qfactor_results","asset_type":"loans"},

    {"file_name": "forwardlook-result.csv","html_id":"div_forwardlook_bafter_tbody","asset_type":"loans"},

    # {"file_name": "override-orignal-values.csv","html_id":"div_orgnl_val","asset_type":"loans"},
    # {"file_name": "override-grade-and-balance.csv","html_id":"div_ovrride_val","asset_type":"loans"},
    {"file_name": "override-before&after-account.csv","html_id":"div_before_aftr_accnt_val","asset_type":"loans"},
    {"file_name": "override-before&after-group.csv","html_id":"div_before_aftr_accnt_val","asset_type":"loans"},

    {"file_name": "exclude-account.csv","html_id":"excludes_account_colm","asset_type":"loans"},

    {"file_name": "select-methodology-main-table.csv","html_id":"sel_met_colm","asset_type":"loans"},
    {"file_name": "select-methodology-reserve-table.csv","html_id":"res_bal_tabl","asset_type":"loans"},

    # {"file_name": "report-download","html_id":"res_bal_tabl","asset_type":"loans"},
]

# ALL_EXECUTIVE_FILES = [x for x in ALL_FILES]
ALL_EXECUTIVE_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("executive")]
ALL_ADJUSTMENT_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("adjustment")]
ALL_QFACTOR_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("qfactor")]
ALL_FORWARDLOOK_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("forwardlook")]
ALL_OVERRIDE_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("override")]
ALL_EXCLUDE_ACC_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("exclude")]
ALL_SELECT_METHOD_FILES = [x for x in ALL_FILES if x.get("file_name","").startswith("select")]

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
    RAW_FILE_PATH = "C:/Users/Puneet/Documents/Python Project/Excel_file/"

    @classmethod
    def get_skq_path(cls,bank_id):
        before_after = input("Do you want data for Before or After, If Before then press 1 : ")
        if before_after == '1': 
            return f"{cls.RAW_FILE_PATH}{bank_id}/initial_data/"
        else:
            return f"{cls.RAW_FILE_PATH}{bank_id}/after_change/"

    @classmethod
    def get_skq_screenshot_path(cls,bank_id):
        return f"{cls.get_skq_path(bank_id)}screenshots/"
    
    @classmethod
    def get_fit_path(cls,bank_id):
        return f"{cls.RAW_FILE_PATH}{bank_id}/after_change/"
    