# -*- coding: UTF-8 -*-

import os
import yaml

from selenium import webdriver


class SeleniumDriverFactory(object):
    """Driver factory to provide driver for running tests on web browsers.
    Supported browsers are 'firefox', 'ie', 'chrome' and 'phantomjs'.
    """
    def __init__(self, browser='firefox', version=None, platform='windows'):
        self.browser = browser
        self.version = version
        self.platform = platform

        with open(os.getcwd() + os.path.sep + "config.yml", 'r') as ymlfile:
            self.config = yaml.load(ymlfile)

    def get_driver(self):

        if os.environ.get('use_grid'):
            use_grid = os.environ.get('use_grid')
        else:
            use_grid = self.config['env']['use_grid']

        if use_grid in [True, 'true', 'True', 'TRUE', '1']:
            if os.environ.get('selenium_grid_ip'):
                selenium_grid_ip = os.environ.get('selenium_grid_ip')
            else:
                selenium_grid_ip = self.config['env']['selenium_grid_ip']

            if os.environ.get('selenium_grid_port'):
                selenium_grid_port = os.environ.get('selenium_grid_port')
            else:
                selenium_grid_port = self.config['env']['selenium_grid_port']

            # Default platform for selenium grid
            platform_name = ''

            if 'windows' in self.platform:
                platform_name = 'VISTA'
            elif 'osx' in self.platform:
                platform_name = 'MAC'

            if 'ie' in self.browser:
                selenium_desired_capabilities = {'browserName': "internet explorer",
                                                 'version': str(self.version),
                                                 'platform': platform_name,
                                                 'javascriptEnabled': True,
                                                 'requireWindowFocus': True,
                                                 'ignoreProtectedModeSettings': True
                                                 }
            else:
                selenium_desired_capabilities = {'browserName': str(self.browser),
                                                 'version': str(self.version),
                                                 'platform': platform_name,
                                                 'javascriptEnabled': True
                                                 }

            return webdriver.Remote(
                command_executor="http://" + str(selenium_grid_ip) + ":" + str(selenium_grid_port) + "/wd/hub",
                desired_capabilities=selenium_desired_capabilities)

        else:
            # Call the method as we return it
            web_driver = getattr(self, self.browser)
            return web_driver()

    @staticmethod
    def firefox():

        import os

        profile = webdriver.FirefoxProfile()

        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', os.getcwd())
        profile.set_preference('app.update.auto', False)
        profile.set_preference('app.update.enabled', False)
        profile.set_preference('app.update.silent', False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv/xls/zip/exe/msi')
        profile.set_preference('xpinstall.signatures.required', False)

        return webdriver.Firefox(profile)

    def chrome(self):

        options = webdriver.ChromeOptions()

        if 'windows' in self.platform:
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
        if 'osx' in self.platform:
            options.add_argument("--kiosk")

        return webdriver.Chrome(chrome_options=options)

    @staticmethod
    def ie():

        dc = webdriver.DesiredCapabilities.INTERNETEXPLORER

        dc["requireWindowFocus"] = True
        dc["ignoreProtectedModeSettings"] = True
        dc["javascriptEnabled"] = True

        return webdriver.Ie(capabilities=dc)

    @staticmethod
    def phantomjs():
        return webdriver.PhantomJS()

