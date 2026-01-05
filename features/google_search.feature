Feature: Google Search Automation
  As a user
  I want to search for information on Google
  So that I can find relevant results

  Background:
    Given I navigate to Google

  Scenario: Search for AI keyword and validate results
    When I search for "AI"
    Then I should see search results displayed
    And the page title should contain "AI"

