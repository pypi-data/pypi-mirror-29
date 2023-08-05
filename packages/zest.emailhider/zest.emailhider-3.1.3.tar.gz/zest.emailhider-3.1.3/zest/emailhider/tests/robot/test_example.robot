# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s zest.emailhider -t test_example.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src zest.emailhider.testing.ZEST_EMAILHIDER_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot zest/emailhider/tests/robot/test_example.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As anonymous user I want to be able to see an email address I can see it because I have Javascript enabled.

  Given an emailhider test page
   Then I see the main email address of the website


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

an emailhider test page
  Go To  ${PLONE_URL}/test_emailhider
  Wait until page contains  zest.emailhider test page


# --- THEN -------------------------------------------------------------------

Then I see the main email address of the website
  Wait until page contains  info@example.org
