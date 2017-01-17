# -*- coding: UTF-8 -*-

from features.support.pageactions.basepage import BasePage

from features.support.pageactions.searchpage import SearchPage
from features.support.locators import homepage as homepage_locators

from time import sleep

from selenium.webdriver.common.keys import Keys


class HomePage(BasePage):
    """Action class to perform different actions on home page
    Usage: home_page = HomePage(context)
    home_page.type_username('pradeepta')
    """
    def __init__(self, context):
        super(HomePage, self).__init__(context)

    def select_roundtrip_radio_button(self):
        self.element_action.click(homepage_locators.round_trip_radio_button)

    def type_origin(self, origin):
        self.element_action.type(homepage_locators.from_text_field, origin)
        sleep(1)
        self.element_action.press_key(homepage_locators.from_text_field, Keys.ENTER)

    def type_destination(self, destination):
        self.element_action.type(homepage_locators.destination_text_field, destination)
        sleep(1)
        self.element_action.press_key(homepage_locators.destination_text_field, Keys.ENTER)

    def select_journey_date(self, depart_on):

        # Split the given date and form the locator to click on calendar date
        date_splitted = depart_on.split("-")

        j_date = date_splitted[0]

        # Locator month starts with 0, so when we provide journey month as 1, that means internally
        # it's converted to 0, specifying month January
        j_month = int(date_splitted[1]) - 1
        j_year = date_splitted[2]

        date_selector_td = homepage_locators.calendar_date_selector.replace\
            ("$value3", j_date).replace("$value1", j_year).replace("$value2", str(j_month))

        self.element_action.click(date_selector_td)

    def click_on_search_flights_buttton(self):
        self.element_action.click(homepage_locators.search_flights_button)
        return SearchPage(self.context)

    def is_user_logged_in(self, username):
        return self.element_action.is_element_displayed(
            homepage_locators.user_avatar_text, replacement=username)
