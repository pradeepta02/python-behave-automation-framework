# -*- coding: UTF-8 -*-

from features.support.pageactions.bookingspage import BookingsPage


class BookingAction(object):
    """Action class to perform operations related to booking flights
    """
    def __init__(self, context):
        self.context = context
        self.bookings_page = BookingsPage(context)

    def add_traveller_details(self, salutation, first_name, last_name, mobile_number):
        """Add traveller information to the booking
        :param salutation: Mr/Mrs/Ms
        :param first_name: First name
        :param last_name: Last name
        :param mobile_number: Contact number
        :return: None
        """
        self.bookings_page.select_traveller_title(salutation)
        self.bookings_page.type_traveller_first_name(first_name)
        self.bookings_page.type_traveller_last_name(last_name)

        self.bookings_page.type_mobile_number(mobile_number)

        self.bookings_page.click_on_traveller_continue_button()


