Feature: Verify flight ticket booking
"""
In order to verify round trip flght ticket booking works
As an user
When I book a roundtrip ticket
I should be able to book the ticket
"""
  @smoke @flight-booking @id-xxxx
  Scenario: Book a roundtrip ticket
    """
      STEPS:

      1. Search for a flight
      2. Select the default flights selected by cleartrip
      4. Opt for trip insurance
      5. Add traveller details

      VERIFICATION: User should be presented with payment section
    """
    Given I am logged in to cleartrip as an user
    When I search for a flight with below details
    | origin | destination | departure_date | return_date |
    | BLR    | BBI         | 19-1-2017      |  21-1-2017  |

    And I proceed with the booking
    """
    Select the default flight choosen by cleartrip
    """

    And I select trip insurance
    And I accept terms and conditions

    When I continue with the booking
    And I add traveller with below details
    | title | first_name | last_name | mobile_no  |
    | Mr    | pradeepta  | swain     | 9741987623 |

    Then I should be presented with payment section