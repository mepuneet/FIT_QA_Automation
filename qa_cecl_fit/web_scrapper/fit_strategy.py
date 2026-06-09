from .base import CommonUtils,By
from itertools import groupby
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from const import CommonPaths

class FITQAStrategy(CommonUtils):

    MAIN_URL = "https://fitqa.pcbb.com/MicroStrategy/asp/Main.aspx"

    EXECUTIVE_OVERVIEW = "pcbb/global/executive-overview/"
    REPORTING_HOME = "pcbb/global/reporting-home/"
    REPORTING_PAGE ="pcbb/global/reporting/page/"
    GRAPH_PAGE ="pcbb/global/reporting/page/graph/"

    # USER = "User"
    # PW = "12345678a#"
    # //*[@id="mstr529"]/table
    def __init__(self,driver):
        self.driver = driver

    def login(self):
        self.open_webpage(self.MAIN_URL)

        # self.driver.find_element(By.ID,value='email_login').send_keys(self.USER)
        # self.driver.find_element(By.ID,value='password_login').send_keys(self.PW)
        # self.driver.find_element(By.ID,value='btn_login').click()
        input("After Login Please Enter")
        print("Logged In")

    def set_bank(self,bank_id,manual=True):
        self.bank_id = bank_id
        self.file_path = CommonPaths.get_fit_path(bank_id)
        self.screenshots_path = CommonPaths.get_fit_screenshot_path(bank_id)

        if manual:
            manually_switch = input(f"waiting for user to do the task for bank {bank_id}: ")
            # select all ticks
            if manually_switch in ("1","yes"):
                print("Switched manually")


    def _open_report_page_by_id(self,report_page_id):...
    def extract_report_page(self,report_page_config):
        '''
        single report page can have multiple report

        '''
        pass

    def _extract_detailed_report_table(self,table_config,switch_window=True):
        try:
            current_window = self.driver.current_window_handle
            parent_table_id = table_config.get('parent_id')
            # //*[@id="report_tbl_data16_2"]/tbody/tr[1]/td[1]
            # print(first_cell.get_attribute('outerHTML'))
            try:
                first_cell = self.driver.find_element(By.XPATH,f'//*[@id="{parent_table_id}"]/tbody/tr[1]/td[1]')
                self.highlight(first_cell)
                first_cell.click()
                print(f"Clicked on {parent_table_id} -->{first_cell.text}")
            except Exception as ee:
                first_cell = self.driver.find_element(By.XPATH,f'//*[@id="{parent_table_id}"]/tbody/tr[1]/td[1]/a')
                self.highlight(first_cell)
                first_cell.click()
                print(f"Clicked on {parent_table_id} -->{first_cell.text}")

            self.add_delay(3)

            # Wait after click
            if switch_window:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.add_delay(6)
                self._extract_table(table_config)
                self.add_delay(1)
                self.driver.close()
                self.driver.switch_to.window(current_window)
            else:
                self._extract_table(table_config)
            self.add_delay(1)

        except Exception as e:
            print(f"Unable to extract-detail-page error: {str(e)[:100]}")

    def _get_report_page_id(self,report_page_config):
        return report_page_config[0].get('report_id')
    
    def extract_reports(self,config):
        grouped_reports = [list(v) for k,v in groupby(config,key= lambda x: x['report_id'])]
        for rep_pg_config in grouped_reports:
            self.extract_report_page(rep_pg_config)

    def extract_executive_reports(self,config:list):
        breakpoint()
        self.extract_data_by_xpath('//*[@id="mstr529"]/table','test.csv')



    def _extract_table(self,table_config):
        try:
            table_id = table_config.get('html_id','')
            if not table_id:
                raise ValueError("Table ID required")

            WebDriverWait(self.driver,8).until(EC.presence_of_element_located((By.ID, table_id)))
            report_name = table_config.get('file_name','')
            self.extract_data_by_id(table_id,report_name=report_name)

        except Exception as e:
            print(f"Error while extracting table: {e}")

    def _select_asset_type(self,asset_type,options_id = 'report_asset_type'):

        asst_dict = {"loans":'1',"unfunded":'3',"htm":'2'}
        got_value = asst_dict.get(asset_type,'1')
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
