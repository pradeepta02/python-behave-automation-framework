# -*- coding: UTF-8 -*-


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, \
    StaleElementReferenceException, NoSuchElementException

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from utils.assertutils import Assert


class ElementAction(object):
    """Action class to perform basic operations (click, type, select ...) on webpage elements
    """
    # Element locator strategies
    locator_strategies = ['XPATH', 'ID', 'NAME', 'CLASS_NAME', 'LINK_TEXT',
                          'CSS_SELECTOR', 'PARTIAL_LINK_TEXT', 'TAG_NAME']

    def __init__(self, context):
        self.context = context

    def fetch_element(self, locator, is_list_of_elements=False, element_timeout=None):
        """Fetch the WebElement
        Find the web element based the specified locator. Before attempting to find the element,
        check if presence and visibility of it is found.
        :param locator: element locator
        :param is_list_of_elements: in case the locator returns multiple elements, set this to true
        :param element_timeout: By default webdriver will wait for the 'element_fetch_timeout' seconds defined in
        config file. It will be overridden if you specify a different timeout to this function
        :return: WebElement, raise exception in case no such element is found
        """
        strategy = locator.split(",")[0].strip()
        actual_locator = locator.replace(strategy + ",", "")

        if element_timeout is None:
            element_timeout = int(self.context.config['env']['element_fetch_timeout'])

        try:

            if strategy not in ElementAction.locator_strategies:
                raise KeyError("Unsupported locator strategy - " + strategy + "! " +
                               "Supported locator strategies are 'XPATH', 'ID', 'NAME', "
                               "'CSS_SELECTOR', 'TAG_NAME', 'LINK_TEXT' and 'PARTIAL_LINK_TEXT'")

            try:
                WebDriverWait(self.context.driver, element_timeout).until(
                    ec.visibility_of_element_located((getattr(By, strategy), actual_locator))
                )
            except(TimeoutException, StaleElementReferenceException):
                self.context.logger.error("Timed out after '" + str(element_timeout) +
                                          "' seconds waiting for element '" + str(actual_locator) +
                                          "' to be present!", exc_info=True)

            if is_list_of_elements:
                return self.context.driver.find_elements(getattr(By, strategy), actual_locator)

            try:
                element = self.context.driver.find_element(getattr(By, strategy), actual_locator)

                return element
            except TypeError:
                return False

        except NoSuchElementException:
            raise NoSuchElementException("Unable to locate element on page: {'strategy': '" +
                                         str(strategy) + "', 'locator': '" + str(actual_locator) + "'}")

    def is_element_present(self, locator, replacement=None, timeout=None):
        """Verify if element is present on page
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param timeout: By default webdriver will wait for the 'element_fetch_timeout' seconds defined in
        config.yml, It will be overridden if you specify a different timeout to this function
        :return: Boolean value specifying if element is present!
        """
        if replacement is not None:
            locator = locator.replace('$value', replacement)

        try:
            self.fetch_element(locator, False, timeout)
            return True
        except NoSuchElementException:
            return False

    def is_element_displayed(self, locator, replacement=None, timeout=None):
        """Verify if element is present on page
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param timeout: By default webdriver will wait for the 'element_fetch_timeout' seconds defined
        in config.yml. It will be overridden if you specify a different timeout to this function
        :return: Boolean value specifying if element is displayed!
        """
        if replacement is not None:
            locator = locator.replace('$value', replacement)

        try:
            if not self.fetch_element(locator, False, timeout):
                return False
            return self.fetch_element(locator, False, timeout).is_displayed()
        except Exception:
            return False

    def is_text_present(self, text):
        """Verify is text is present on webpage
        :param text: text to verify
        it will refresh the browser and try to find the element again
        :return: Boolean value specifying if text is present in webpage body
        """
        try:
            body = self.fetch_element("TAG_NAME,body")
            is_text_present_in_body = text in body.text

            if is_text_present_in_body:
                self.context.logger.info("Body contains text '" + text + "'")
            else:
                self.context.logger.info("Body does not contain text '" + text + "'")

            return is_text_present_in_body
        except Exception as e:
            self.context.logger.error("Unable to check presence of text '" + text + "' on page! Error: %s" % e,
                                      exc_info=True)
            return False

    def is_element_checked(self, locator, replacement=None, timeout=None):
        """Verify is element is checked
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param timeout: By default webdriver will wait for the 'element_fetch_timeout' seconds defined in config.yml
         It will be overridden if you specify a different timeout to this function
        :return: Boolean value specifying if element is checked!
        """
        if replacement is not None:
            locator = locator.replace('$value', replacement)

        try:
            is_element_checked = self.fetch_element(locator, False, timeout).is_selected()
            self.context.logger.info("Checked status for element '" + locator + "' is '" +
                                     str(is_element_checked) + "'")

            return is_element_checked
        except Exception as e:
            self.context.logger.error("Unable to check checked status for element '" + locator + "'. Error: %s" % e,
                                      exc_info=True)
            return False

    def click(self, locator, replacement=None, click_using_java_script=False):
        """Click on element
        :param locator: locator on which to click
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param click_using_java_script: whether to click using java script
        :return: None
        """
        if replacement:
            locator = locator.replace('$value', replacement)
        if click_using_java_script:
            _ele = self.fetch_element(locator)
            self.execute_java_script("arguments[0].click();", _ele)
            self.context.logger.info("Clicked on element '" + locator + "' using java script")
        else:
             try:
                strategy = locator.split(",")[0].strip()
                actual_locator = locator.replace(strategy + ",", "")

                timeout = int(self.context.config['env']['element_fetch_timeout'])

                WebDriverWait(self.context.driver, timeout).until(
                        ec.element_to_be_clickable((getattr(By, strategy), actual_locator))
                    )

                _ele = self.fetch_element(locator)

                if click_using_java_script:
                    self.execute_java_script("arguments[0].click();", _ele)
                else:
                    _ele.click()

                    self.context.logger.info("Clicked on element '" + locator + "'")

             except Exception as e:

                if 'safari' not in self.context.browser:
                    self.context.logger.info("Unable to click on element '" + locator +
                                             "'. Trying to click using Action Chains")

                    try:
                        element = self.fetch_element(locator)

                        actions = ActionChains(self.context.driver)
                        actions.move_to_element(element)
                        actions.click(element)
                        actions.perform()

                        self.context.logger.info("Action Chains - Clicked on element '" + locator + "'")
                    except Exception as e:
                        self.context.logger.error("Unable to click on element '" + locator + "'. Error: %s" % e,
                                                  exc_info=True)
                        Assert.assert_fail("Unable to click on element '" + locator + "'")

    def type(self, locator, text, replacement=None):
        """Type text in locator
        :param locator: locator in which to type
        :param text: text to type
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: None
        """
        if replacement:
            locator = locator.replace('$value', replacement)

        try:

            _element = self.fetch_element(locator)
            _element.clear()
            _element.send_keys(text)
            self.context.logger.info("Typed text '" + text + "' on element '" + locator + "'")
        except Exception as e:
            self.context.logger.error("Unable to type text '" + text + "' on element '" + locator + "'. Error: %s" % e,
                                      exc_info=True)
            Assert.assert_fail("Unable to type text '" + text + "' on element '" + locator + "'")

    def submit(self, locator, replacement=None):
        """Submit a form
        :param locator: input submit button
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: None
        """
        if replacement:
            locator = locator.replace('$value', replacement)

        try:
            _element = self.fetch_element(locator)
            _element.submit()
            self.context.logger.info("Submitted form'")
        except Exception as e:
            self.context.logger.error("Unable to submit form! Error: %s" % e, exc_info=True)
            Assert.assert_fail("Unable to submit form!")

    def get_text(self, locator, replacement=None):
        """Return text from locator
        :param locator: locator from which to fetch text
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: element text, None in case no text could be fetched
        """
        if replacement:
            locator = locator.replace('$value', replacement)

        try:
            element_text = self.fetch_element(locator).text
            self.context.logger.info("Get text returned '" + element_text + "' for element '" + locator + "'")

            return element_text
        except Exception as e:
            self.context.logger.error("Unable to get text from element '" + locator + "'. Error: %s" % e,
                                      exc_info=True)
            return None

    def check(self, locator, replacement=None):
        """Check element
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: None
        """
        if replacement is not None:
            locator = locator.replace('$value', replacement)

        try:
            element = self.fetch_element(locator)
            if not element.is_selected():
                element.click()
                self.context.logger.info("Checked checkbox having element '" + locator + "'")
        except Exception as e:
            self.context.logger.error("Unable to check locator '" + locator + "'. Error: %s" % e,
                                      exc_info=True)
            Assert.assert_fail("Unable to check locator '" + locator + "'")

    def uncheck(self, locator, replacement=None):
        """Uncheck element
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: None
        """
        if replacement is not None:
            locator = locator.replace('$value', replacement)

        try:
            element = self.fetch_element(locator)
            if element.is_selected():
                element.click()
                self.context.logger.info("Unchecked checkbox having element '" + locator + "'")
        except Exception as e:
            self.context.logger.error("Unable to uncheck locator '" + locator + "'. Error: %s" % e,
                                      exc_info=True)
            Assert.assert_fail("Unable to uncheck locator '" + locator + "'")

    def get_title(self):
        """Return browser title
        :return: browser title, None in case of exception
        """
        try:
            self.context.logger.info("Get title returned '" + self.context.driver.title + "'")
            return self.context.driver.title
        except Exception as e:
            self.context.logger.error("Unable to get browser title! Error: %s" % e, exc_info=True)
            return None

    def get_xpath_count(self, locator, replacement=None):
        """Uncheck element
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: length of elements matching, None in case no match found
        """
        if replacement is not None:
            locator = locator.replace('$value', replacement)

        try:
            elements = self.fetch_element(locator, is_list_of_elements=True)

            self.context.logger.info("Xpath count for element '" + locator + "', returned '" +
                                     str(len(elements)) + "'")

            return len(elements)
        except Exception as e:
            self.context.logger.error("Unable to get xpath count for locator '" + locator +
                                      "'. Error: %s" % e, exc_info=True)
            return None

    def hover(self, locator, replacement=None):
        """Mouse over on element
        :param locator: element locator
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :return: None
        """
        if replacement is not None:
            locator = locator.replace('$value', replacement)

        try:
            element = self.fetch_element(locator)

            mouse_hover = ActionChains(self.context.driver).move_to_element(element)
            mouse_hover.perform()
        except Exception as e:
            self.context.logger.error("Unable to hover on locator '" + locator + "'. Error: %s" % e,
                                      exc_info=True)
            Assert.assert_fail("Unable to hover on locator '" + locator + "'")

    def execute_java_script(self, script, element=None):
        """Execute raw java script statements
        :param script: java script to execute
        :param element: webdriver element on which to execute the java script
        :return: None
        """
        try:
            if element:
                return self.context.driver.execute_script(script, element)
            else:
                return self.context.driver.execute_script(script)
        except Exception as e:
            self.context.logger.error("Unable to execute java script '" + script + "'. Error: %s" % e,
                                     exc_info=True)
            Assert.assert_fail("Unable to execute java script '" + script + "'")

    def select_by_visible_text(self, locator, option_text, replacement=None, retry_by_browser_refresh=False):
        """Select an option by visible option text
        :param locator: locator of select element
        :param replacement: if locator contains dynamic part, i.e. '$value',
        it will be replaced by replacement variable
        :param option_text: option text by which to select the option
        :param retry_by_browser_refresh: if set to True, when webdriver is not able to find any element,
        it will refresh the browser and try to find the element again
        :return: None
        """
        if replacement:
            locator = locator.replace('$value', replacement)

        try:
            select = Select(self.fetch_element(locator))
            select.select_by_visible_text(option_text)

            self.context.logger.info("Selected element '" + locator + "' by visible text '" + option_text + "'")
        except Exception as e:
            self.context.logger.error("Unable to select option '" + option_text + "'. Error: %s" % e,
                                      exc_info=True)
            Assert.assert_fail("Unable to select option '" + option_text + "'")

    def switch_to_frame(self, frame_number, assert_it=True):
        """Switch to a frame
        :param frame_number: frame number to switch to
        :param assert_it: whether to assert switching to frame or not
        :return: None
        """
        try:
            self.context.driver.switch_to.frame(frame_number)
            self.context.logger.info("Successfully switched frame")
        except Exception as e:
            self.context.logger.info("Frame not loaded yet! Waiting for another 10 seconds for frame to load...")

            from time import sleep
            sleep(10)

            try:
                self.context.driver.switch_to.frame(frame_number)
                self.context.logger.info("Successfully switched to frame numbered '" + str(frame_number) + "'")
            except Exception as e:
                self.context.logger.error("Unable to locate frame numbered '" + str(frame_number) + "' Error: %s" % e,
                                          exc_info=True)
                if assert_it:
                    Assert.assert_fail("Unable to locate frame numbered '" + str(frame_number) + "'")

    def switch_to_default_content(self, assert_it=True):
        """Switch to parent window
        :return: None
        """
        try:
            self.context.driver.switch_to.default_content()
            self.context.logger.info("Successfully switched to default frame")
        except Exception as e:
            self.context.logger.error("Unable to switch to default content! Error: %s" % e, exc_info=True)
            if assert_it:
                Assert.assert_fail("Unable to switch to default content!")

    def press_key(self, locator, key, replacement=None):
        """Press keyboard key in locator
        :param locator: locator in which to type
        :param key: key to press
        :param replacement: this should replace the dynamic part in locator
        it will refresh the browser and try to find the element again
        :return: None
        """
        if replacement:
            locator = locator.replace('$value', replacement)

        try:
            self.fetch_element(locator).send_keys(key)
            self.context.logger.info("Pressed key '" + key + "' on element '" + locator + "'")
        except Exception as e:
            self.context.logger.error("Unable to press key '" + key + "' on element '" + locator + "'. Error: %s" % e,
                                      exc_info=True)
            Assert.assert_fail("Unable to press key '" + key + "' on element '" + locator + "'")
