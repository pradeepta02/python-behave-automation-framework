# -*- coding: UTF-8 -*-

# ----------------------------------------------------------------------------
#   SUPPORTED LOCATOR STRATEGIES:
#       * XPATH
#       * ID
#       * NAME
#       * CSS_SELECTOR
#       * TAG_NAME
#       * LINK_TEXT
#       * PARTIAL_LINK_TEXT
# ----------------------------------------------------------------------------

user_avatar_text = "XPATH,//li[@class='menuItem listMenuContainer userAccountMenuContainer']//span[text()='$value']"
round_trip_radio_button = "ID,RoundTrip"
from_text_field = "NAME,origin"
destination_text_field = "NAME,destination"

from_date = "ID,FromDate"
return_date = "ID,ReturnDate"

calendar_date_selector = "XPATH,//table[@class='calendar']//td[@data-year='$value1' and @data-month='$value2']" \
                         "/a[text()='$value3']"

search_flights_button = "ID,SearchBtn"

