*** Variables ***
${url_login}        ${PLONE_URL}/popup_login_form
${url_servei_add}   ${PLONE_URL}/++add++serveitic

*** Keywords ***
Input f_text
    [Arguments]    ${field}    ${value}
    Input text     form-widgets-${field}    ${value}

Input f_rich
    [Arguments]   ${field}   ${value}
    Select frame  id=form.widgets.${field}_ifr
    Input text    id=content   ${value}
    Unselect frame

Input f_from_to
    [Arguments]         ${field}    @{labels}
    :FOR    ${label}    IN    @{labels}
    \    Select from list by label    form-widgets-${field}-from    ${label}
    \    Click Button                 xpath=//table[@id="form-widgets-${field}"]//button[@name="from2toButton"]

A logged user
    Go to         ${url_login}
    Input text    inputEmail     admin
    Input text    inputPassword  secret
    Click button  submit

Servei form is submitted
    [Arguments]        ${title}
    ...                ${description}
    ...                ${serveiDescription}
    ...                ${responsable}
    ...                ${responsableMail}
    ...                ${product_id}
    ...                ${prestador}
    ...                ${ubicacio}
    ...                ${tipologia}
    ...                ${ambit}
    Go to              ${url_servei_add}

    Input f_text       title                ${title}
    Input f_text       description          ${description}
    Input f_rich       serveiDescription    ${serveiDescription}
    Input f_text       responsable          ${responsable}
    Input f_text       responsableMail      ${responsableMail}
    Input f_text       product_id           ${product_id}
    Input f_from_to    prestador            ${prestador}
    Input f_from_to    ubicacio             ${ubicacio}
    Input f_from_to    tipologia            ${tipologia}
    Input f_from_to    ambit                ${ambit}

    Click button    form-buttons-save
    Wait Until Page Contains Element    name=form.button.confirm
    Click button    name=form.button.confirm
