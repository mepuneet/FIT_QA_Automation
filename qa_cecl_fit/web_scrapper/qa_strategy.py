from .base import CommonUtils,By
from itertools import groupby
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from const import CommonPaths
from selenium.webdriver.common.action_chains import ActionChains

class NewQAStrategy(CommonUtils):

    MAIN_URL = "http://10.2.232.163:3000/"
    EXECUTIVE_OVERVIEW = "pcbb/global/executive-overview/"
    # REPORTING_HOME = "pcbb/global/reporting-home/"
    REPORTING_HOME = "cecl/global/reporting/download/?download_type=excel&asset_type=&effective_date=&effective_date_prior=&expand_page=1"
    REPORTING_PAGE ="pcbb/global/reporting/page/"
    ADJUSTMENT_PAGE ="cecl/adjustment"
    EXCLUDE_ACC_PAGE ="cecl/adjustments/exclude-accounts/"
    OVERRIDE_PAGE ="cecl/adjustments/override/"
    QFACTOR_PAGE ="cecl/factors/qfactor/in-process?call_from=qfactor-inprocess"
    FORWARDLOOK_PAGE ="cecl/factors/forward/whatif/?call_from=forwardlookinprocess"
    SELECT_METHODOLOGY_PAGE ="cecl/review-setup/configuration/select-methodology/"
    GRAPH_PAGE ="pcbb/global/reporting/page/graph/"

    USER = "puneet_admin"
    PW = "123456789a#PCBB"

    asset_type_mapping = {"1": "Loans", "2": "HTM_Securities", "3": "Unfunded_Commitments"}
    
    def __init__(self,driver):
        self.driver = driver
        self.manual_delay = 0

    def login(self):
        self.open_webpage(self.MAIN_URL)

        self.driver.find_element(By.ID,value='email_login').send_keys(self.USER)
        self.driver.find_element(By.ID,value='password_login').send_keys(self.PW)
        self.driver.find_element(By.ID,value='btn_login').click()
        self.add_delay(5)
        print("Logged In")

    def set_manual_delay(self,sec:int):
        self.manual_delay = sec

    def set_bank(self,bank_id,manual=True):
        self.bank_id = bank_id

        self.file_path = CommonPaths.get_skq_path(bank_id)
        self.screenshots_path = CommonPaths.get_skq_screenshot_path(bank_id)

        self.driver.find_element(By.ID,value='search_institution').send_keys(self.bank_id)
        self.add_delay(1)
        if manual:
            manually_switch = input(f"waiting for user to do the task for bank {bank_id}: ")
            # select all ticks
            if manually_switch in ("1","yes"):
                print("Switched manually")


    def _open_report_page_by_id(self,report_page_id):
        if report_page_id in (6,7,8,9,10,14,24,25):
            url = f"{self.MAIN_URL}{self.GRAPH_PAGE}?reportid={report_page_id}"
        else:
            url = f"{self.MAIN_URL}{self.REPORTING_PAGE}?reportid={report_page_id}"
        self.open_webpage(url,"report_filter_date")
        self.add_delay(self.manual_delay)


    def extract_report_page(self,report_page_config):
        '''
        single report page can have multiple report

        '''
        # open report page
        report_page_id = self._get_report_page_id(report_page_config)
        self._open_report_page_by_id(report_page_id)

        grouped_assets = [list(v) for k,v in groupby(report_page_config,key= lambda x: x['asset_type'])]
        
        try:
            # once report page is opened extract all report on pages
            for grouped_asset in grouped_assets:

                asset_type = grouped_asset[0].get('asset_type','loans')
                switched = self._select_asset_type(asset_type)
                if switched:
                    for table_config in grouped_asset:
                        if not table_config.get('parent_id',''):
                            self._extract_table(table_config)
                        else:
                            self._extract_detailed_report_table(table_config)
        except Exception as e:
            print("report page error",str(e))

    def _extract_detailed_report_table(self,table_config,switch_window=True):
        try:
            self.add_delay(1)
            current_window = self.driver.current_window_handle
            parent_table_id = table_config.get('parent_id')
            # //*[@id="report_tbl_data16_2"]/tbody/tr[1]/td[1]
            # //*[@id="report_tbl_data"]/tbody/tr[1]/td[1]
            try:
                # first_cell = self.driver.find_element(By.XPATH,f'//*[@id="{parent_table_id}"]/tbody/tr[1]/td[1]')
                first_cell = self.driver.find_element(By.XPATH,f'//*[@id="{parent_table_id}"]/tbody/tr[1]/td[1]/a')
                self.highlight(first_cell)
                first_cell.click()
                print(f"Clicked on {parent_table_id} -->{first_cell.text}")
            except Exception as ee:
                first_cell = self.driver.find_element(By.XPATH,f'//*[@id="{parent_table_id}"]/tbody/tr[1]/td[1]')
                self.highlight(first_cell)
                first_cell.click()
                print(f"Clicked on {parent_table_id} -->{first_cell.text}")
            # Wait after click
            if switch_window:
                # what if window is not switched ...?
                last_window_id = self.driver.window_handles[-1]
                if current_window == last_window_id:
                    raise ValueError(f"Window not opened Unable to click id {parent_table_id}")

                self.driver.switch_to.window(self.driver.window_handles[-1])                
                self.add_delay(6)
                self._extract_table(table_config)
                self.add_delay(1)
                self.driver.close()
                self.driver.switch_to.window(current_window)
            else:
                self.driver.implicitly_wait(5) # seconds
                self._extract_table(table_config)
            self.add_delay(1)

        except Exception as e:
            print(f"Unable to extract-detail-page error: {str(e)[:100]}")

    def _get_report_page_id(self,report_page_config):
        return report_page_config[0].get('report_id')
    
    # def extract_reports(self,config):
    #     grouped_reports = [list(v) for k,v in groupby(config,key= lambda x: x['report_id'])]
    #     for rep_pg_config in grouped_reports:
    #         self.extract_report_page(rep_pg_config)

    def extract_executive_reports(self,config:list):

        # need to select details
        self.driver.find_element(By.ID,value="group_details-tab").click()
        grouped_assets = [list(v) for k,v in groupby(config,key= lambda x: x['asset_type'])]
        for grouped_asset in grouped_assets:
            asset_type = grouped_asset[0].get('asset_type','loans')
            #report_asset_type
            switched = self._select_asset_type(asset_type,options_id="slct_asset_type")
            if switched:
                for table_config in grouped_asset:
                    if not table_config.get('parent_id',''):
                        self._extract_table(table_config)
                    else:
                        self._extract_detailed_report_table(table_config,switch_window=False)

    def _extract_table(self,table_config):
        try:
            table_id = table_config.get('html_id','')
            if not table_id:
                raise ValueError("Table ID required")

            try:
                WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID, "dynamic_breadcrumb")))
                WebDriverWait(self.driver,15).until(EC.presence_of_element_located((By.ID, table_id)))

                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "loaderInternal")))
            except Exception as e:
                print(f"Table error not selected {str(e)[:30]}")

            report_name = table_config.get('file_name','')
            self.extract_data_by_id(table_id,report_name=report_name)

        except Exception as e:
            print(f"Error while extracting table: {e}")

    def _select_asset_type(self,asset_type,options_id = 'report_asset_type'):
        asst_dict = {"loans":'1',"unfunded":'3',"htm":'2'}
        got_value = asst_dict.get(asset_type,'1')
        self.driver.implicitly_wait(4) # seconds        
        select = Select(self.driver.find_element(By.ID,value=options_id))        
        selected_value = select.first_selected_option.get_attribute('value')
        available_options =  [x.get_attribute('value') for x in select.options]

        if selected_value != got_value and (got_value in available_options):
            select.select_by_value(got_value)
            print(f"Clicked to Asset-Type: {asset_type}")
            self.add_delay(5)

        elif selected_value == got_value:
            return True

        elif got_value not in available_options:
            # will be catched in above try catch
            print(f"Skipped: Asset-Type `{asset_type}` not found in options")
            return False
        return True
    
    def extract_adjustment_data(self, config: list):
        adjustment_page_url = f"{self.MAIN_URL}{self.ADJUSTMENT_PAGE}"
        self.open_webpage(adjustment_page_url)
        # Loop through the config to extract tables or data
        for table_config in config:
            try:
                table_id = table_config.get('html_id', '')
                if not table_id:
                    raise ValueError("Table ID required for extraction")

                # Wait until the table is present and the loader is invisible
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, table_id)))
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "loaderInternal")))

                # Extract data using the table ID and optional file name
                report_name = table_config.get('file_name', '')
                self.extract_data_by_id(table_id, report_name=report_name)

            except Exception as e:
                print(f"Error while extracting adjustment data: {e}")

    def extract_qfactor_data(self, config: list):
        # Step 1: Land on QFactor page
        qfactor_page_url = f"{self.MAIN_URL}{self.QFACTOR_PAGE}"
        self.open_webpage(qfactor_page_url)

        # Step 2: Click on the 'asset_type_show_hide' to navigate to the asset type selection page
        self.driver.find_element(By.ID, "asset_type_show_hide").click()
        # Step 3: Loop through the asset types and repeat the process for each one
        asset_types = ["1", "2", "3"]  # Corresponding to Loans, HTM Securities, Unfunded Commitments
        for asset_type_value in asset_types:
            try:
                # Wait for the new page to load with the asset type selection options
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "lst_financial_asset_type")))
                
                # Locate the select element
                dropdown = self.driver.find_element(By.ID, "lst_financial_asset_type")
                
                # Find and select the asset type by its value (Loans = 1, HTM Securities = 2, Unfunded Commitments = 3)
                option = dropdown.find_element(By.CSS_SELECTOR, f"option[value='{asset_type_value}']")
                
                # Perform double-click on the option to select it
                action = ActionChains(self.driver)
                action.double_click(option).perform()

                # Step 4: Submit the selected asset type (assuming there's a submit button with ID 'submit_button')
                submit_button = self.driver.find_element(By.ID, "run_document")
                submit_button.click()

                # Step 5: Wait for the QFactor page to load again after submission
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, "dynamic_breadcrumb")))
                
                # Step 6: Fetch the data as per the selected asset type
                for table_config in config:
                    try:
                        table_id = table_config.get('html_id', '')
                        if not table_id:
                            raise ValueError("Table ID required for extraction")
                        
                        # Wait for the table to appear and the loader to disappear
                        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, table_id)))
                        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "loaderInternal")))

                        # Extract data from the table using the table ID and optional file name
                        asset_type_name = self.asset_type_mapping.get(asset_type_value, "Unknown Asset Type")
                        report_name = f"{asset_type_name}-{table_config.get('file_name', '')}"
                        self.extract_data_by_id(table_id, report_name=report_name)

                    except Exception as e:
                        print(f"Error while extracting data for asset type {asset_type_value}: {e}")

                # Step 7: After processing, go back to the asset type selection page for the next asset type
                self.driver.find_element(By.ID, "asset_type_show_hide").click()

            except Exception as e:
                print(f"Error during asset type selection process for {asset_type_value}: {e}")

    def extract_forwordlook_data(self, config: list):
        # Step 1: Land on QFactor page
        forwardlook_page_url = f"{self.MAIN_URL}{self.FORWARDLOOK_PAGE}"
        self.open_webpage(forwardlook_page_url)

        # Step 2: Click on the 'asset_type_show_hide' to navigate to the asset type selection page
        self.driver.find_element(By.ID, "asset_type_show_hide").click()
        self.add_delay(10)
        # Step 3: Loop through the asset types and repeat the process for each one
        asset_types = ["1", "2", "3"]  # Corresponding to Loans, HTM Securities, Unfunded Commitments
        for asset_type_value in asset_types:
            try:
                # Wait for the new page to load with the asset type selection options
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "lst_financial_asset_type")))
                
                # Locate the select element
                dropdown = self.driver.find_element(By.ID, "lst_financial_asset_type")
                
                # Find and select the asset type by its value (Loans = 1, HTM Securities = 2, Unfunded Commitments = 3)
                option = dropdown.find_element(By.CSS_SELECTOR, f"option[value='{asset_type_value}']")
                
                # Perform double-click on the option to select it
                action = ActionChains(self.driver)
                action.double_click(option).perform()

                # Step 4: Submit the selected asset type (assuming there's a submit button with ID 'submit_button')
                submit_button = self.driver.find_element(By.ID, "run_document")
                submit_button.click()

                # Step 5: Wait for the QFactor page to load again after submission
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, "dynamic_breadcrumb")))
                
                # Step 6: Fetch the data as per the selected asset type
                for table_config in config:
                    try:
                        table_id = table_config.get('html_id', '')
                        if not table_id:
                            raise ValueError("Table ID required for extraction")
                        
                        # Wait for the table to appear and the loader to disappear
                        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, table_id)))
                        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "loaderInternal")))

                        # Extract data from the table using the table ID and optional file name
                        asset_type_name = self.asset_type_mapping.get(asset_type_value, "Unknown Asset Type")
                        report_name = f"{asset_type_name}-{table_config.get('file_name', '')}"
                        self.extract_data_by_id(table_id, report_name=report_name)

                    except Exception as e:
                        print(f"Error while extracting data for asset type {asset_type_value}: {e}")

                # Step 7: After processing, go back to the asset type selection page for the next asset type
                self.driver.find_element(By.ID, "asset_type_show_hide").click()

            except Exception as e:
                print(f"Error during asset type selection process for {asset_type_value}: {e}")

    def scroll_page(self):
        # Scroll down the page in increments until the end of the page is reached
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to the bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.add_delay(2)  # Wait for new content to load (adjust delay if needed)

            # Check the new scroll height after waiting for page load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Break the loop if no new content is loaded
            if new_height == last_height:
                break
            last_height = new_height

    def extract_override_data(self, config: list):
        override_page_url = f"{self.MAIN_URL}{self.OVERRIDE_PAGE}"
        self.open_webpage(override_page_url)
        # Loop through the config to extract tables or data
        for table_config in config:
            try:
                table_id = table_config.get('html_id', '')
                report_name = table_config.get('file_name', '')

                # if table_id in ('div_orgnl_val', 'div_ovrride_val'):
                #     self.add_delay(1)
                #     manually_switch= input("Have you scrolled data for bank")
                #     if manually_switch in ("1","yes"):
                #         print("Switched manually")
                if report_name == "override-before&after-group.csv":
                    dropdown_element = self.driver.find_element(By.ID, "rslt_before_aftr")
                    select = Select(dropdown_element)
                    select.select_by_value("grp")  #

                if not table_id:
                    raise ValueError("Table ID required for extraction")

                # Wait until the table is present and the loader is invisible
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, table_id)))
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "loaderInternal")))

                # Extract data using the table ID and optional file name
                report_name = table_config.get('file_name', '')
                self.extract_data_by_id(table_id, report_name=report_name)

            except Exception as e:
                print(f"Error while extracting adjustment data: {e}")

    def extract_exclude_account_data(self, config: list):
        exclude_page_url = f"{self.MAIN_URL}{self.EXCLUDE_ACC_PAGE}"
        self.open_webpage(exclude_page_url)

        # Scroll through the page to ensure all content is loaded
        self.scroll_page()
        for table_config in config:
            try:
                table_id = table_config.get('html_id', '')
                if table_id in ('excludes_account_colm'):
                    self.add_delay(1)
                    # manually_switch= input("Have you scrolled data for bank : ")
                    # if manually_switch in ("1","yes"):
                    #     print("Switched manually")

                if not table_id:
                    raise ValueError("Table ID required for extraction")

                # Wait until the table is present and the loader is invisible
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, table_id)))
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "loaderInternal")))

                # Extract data using the table ID and optional file name
                report_name = table_config.get('file_name', '')
                self.extract_data_by_id(table_id, report_name=report_name)

            except Exception as e:
                print(f"Error while extracting adjustment data: {e}")


    def extract_select_methodology_data(self, config: list):
        select_methodolog_page_url = f"{self.MAIN_URL}{self.SELECT_METHODOLOGY_PAGE}"
        self.open_webpage(select_methodolog_page_url)
        for table_config in config:
            try:
                table_id = table_config.get('html_id', '')
                if not table_id:
                    raise ValueError("Table ID required for extraction")

                # Wait until the table is present and the loader is invisible
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, table_id)))
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "loaderInternal")))

                # Extract data using the table ID and optional file name
                report_name = table_config.get('file_name', '')
                self.extract_data_by_id(table_id, report_name=report_name)

            except Exception as e:
                print(f"Error while extracting adjustment data: {e}")

    def extract_reports(self, config: list):
        report_page_url = f"{self.MAIN_URL}{self.REPORTING_HOME}"
        self.open_webpage(report_page_url)

        # Wait for the checkboxes to load and get all checkboxes with class "selected_report"
        checkboxes = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "selected_report"))
        )
        
        # Iterate over all checkboxes and check each one
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                checkbox.click()

        download_button = self.driver.find_element(By.CLASS_NAME, "download_reports")
        download_button.click()
        self.add_delay(500)