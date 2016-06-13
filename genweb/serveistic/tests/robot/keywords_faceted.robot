*** Variables ***
${url_faceted_search}    ${PLONE_URL}/ca

*** Keywords ***
The faceted search
    Go to                  ${url_faceted_search}

Check tipologia
    [Arguments]    ${facet_value}
    ${id} =        set variable if
    ...            ${facet_value} == "Web"    c5_web
    ...            ${facet_value} == "ERP"    c5_erp
    ...            ${facet_value} == "Gestor continguts"    c5_gestor-continguts
    ...            ${facet_value} == "Eines comunicació"    c5_eines-comunicacia3
    ...            ${facet_value} == "Eines usuari"         c5_eines-usuari
    ...            ${facet_value} == "Ofimàtica"            c5_ofima-tica
    ...            ${facet_value} == "Càlcul"               c5_ca-lcul
    Select checkbox        id=${id}
    Sleep                  1s

Uncheck tipologia
    [Arguments]    ${facet_value}
    ${id} =        set variable if
    ...            ${facet_value} == "Web"    c5_web
    ...            ${facet_value} == "ERP"    c5_erp
    ...            ${facet_value} == "Gestor continguts"    c5_gestor-continguts
    ...            ${facet_value} == "Eines comunicació"    c5_eines-comunicacia3
    ...            ${facet_value} == "Eines usuari"         c5_eines-usuari
    ...            ${facet_value} == "Ofimàtica"            c5_ofima-tica
    ...            ${facet_value} == "Càlcul"               c5_ca-lcul
    Unselect checkbox      id=${id}
    Sleep                  1s

Check ambit
    [Arguments]    ${facet_value}
    ${id} =        set variable if
    ...            ${facet_value} == "Recerca"                    c4_recerca
    ...            ${facet_value} == "Docència i aprenentatge"    c4_docancia-i-aprenentatge
    ...            ${facet_value} == "Gestió"                     c4_gestia3
    ...            ${facet_value} == "Lloc de treball/eines usuari"  c4_lloc-de-treball-eines-usuari
    ...            ${facet_value} == "Estratègia i planificació"   c4_estratagia-i-planificacia3
    ...            ${facet_value} == "Infraestructures"            c4_infraestructures
    Select checkbox        id=${id}
    Sleep                  1s

Uncheck ambit
    [Arguments]    ${facet_value}
    ${id} =        set variable if
    ...            ${facet_value} == "Recerca"                    c4_recerca
    ...            ${facet_value} == "Docència i aprenentatge"    c4_docancia-i-aprenentatge
    ...            ${facet_value} == "Gestió"                     c4_gestia3
    ...            ${facet_value} == "Lloc de treball/eines usuari"  c4_lloc-de-treball-eines-usuari
    ...            ${facet_value} == "Estratègia i planificació"   c4_estratagia-i-planificacia3
    ...            ${facet_value} == "Infraestructures"            c4_infraestructures
    Unselect checkbox      id=${id}
    Sleep                  1s

Check ubicacio
    [Arguments]    ${facet_value}
    ${id} =        set variable if
    ...            ${facet_value} == "CNord"         c6_cnord
    ...            ${facet_value} == "CSud"          c6_csud
    ...            ${facet_value} == "Terrassa"      c6_terrassa
    ...            ${facet_value} == "Vilanova"      c6_vilanova
    ...            ${facet_value} == "Manresa"       c6_manresa
    ...            ${facet_value} == "CBLlobregat"   c6_cbllobregat
    Select checkbox        id=${id}
    Sleep                  1s

Uncheck ubicacio
    [Arguments]    ${facet_value}
    ${id} =        set variable if
    ...            ${facet_value} == "CNord"         c6_cnord
    ...            ${facet_value} == "CSud"          c6_csud
    ...            ${facet_value} == "Terrassa"      c6_terrassa
    ...            ${facet_value} == "Vilanova"      c6_vilanova
    ...            ${facet_value} == "Manresa"       c6_manresa
    ...            ${facet_value} == "CBLlobregat"   c6_cbllobregat
    Unselect checkbox      id=${id}
    Sleep                  1s

Check prestador
    [Arguments]    ${facet_value}
    ${id} =        set variable if
    ...            ${facet_value} == "UPCnet"        c3_upcnet
    ...            ${facet_value} == "Terrassa"      c3_terrassa
    ...            ${facet_value} == "Movistar"      c3_movistar
    Select checkbox        id=${id}
    Sleep                  1s

Uncheck prestador
    [Arguments]    ${facet_value}
    ${id} =        set variable if
    ...            ${facet_value} == "UPCnet"        c3_upcnet
    ...            ${facet_value} == "Terrassa"      c3_terrassa
    ...            ${facet_value} == "Movistar"      c3_movistar
    Unselect checkbox      id=${id}
    Sleep                  1s
