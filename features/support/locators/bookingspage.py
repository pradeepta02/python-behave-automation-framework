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

add_baggage_button = "XPATH,//div[@id='beforeBaggae']//button[@class='fRight action selectAddonButton']"
check_in_baggage_row = "XPATH,//span[text()='Check-In Baggage - up to $valuekg']"
add_baggage_done_button = "XPATH,//input[@class='booking mealButton button fRight']"

trip_insurance_checkbox = "ID,insurance_box"
accept_terms_and_conditions_checkbox = "ID,insurance_confirm"

continue_booking_button = "XPATH,//input[@value='Continue booking']"

i_have_cleartrip_password_checkbox = "ID,signinLabel"
password_field = "ID,password_1"

continue_button = "ID,LoginContinueBtn_1"

traveller_title_select_option = "ID,AdultTitle1"
traveller_first_name_text_field = "ID,AdultFname1"
traveller_last_name_text_field = "ID,AdultLname1"

dob_day_select_option = "ID,AdultDobDay1"
dob_month_select_option = "ID,AdultDobMonth1"
dob_year_select_option = "ID,AdultDobYear1"

nationality_text_field = "XPATH,//input[@placeholder='Nationality']"
mobile_number_text_field = "ID,mobileNumber"

traveller_continue_button = "ID,travellerBtn"

make_payment_button = "ID,paymentSubmit"
