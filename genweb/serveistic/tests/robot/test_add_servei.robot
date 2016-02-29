*** Settings ***
Documentation    Servei addition-related tests

Library          Selenium2Library
Resource         plone/app/robotframework/selenium.robot
Resource         genweb/serveistic/tests/robot/keywords.robot

Test Setup       Prepare environment
Test Teardown    Close browser

*** Variables ***
${selenium_speed}   .2 seconds
${browser}          chrome

@{servei_data}      Servei de correu 
...                 Servei de correu de la UPC.
...                 Servei de correu de la UPC.
...                 Josep Tardà
...                 jtarda@upc.edu
...                 correu_upc
...                 UPCnet
...                 CNord
...                 ERP
...                 Docència i aprenentatge
 

*** Test Cases ***
Servei is created
    Given a logged user
    When servei form is submitted    @{servei_data}
    Page should contain              @{servei_data}[0]

*** Keywords ***
Prepare environment
    Set selenium speed     ${selenium_speed}
    Open browser           ${url_servei_add}  ${browser}
