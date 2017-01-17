# -*- coding: UTF-8 -*-

from features.support.pageactions.homepage import HomePage


class SearchAction(object):
    """Action class to perform oprations related to searching flights
    """
    def __init__(self, context):
        self.context = context
        self.home_page = HomePage(self.context)

    def search_for_flights(self, origin, destination, from_date, to_date, trip_type='round_trip'):
        """Search for a flight
        :param origin: Origin city
        :param destination: Destination city
        :param from_date: Travelling Date
        :param to_date: Return Date
        :param trip_type: Whether 'oneway' or 'roundtrip'
        :return: None
        """

        # Currently only implemented to select roundtrip.
        # TO-DO: for one-way trip implement page function to select one-way trip
        if 'round_trip' in trip_type:
            self.home_page.select_roundtrip_radio_button()

        self.home_page.type_origin(origin)
        self.home_page.type_destination(destination)
        self.home_page.select_journey_date(from_date)
        self.home_page.select_journey_date(to_date)

        return self.home_page.click_on_search_flights_buttton()


