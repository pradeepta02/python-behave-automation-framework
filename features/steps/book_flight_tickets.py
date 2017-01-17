# -*- coding: UTF-8 -*-

from behave import step, given, then

from features.support.actions.loginaction import LoginAction
from features.support.actions.searchaction import SearchAction
from features.support.actions.bookingaction import BookingAction

from utils.assertutils import Assert

# ===============================================================================================
# STEP DEFINITIONS:
# ===============================================================================================


@given(u'I am logged in to cleartrip as an user')
def step_impl(context):
    # Save the references of actions and page actions object in context.scenario
    # So that We can use the same object references in other steps
    context.scenario.login_action = LoginAction(context)
    context.scenario.home_page = context.scenario.login_action.login(
        context.username, context.password)

    Assert.assert_true(context.scenario.home_page.is_user_logged_in(context.username),
                       "User '" + context.username + "' is not logged in!")


@step(u'I search for a flight with below details')
def step_impl(context):
    context.scenario.search_action = SearchAction(context)

    context.scenario.search_page = None

    for row in context.table:
        context.scenario.search_page = context.scenario.search_action.search_for_flights(row['origin'],
                                                                                         row['destination'],
                                                                                         row['departure_date'],
                                                                                         row['return_date'])


@step(u'I proceed with the booking')
def step_impl(context):
    context.scenario.bookings_page = context.scenario.search_page.click_on_book_button()
    context.scenario.bookings_action = BookingAction(context)


@step(u'I select trip insurance')
def step_impl(context):
    context.scenario.bookings_page.check_trip_insurance_checkbox()


@step(u'I accept terms and conditions')
def step_impl(context):
    context.scenario.bookings_page.check_accept_terms_and_conditions_checkbox()


@step(u'I continue with the booking')
def step_impl(context):
    context.scenario.bookings_page.click_on_continue_booking_button()


@step(u'I add traveller with below details')
def step_impl(context):
    for row in context.table:
        context.scenario.bookings_action.add_traveller_details(row['title'], row['first_name'], row['last_name'],
                                                               row['mobile_no'])


@then(u'I should be presented with payment section')
def step_impl(context):
    Assert.assert_true(context.scenario.bookings_page.is_payment_section_displayed(),
                       "Payment section is not displayed!")

