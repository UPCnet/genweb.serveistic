*** Settings ***
Documentation    Basic tests to check whether the serveistic package is installed
Library          Selenium2Library
Resource         plone/app/robotframework/selenium.robot

*** Variables ***
${browser}         chrome
${url_homepage}    ${PLONE_URL}/

*** Test Cases ***
Homepage is shown
    Open browser           ${url_homepage}  ${browser}
    Page should contain    Plone site
    Close browser
