from handlers import Browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SiteChecker:

    def __init__(self):
        self.browser = Browser()
        self.browser.options = self.browser.create_browser_options(background_mode=True,
                                                         hide_images=True,
                                                         skip_wait_load_page=True,
                                                         open_dev_tab=True)

    def get_akniga_page(self, url):
        script = "return window.performance.getEntriesByType('resource').reverse().find(item => item.name.includes('m3u8')).name"
        driver = self.browser.webdriver

        driver.get(url=url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'audio[src]')))

        m3u8_link = driver.execute_script(script=script)

        html = driver.page_source

        return {"m3u8": m3u8_link, "html": html}

