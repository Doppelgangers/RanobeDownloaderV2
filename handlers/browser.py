from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Browser:

    def __init__(self):
        self._options = self.create_browser_options()
        self._driver = None

    @staticmethod
    def create_browser_options(background_mode: bool = False,
                               hide_images: bool = True,
                               skip_wait_load_page: bool = True,
                               open_dev_tab: bool = True
                               ) -> webdriver.ChromeOptions:

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")

        if open_dev_tab:
            options.add_argument("--auto-open-devtools-for-tabs")

        if hide_images:
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

        if background_mode:
            options.headless = True

        if skip_wait_load_page:
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "none"

        return options

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options: webdriver.ChromeOptions):
        self._options = options

    @property
    def webdriver(self) -> WebDriver:
        try:
            self._driver = webdriver.Chrome(options=self.options)
            return self._driver
        except selenium_exceptions.SessionNotCreatedException as e:
            if 'This version of ChromeDriver' in (error := e.args[0]):
                raise Exception(f'{error}, "Обновите ChromeDriver"')
        except selenium_exceptions.WebDriverException as e:
            if (error := e.args[0]) == 'unknown error: cannot find Chrome binary':
                raise selenium_exceptions.WebDriverException(f"{error}\nGoogle Chrome не найдён в пути по умолчанию\nУстановите google chrome.")
        except Exception as e:
            raise Exception("Произошла ошибка\n\n", e.args[0])
