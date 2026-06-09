from selenium import webdriver

class ChromeDriver:

    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-webgl")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options=options)
        return driver