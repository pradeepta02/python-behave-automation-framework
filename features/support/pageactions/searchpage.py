# -*- coding: UTF-8 -*-

from features.support.pageactions.basepage import BasePage

from features.support.pageactions.bookingspage import BookingsPage
from features.support.locators import searchpage as searchpage_locators


class SearchPage(BasePage):
    """Action class to perform different actions on search page
    Usage: search_page = SearchPage(context)
    seach_page.click_on_book_button()
    """
    def __init__(self, context):
        super(SearchPage, self).__init__(context)

    def click_on_book_button(self):
        self.element_action.click(searchpage_locators.book_button, click_using_java_script=True)
        return BookingsPage(self.context)

