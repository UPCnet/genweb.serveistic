*** Settings ***
Documentation       Test the faceted search engine

Library             Selenium2Library
Resource            keywords.robot
Resource            keywords_faceted.robot

Suite setup          Setup environment
Suite teardown       Teardown environment

*** Variables ***
${PLONE_URL}        %{url}
${browser}          chrome
${selenium_speed}   .2 seconds
${url_base}         %{url}
${url_login}        ${url_base}/popup_login_form
${url_logout}       ${url_base}/logout
${url_homepage}     ${url_base}/ca
${url_setup}        ${url_base}/ca/test_setup
${url_teardown}     ${url_base}/ca/test_teardown

*** Test Cases ***
Homepage shows faceted search
    Given the faceted search
    Page should contain      Tipologia
    Page should contain      Àmbit
    Page should contain      Ubicació
    Page should contain      Prestador

Faceted search works with facets
    Given the faceted search
    Wait until page contains    Servei WRCX
    Page should contain         Servei WGCU
    Page should contain         Servei WGCT
    Page should contain         Servei EXLM

    When check tipologia        "Web"
    Wait until page contains    Servei WRCX
    Page should contain         Servei WGCU
    Page should contain         Servei WGCT
    Page should not contain     Servei EXLM

    When check ambit            "Gestió"
    Wait until page contains    Servei WGCU
    Page should contain         Servei WGCT
    Page should not contain     Servei WRCX
    Page should not contain     Servei EXLM

    When check ubicacio         "Manresa"
    Wait until page contains    Servei WGCU
    Page should not contain     Servei WRCX
    Page should not contain     Servei WGCT
    Page should not contain     Servei EXLM

    When check prestador        "Terrassa"
    Wait until page does not contain    Servei WGCU
    Page should not contain     Servei WRCX
    Page should not contain     Servei WGCT
    Page should not contain     Servei EXLM

    When check prestador        "UPCnet"
    Wait until page contains    Servei WGCU
    Page should not contain     Servei WRCX
    Page should not contain     Servei WGCT
    Page should not contain     Servei EXLM

    When check ubicacio         "CNord"
    Wait until page contains    Servei WGCT
    Page should contain         Servei WGCU
    Page should not contain     Servei WRCX
    Page should not contain     Servei EXLM

    When uncheck prestador      "UPCnet"
    And uncheck prestador       "Terrassa"
    And check ambit             "Recerca"
    Wait until page contains    Servei WGCT
    Page should contain         Servei WGCU
    Page should contain         Servei WRCX

    When uncheck ambit          "Recerca"
    And uncheck ambit           "Gestió"
    And check tipologia         "ERP"
    And check ubicacio          "CBLlobregat"
    And uncheck ubicacio        "CNord"
    And uncheck ubicacio        "Manresa"
    Wait until page contains    Servei EXLM
    Page should not contain     Servei WGCT
    Page should not contain     Servei WGCU
    Page should not contain     Servei WRCX

*** Keywords ***
A logged user
    Go to                  ${url_login}
    Input text             inputEmail     admin
    Input text             inputPassword  admin
    Click button           submit

Setup environment
    Set selenium speed     ${selenium_speed}
    Open browser           ${url_base}  ${browser}
    Given a logged user
    Go to                  ${url_setup}
    Go to                  ${url_logout}

Teardown environment
    Given a logged user
    Go to                  ${url_teardown}
    Go to                  ${url_logout}
    Close browser
