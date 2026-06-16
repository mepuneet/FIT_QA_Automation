from web_scrapper.web_driver import ChromeDriver
from web_scrapper.qa_strategy import NewQAStrategy
# from web_scrapper.fit_strategy import FITQAStrategy
import const

class ContextRunner:
    def __init__(self,strategy_cls):
        self.driver = ChromeDriver.get_driver()
        self.strategy =  strategy_cls(self.driver)

    def run(self,bank_no):
        self.strategy.login()
        self.strategy.set_bank(bank_no)
        self.strategy.set_manual_delay(5)

        self._extract_executive_summary()
        self._extract_adjustment_data()
        self._extract_override_data()
        self._extract_exclude_account_data()
        self._extract_qfactor_data()
        self._extract_forwordlook_data()
        self._extract_select_methodology_data()
        # self._extract_reports()
        self._extract_in_single_file()



        self.driver.quit()

    def _extract_executive_summary(self):
        self.strategy.extract_executive_reports(const.ALL_EXECUTIVE_FILES)

    def _extract_override_data(self):
        self.strategy.extract_override_data(const.ALL_OVERRIDE_FILES)

    def _extract_adjustment_data(self):
        self.strategy.extract_adjustment_data(const.ALL_ADJUSTMENT_FILES)

    def _extract_qfactor_data(self):
        self.strategy.extract_qfactor_data(const.ALL_QFACTOR_FILES)

    def _extract_forwordlook_data(self):
        self.strategy.extract_forwordlook_data(const.ALL_FORWARDLOOK_FILES)

    def _extract_exclude_account_data(self):
        self.strategy.extract_exclude_account_data(const.ALL_QFACTOR_FILES)

    def _extract_select_methodology_data(self):
        self.strategy.extract_select_methodology_data(const.ALL_SELECT_METHOD_FILES)

    def _extract_reports(self):
        self.strategy.extract_reports(const.ALL_SELECT_METHOD_FILES)

    def _extract_in_single_file(self):
        self.strategy.extract_in_single_file()

if __name__ == "__main__":
    # TODO make folder if not exists
    # TODO FIT-QA how
    # TODO Move Report config related
    ""
    bank_id = input("Select Bank number for scrapping: ")
    bank_id = const.BANK_ID if len(bank_id) < 3 else bank_id
    cr  = ContextRunner(NewQAStrategy)
    cr.run(bank_id)
