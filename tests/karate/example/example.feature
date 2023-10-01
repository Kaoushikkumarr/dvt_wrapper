@mamba
Feature: Karate hello world example
# Please refer to the Karate README (found in tests/karate/README.md) for information on getting started
  Scenario: Checking for a Hello World response object
    Given url baseUrl.service
    When method get
    Then status 200
    And match response == {"greeting": "Hello data-decoupling-automation!"}

  Scenario: Different ways of testing a Hello World response object
    * def example_response_from_file = read('example_response.json')
    * def expected_response =
  """
  {
    "greeting": "Hello data-decoupling-automation!"
  }
  """
    Given url baseUrl.service
    When method get
    Then status 200
  # Matching response object
    * match response == {"greeting": "Hello data-decoupling-automation!"}
  # Using variable to match with response
    * match response == expected_response
  # Using saved response from file to match with response
    * match response == example_response_from_file
  # Navigating json response by property to match with value
    * match response.greeting == 'Hello data-decoupling-automation!'
  # Using fuzzy matching to match that it is a string
    * match response.greeting == '#string'