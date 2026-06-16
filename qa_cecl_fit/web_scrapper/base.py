import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment
from utils import write_file
from openpyxl.utils import get_column_letter
import pandas as pd
import os

class CommonUtils:

    def save_element(self,element,file_name,screen_shot=True,extract_df=False):

        try:
            table_html = element.get_attribute('outerHTML')        
            df = pd.read_html(table_html)[0]
            full_path = os.path.join(self.file_path, file_name)

            with pd.ExcelWriter(full_path, engine="openpyxl") as writer:
                df.to_excel(writer,sheet_name="Data",merge_cells=True)

            # Format Excel
            wb = load_workbook(full_path)
            ws = wb["Data"]
            ws.delete_cols(1)

            # Determine number of header rows
            header_rows = df.columns.nlevels   # +1 because pandas writes index header

            # Make header rows bold and centered
            for row in ws.iter_rows(min_row=1, max_row=header_rows):
                for cell in row:
                    cell.font = Font(bold=True)
                    cell.alignment = Alignment(horizontal="center",vertical="center",wrap_text=True)
            # Auto-fit column widths
            for col_num, column_cells in enumerate(ws.columns, 1):
                max_length = 0
                for cell in column_cells:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))

                ws.column_dimensions[get_column_letter(col_num)].width = max_length + 2
            # Freeze header rows
            ws.freeze_panes = f"A{header_rows + 1}"
            wb.save(full_path)
            print(f"Extracted and formatted: {full_path}")
        except Exception as e:
            print(f"Error while extracting adjustment data: {e}")

    def extract_data_by_id(self,table_id,report_name='',keep_screenshot=True,extract_as_df=False):
        self.add_delay(10)
        # WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.ID, table_id)))
        element = self.driver.find_element(By.ID,value=table_id)
        report_name = table_id if not report_name else report_name
        self.save_element(element,report_name,keep_screenshot,extract_as_df)

    def extract_data_by_xpath(self,xpath,report_name='',keep_screenshot=True,extract_as_df=False):
        self.add_delay(2)
        WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = self.driver.find_element(By.XPATH,value=xpath)
        report_name = xpath if not report_name else report_name
        self.save_element(element,report_name,keep_screenshot,extract_as_df)


    def open_webpage(self,url,web_id=None):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID, "dynamic_breadcrumb")))
        except Exception as e:
            pass

        if web_id:
            try:
                WebDriverWait(self.driver,15).until(EC.presence_of_element_located((By.ID, web_id)))
            except Exception as e:
                print(f"Web open Error {e}")

        else:
            self.add_delay(5)
        self.add_delay(3)
        print("-"*100)
        print(f"Web-page opened: {url}")

    def _generate_file_from_table(self,table_html):
        soup = BeautifulSoup(table_html,"html.parser")
        tbl_rows = soup.find_all("tr")
        rows_data = []
        for row in tbl_rows:
            tbl_cells = row.find_all("th") or row.find_all("td")
            single_rows = []
            for cell in tbl_cells:
                single_rows.append(cell.get_text())
            
            s_txt = "\t".join(single_rows)
            rows_data.append(s_txt)
        txt_file = "\n".join(rows_data)
        return txt_file

    def highlight(self,element):
        """Highlights (blinks) a Selenium Webdriver element"""
        driver = element._parent
        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                element, s)
        # original_style = element.get_attribute('style')
        apply_style("background: yellow; border: 2px solid red;")
        self.add_delay(0.5)
        # apply_style(original_style)

    def add_delay(self,n_seconds):
        print(f"........... sleeping for {n_seconds} seconds")
        time.sleep(n_seconds)


def click_n_wait(driver, button, timeout=5):
    source = driver.page_source
    button.click()
    def compare_source(driver):
        try:
            return source != driver.page_source
        except WebDriverException:
            pass
    WebDriverWait(driver, timeout).until(compare_source)