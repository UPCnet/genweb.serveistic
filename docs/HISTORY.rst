Changelog
=========

1.6.17 (unreleased)
-------------------

- Nothing changed yet.


1.6.16 (2019-11-06)
-------------------

* Estilos [Iago López Fernández]

1.6.15 (2019-10-10)
-------------------

* Adaptar página principal a pantallas más pequeñas [Iago López Fernández]
* Solucionar error setup_home [Iago López Fernández]

1.6.14 (2019-05-02)
-------------------

* display style fixed in Safari browser [r.ventura]

1.6.13 (2019-03-07)
-------------------

* Merge remote-tracking branch 'origin/master' into develop [Iago López Fernández]
* No reducir la imagen de cabecera [Iago López Fernández]
* Cambiar literales [Iago López Fernández]

1.6.12 (2019-02-28)
-------------------



1.6.12 (2019-02-28)
-------------------

* Add packages to install [Corina Riba]
* Imagen capcalera y capcalera_mini personalizada por el manage [Iago López Fernández]
* Estilo: Quitar redondeado en el borde del menu [Iago López Fernández]
* Colores menu - review_state [Iago López Fernández]
* viewlets.xml [Iago López Fernández]
* Centrar horizontalmente imagen cabecera [Iago López Fernández]
* Traducción [Iago López Fernández]
* Cabecera [Iago López Fernández]
* Imagen cabecera resposive + Orden portlets dispositivos tables y moviles [Iago López Fernández]
* Cabecera [Iago López Fernández]
* Estilos cabecera [Iago López Fernández]
* Resposive menu in mobile [Iago López Fernández]
* Cabecera [Iago López Fernández]
* Cabecera [root muntanyeta]
* Eliminar personalización del footer del paquete [root muntanyeta]
* Estilo titulo cabecera [iago.lopez]

1.6.11 (2018-07-10)
-------------------

* Merge remote-tracking branch 'origin/redesign' [Corina Riba]
* Nuuevos banner + Centrar titulo banner si no hay descripcion [iago.lopez]
* Estilos [iago.lopez]
* Estilo div.photoAlbumEntry [iago.lopez]

1.6.10 (2018-06-25)
-------------------

* Add oauth2client required [Corina Riba]
*  [Corina Riba]
* The new release of 'google-api-python-client' drops the hard requirement on oauth2client but it is still supported and need to be explicitly installed. [Corina Riba]

1.6.9 (2018-03-21)
------------------

* Override de la vista sitemap para mostrar solo el primer nivel [iago.lopez]
* WCAG: Etiqueta <i> utilizada para añadir iconos a <span> [iago.lopez]
* WCAG: Etiqueta <b> utilizada para añadir iconos a <span> [iago.lopez]
* WCAG: Modal login: h3 a h2 [iago.lopez]
* WCAG: añadido atributo alt en etiqueta <img> del footer [iago.lopez]

1.6.8 (2017-12-18)
------------------

* Portlet Notificacions: Mostrar enlace cuando no hay notificaciones [iago.lopez]
* Updated search input inside Servei TIC [iago.lopez]

1.6.7 (2017-11-15)
------------------

* Cambio de la estroctura de documentos al crear un ServeiTIC [iago.lopez]
* Eliminar boton de login para comentar repetido [iago.lopez]
* Updated search input inside Servei TIC [iago.lopez]
* Change literals and updated csv [iago.lopez]

1.6.6 (2017-10-02)
------------------

* Change homeupc protocol [Corina Riba]
* Afegir botó per habilitar/deshabilitar comentaris al tipus de contingut serveitic [iago.lopez]

1.6.5 (2017-02-07)
------------------



1.6.4 (2017-02-01)
------------------

* Set timeout of Problemes WS client [Santi]

1.6.3 (2017-01-24)
------------------

* Add packet to serveitic.allowed_content_types [Santi]
* Make section.allowed_types=serveitic.allowed_types [Santi]
*  [Santi]
* Sections of the nav bar showed on top of serveitic's view are [Santi]
* filtered by: [Santi]
* portal_type=serveitic.allowed_types [Santi]
* Add Link to serveitic.allowed_content_types [Santi]
* Add IDexterityTranslatable to content types [Santi]
* removed fixed version in package [Roberto Diaz]

1.6.2 (2016-12-07)
------------------

* Corregir error durant el càlcul d'indicadors [Santi]
*  [Santi]
* L'expressió regular utilitzada per comptabilitzar les visites [Santi]
* vingudes d'un servei TIC superava la llargària permesa per GA API. [Santi]
*  [Santi]
* Ara, en comptes d'utilitzar un sol filtre amb una expressió [Santi]
* composta per les URLs dels N serveis TIC, s'utilitzen N filtres, [Santi]
* cadascú amb una expressió regular composta per una sola URL. [Santi]

1.6.1 (2016-11-08)
------------------

* Afegir espai entre banners al portlet [Santi]

1.5 (2016-10-26)
----------------

* Afegir freqüència d'indicadors i altres canvis [Santi]
*  [Santi]
* - Afegir tipus i freqüència a les definicions dels indicadors. [Santi]
* - Mostrar informació de freqüència al portlet d'indicadors. [Santi]
* - Transformar ReporterException en CalculatorException quan siga [Santi]
* convenient. [Santi]
* - Legir el certificat de Google Analytics des del panell de [Santi]
* configuración en comptes de fer-lo des d'un fitxer. [Santi]
* - Corregir la situació en la qual la toolbar de l'usuari oculta [Santi]
* part del fragment d'una pàgina quan s'accedeix mitjançant una [Santi]
* URL amb #. [Santi]

1.4 (2016-09-19)
----------------

* Afegir actualització d'indicadors TIC [Santiago Cortes]
*  [Santiago Cortes]
* Afegir actualització dels indicadors: [Santiago Cortes]
* - servei-n, [Santiago Cortes]
* - visita-n-data_mes, [Santiago Cortes]
* - visita-n-data_setmana, [Santiago Cortes]
* - visita-n-data_ahir. [Santiago Cortes]
* Fer que el cercador facetat cerque per etiquetes [Santiago Cortes]
*  [Santiago Cortes]
* El cercador facetat inclou als resultats els serveis TIC que tenen [Santiago Cortes]
* etiquetes que apareixen en el text introduït en la caixa de cerca. [Santiago Cortes]
* Més informació al tiquet 688713. [Santiago Cortes]
* Millorar aspecte dels portlets [Santiago Cortes]
*  [Santiago Cortes]
* - Reestructurar portlet d'indicadors per a mostrar el valor i [Santiago Cortes]
* la descripció de l'indicador en línies diferents. [Santiago Cortes]
* - Afegir marge als portlets de problemes i notificacios. [Santiago Cortes]
* Fer els links als problemes target=_blank [Santiago Cortes]
* Add portlet touchers [Santiago Cortes]

1.3.9 (2016-09-05)
------------------

* Aplicar odre d'indicadors solament al portlet [Santiago Cortes]
*  [Santiago Cortes]
* L'ordre de visualització dels indicadors s'aplica només al portlet [Santiago Cortes]
* d'indicadors i deixa per tant d'aplicar-se a la vista de tots els [Santiago Cortes]
* indicadors. [Santiago Cortes]

1.3.8 (2016-08-31)
------------------

* Afegir ordre de visualització d'indicadors [Santiago Cortes]
*  [Santiago Cortes]
* El tipus de dades 'serveitic' defineix a través del camp [Santiago Cortes]
* 'service_indicators_order' l'ordre en el qual han de mostrar-se [Santiago Cortes]
* els indicadors dels serveis al portlet 'indicadors' i a la vista [Santiago Cortes]
* 'indicadors_list'. [Santiago Cortes]
* Afegir actualització d'indicadors [Santiago Cortes]
*  [Santiago Cortes]
* - Utilitzar API indicadors de genweb.core. [Santiago Cortes]
* - Afegir definició i actualització de l'indicador "Nombre [Santiago Cortes]
* de serveis". [Santiago Cortes]

1.3.7 (2016-07-27)
------------------

* Corregir alineació de faceted checkbox↔label [Santiago Cortes]
* Mostrar data de categoria i ocultar la d'indicador [Santiago Cortes]
* Ocultar paginació superior del cercador facetat [Santiago Cortes]
* Corregir el cercador general i altres canvis [Santiago Cortes]
*  [Santiago Cortes]
* - Treure el patch de filter_query i especificar el path de la cerca [Santiago Cortes]
* utilitzant codi JS. [Santiago Cortes]
* - Corregir la propietat CSS font-family per a mostrar sempre el [Santiago Cortes]
* mateix tipus de lletra. [Santiago Cortes]

1.3.6 (2016-07-25)
------------------

* Canviar cercador, redefinir notificació i altres [Santiago Cortes]
*  [Santiago Cortes]
* - El cercador de la part superior dreta cerca elements dins del [Santiago Cortes]
* path des d'on s'utilitza. [Santiago Cortes]
* - La vista de notificació sols mostra el cos, que es un camp de [Santiago Cortes]
* text enriquit. [Santiago Cortes]
* - La caixa de text del cercador facetat mostra per defecte "Cerca [Santiago Cortes]
* un Servei TIC" [Santiago Cortes]
* - La pàgina d'inici no mostra el títol. [Santiago Cortes]
* - L'alçada de les caixes de les facetes del cercador és menor. [Santiago Cortes]
* changed comments to <tal:comment replace="nothing"> [root@peterpre]
* Millorar README [Santiago Cortes]

1.3.5 (2016-06-20)
------------------

* Mostrar darrera modificació dels indicadors [Santiago Cortes]
*  [Santiago Cortes]
* Mostrar la data de darrera modificació de cada indicador tant al [Santiago Cortes]
* portlet d'indicadors com a la vista de tots els indicadors. [Santiago Cortes]
* Afegir tests per a Servei TIC [Santiago Cortes]

1.3.4 (2016-06-13)
------------------

* Canviar estructura de servei TIC [Santiago Cortes]
*  [Santiago Cortes]
* - Canviar l'estructura de carpetes d'un servei TIC d'acord amb la [Santiago Cortes]
* proposta del tiquet 670697. [Santiago Cortes]
* - Millorar el client del WS de Problemes per a que suporte el valor [Santiago Cortes]
* None per a username i password. [Santiago Cortes]
* - Afegir tests d'aceptació per al buscador facetat. [Santiago Cortes]

1.3.3 (2016-05-25)
------------------

* Include simplejson as requirement [Santiago Cortes]

1.3.2 (2016-05-20)
------------------

* Evitar que la reinstal·lació elimine les facetes [Santiago Cortes]

1.3.1 (2016-05-20)
------------------

* Processar respostes buides del WS d'Indicadors [Santiago Cortes]
*  [Santiago Cortes]
* - Considerar les respostes HTTP amb el cos buit com a llista [Santiago Cortes]
* JSON buida. [Santiago Cortes]

1.3 (2016-05-20)
----------------

* Millorar l'aspecte del portlet d'indicadors [Santiago Cortes]
*  [Santiago Cortes]
* - Canviar l'estructura HTML del portlet d'indicadors i també dels [Santiago Cortes]
* portlets de problemes i notificacions per a que siguen consistents. [Santiago Cortes]
* - Eliminar el prefix de les categories que comencen amb el nom del [Santiago Cortes]
* seu indicador. [Santiago Cortes]
* - Corregir els estils CSS dels formularis de creació i edició d'un [Santiago Cortes]
* Servei TIC. [Santiago Cortes]
* Corregir problemes i simplificar codi JS [Santiago Cortes]
*  [Santiago Cortes]
* - Fer que el valor dels camps de contrasenya de la secció Serveis TIC [Santiago Cortes]
* del panell de control no es perden quan es desa el formulari. [Santiago Cortes]
* - Corregir un problema amb la visualització de la versió retallada de [Santiago Cortes]
* la imatge de capçalera d'un servei. [Santiago Cortes]
* - Canviar l'estructura HTML del indicadors. [Santiago Cortes]
* - Moure el codi JavaScript a un sol fitxer i simplificar el codi JS de [Santiago Cortes]
* les plantilles HTML. [Santiago Cortes]
* Millorar el rendiment [Santiago Cortes]
*  [Santiago Cortes]
* - Mostrar una versió retallada de la imatge de capçalera [Santiago Cortes]
* de cada servei. [Santiago Cortes]
* - Eliminar una petició asíncrona a la pàgina d'inici. [Santiago Cortes]
* - Eliminar codi JavaScript no utilitzat. [Santiago Cortes]
* - Utilitzar una versió comprimida sense pèrdua de la imatge [Santiago Cortes]
* de capçalera de la pàgina d'inici. [Santiago Cortes]
* - Especificar la mida de les imatges de la barra de compartir. [Santiago Cortes]

1.2 (2016-05-04)
----------------

* Utilitzar imatges reduïdes als resultats de cerca [Santiago Cortes]
* Afegir icona RSS i altres millores [Santiago Cortes]
*  [Santiago Cortes]
* - Afegir una icona RSS al pop-up de "Comparteix" d'un servei. [Santiago Cortes]
* - Mostrar els títols dels serveis amb el seu cas natural de [Santiago Cortes]
* majúscules/minúscules. [Santiago Cortes]
* - Millorar els banners sense imatge per a que s'adapten a l'altura [Santiago Cortes]
* del seu contingut i no mostren la icona d'obrir en una pestanya nova. [Santiago Cortes]

1.1 (2016-04-26)
----------------

* Afegir portlet d'indicadors i altres millores [Santiago Cortes]
*  [Santiago Cortes]
* - Afegir el porlet d'indicadors a la vista d'un servei. [Santiago Cortes]
* - Corregir errors de codificació als Dexterity FTIs. [Santiago Cortes]
* - Afegir imatge per defecte per al resultat de cerca d'un servei. [Santiago Cortes]
* - Reestructurar la capçalera i el peu. [Santiago Cortes]
* - Afegir realm authorization al client web de problemes. [Santiago Cortes]
* - Afegir manual d'ús. [Santiago Cortes]
* - Corregir els behaviors de Notificació. [Santiago Cortes]
* - Millorar estils css. [Santiago Cortes]
* Fix carousel navigation, improve banner portlet [Santiago Cortes]
*  [Santiago Cortes]
* - Fix carousel navigation so that the next and prev links do not behave [Santiago Cortes]
* like anchor links and do not reload the page. [Santiago Cortes]
* - Add title getter to the banner portlet assignment to show the [Santiago Cortes]
* banner type on the porlets manager. [Santiago Cortes]
* - Add description to Notificació TIC Dexterity FTI. [Santiago Cortes]
* Add custom rolemap [Santiago Cortes]
* Make info-link configurable via control panel [Santiago Cortes]
*  [Santiago Cortes]
* The info icon (i) on the upper bar links now to a URL that is set on [Santiago Cortes]
* the Serveis TIC settings section of the control panel. [Santiago Cortes]

1.0 (2016-04-07)
----------------

- Initial release
