# -*- coding: UTF-8 -*-

from features.support.pageactions.basepage import BasePage

from features.support.pageactions.homepage import HomePage
from features.support.locators import loginpage as loginpage_locators


class LoginPage(BasePage):
    """Action class to perform different actions on home page
    Usage: home_page = HomePage(context)
    home_page.type_username('pradeepta')
    """
    def __init__(self, context):
        super(LoginPage, self).__init__(context)

    def click_on_your_trips_link(self):
        self.element_action.click(loginpage_locators.your_trips_dropdown_menu)

    def click_on_sign_in_link(self):
        self.element_action.click(loginpage_locators.signin_link)
        self.context.driver.switch_to_frame('modal_window')

    def type_username(self, username):
        self.element_action.type(loginpage_locators.username_text_field, username)

    def type_password(self, password):
        self.element_action.type(loginpage_locators.password_field, password)

    def click_on_sign_in_button(self):
        self.element_action.click(loginpage_locators.signin_button)
        self.element_action.switch_to_default_content()

        return HomePage(self.context)

