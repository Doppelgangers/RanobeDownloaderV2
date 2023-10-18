from handlers import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AKnigaWebPage:

    def __init__(self, url):
        self.browser = Browser()
        self.browser.options = self.browser.create_browser_options(background_mode=True,
                                                                   hide_images=True,
                                                                   skip_wait_load_page=True,
                                                                   open_dev_tab=True)
        self._driver = self.browser.webdriver
        self._driver.get(url)
        WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'audio[src]')))

    @property
    def m3u8_link(self):
        script = "return window.performance.getEntriesByType('resource').reverse().find(item => item.name.includes('m3u8')).name"
        m3u8_link = self._driver.execute_script(script=script)
        return m3u8_link

    @property
    def html_code(self):
        return self._driver.page_source
