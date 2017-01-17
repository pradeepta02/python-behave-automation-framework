# -*- coding: UTF-8 -*-

from features.support.pageactions.basepage import BasePage

from features.support.locators import bookingspage as bookingspage_locators


class BookingsPage(BasePage):
    """Action class to perform different actions on bookings page
    Usage: bookings_page = BookingsPage(context)
    bookings_page.select_baggage_size('20')
    """
    def __init__(self, context):
        super(BookingsPage, self).__init__(context)

    def click_on_add_baggage_button(self):
        self.element_action.click(bookingspage_locators.add_baggage_button)

    def select_baggage_size(self, size):
        self.element_action.click(bookingspage_locators.check_in_baggage_row,
                                  replacement=size)

    def click_on_add_baggage_done_button(self):
        self.element_action.click(bookingspage_locators.add_baggage_done_button)

    def check_trip_insurance_checkbox(self):
        self.element_action.check(bookingspage_locators.trip_insurance_checkbox)

    def check_accept_terms_and_conditions_checkbox(self):
        self.element_action.check(bookingspage_locators.accept_terms_and_conditions_checkbox)

    def click_on_continue_booking_button(self):
        self.element_action.click(bookingspage_locators.continue_booking_button)

    def select_traveller_title(self, title):
        self.element_action.select_by_visible_text(
            bookingspage_locators.traveller_title_select_option, title)

    def type_traveller_first_name(self, first_name):
        self.element_action.type(
            bookingspage_locators.traveller_first_name_text_field, first_name)

    def type_traveller_last_name(self, last_name):
        self.element_action.type(
            bookingspage_locators.traveller_last_name_text_field, last_name)

    def type_mobile_number(self, mobile_number):
        self.element_action.type(bookingspage_locators.mobile_number_text_field, mobile_number)

    def click_on_traveller_continue_button(self):
        self.element_action.click(bookingspage_locators.traveller_continue_button)

    def is_payment_section_displayed(self):
        return self.element_action.is_element_displayed(bookingspage_locators.make_payment_button)
