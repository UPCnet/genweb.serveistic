# -*- coding: utf-8 -*-
folder_structure = (
    (
        # title, type, exclude_from_nav, allow_discussion,
        # allowed_types,
        # layout, default_page,
        # content
        "El servei", "Folder", False, False,
        ('Document', 'File', 'Folder', 'Image'),
        'folder_index_view', None,
        (
            # title, type, exclude_from_nav, allow_discussion, allowed_types, layout,
            # description,
            # text,
            ("Descripció del servei", "Document", False, False, None, None,
                None,
                u"""<p style="text-align: center; "><strong>*** Pàgina imprescindible per publicar el servei ***</strong></p>
                    <p>Aquest apartat descriu a l’usuari el model de funcionament del servei i les seves funcionalitats. ATENCIÓ: No s'ha de confondre amb el manual de l'usuari.</p>
                    <p>Parlar  de:</p>
                    <ul>
                    <li>Com s’usa el servei (portal web, mòbil, telèfon...)</li>
                    <li>Els rols que pot prendre l’usuari</li>
                    <li>Les funcionalitats disponibles</li>
                    <li>Característiques del servei</li>
                    </ul>
                    <p style="text-align: left; ">Podeu consultar la descripció del servei de <a class="internal-link" href="resolveuid/d22f551c904b40458179e27ee115d4bb" target="_self" title="">correuUPC</a> i la <a class="internal-link" href="resolveuid/e1540bb0c5ac4f2b93615155bc7a0955" target="_blank" title="">guia d'estil</a></p>"""),

            ("Normativa", "Document", False, False, None, None,
                None,
                u"""<p style="text-align: center; "><strong>*** Pàgina imprescindible per publicar el servei ***</strong></p>
                    <p>L’apartat de normativa descriu clarament les normes d’ús del servei. Generalment  correspon a la Direcció TIC emplenar aquest apartat.</p>
                    <p>Parla de:</p>
                    <ul>
                    <li>Qui pot utilitzar el servei</li>
                    <li>Normes d'ús per als usuaris del servei</li>
                    <li>Normes d'ús per als administradors del servei i els responsables funcionals (A definir per la direcció TIC).</li>
                    <li>Compromís que adquireix l'usuari a l'utilitzar el servei</li>
                    <li>Compromís que adquireix l'administrador o el gestor del servei </li>
                    </ul>"""),

            ("Procediments", "Document", False, False, None, None,
                None,
                u"""<p style="text-align: center; "><strong>*** Pàgina imprescindible per publicar el servei ***</strong></p>
                    <p>Aquest apartat descriu tots els procediments relacionats amb el servei: Alta, baixa, modificació.</p>
                    <p>Redacta en un apartat diferent cada un dels procediments. A cada apartat parla-hi de:</p>
                    <ul>
                    <ul>
                    <li>Com es realitza</li>
                    <li>Per quin canal</li>
                    <li>A qui va dirigit</li>
                    </ul>
                    </ul>
                    <p>Els procediments han d’estar validats per la direcció TIC i els responsables funcionals i tecnològics. En alguns serveis la Normativa i els procediments s'ajunten en un apartat Normativa i procediments.</p>
                    <p> <br /><br /></p>"""),

            ("Evolució del servei", "Document", False, False, None, None,
                None,
                u"""<p>Evolució del servei. Un recull de les versions del servei (no del programari que utilitza el servei)</p>
                    <p>L'estructura d'aquest apartat ha de ser:</p>
                    <p>Una definició del model d'evolució del servei: El servei evoluciona segons el <a class="external-link" href="https://intranet.upc.edu/espaitic/ca/cetic/documents-normatius/serveis-tic-projectes" target="_self" title="">model de gestió dels projectes associats als Serveis TIC de la UPC</a>, el model descriu el mecanisme per proposar nous projectes, el cicle de vida i el sistema de gestió dels projectes. Podeu fer seguiment dels projectes d'Equips TIC a: <a class="external-link" href="https://protic.upc.edu/projects/equipstic-cataleg-d-equipament-tic-d5-4" target="_self" title="">https://protic.upc.edu/projects/equipstic-cataleg-d-equipament-tic-d5-4</a></p>
                    <p>Primer la versió futura i després les diferents versions començant per l'actual. Podeu consultar l'apartat d'evolució dels serveis de <a class="internal-link" href="resolveuid/a22d6d451c1a40738799c7c00e29d605" target="_parent" title="">correuUPC</a> i <a class="internal-link" href="resolveuid/1b0bd387d3ec4e2488c1ff257f9855b3" target="_self" title="">equipsTIC</a></p>
                    <h2>Versió futura</h2>
                    <p>Llista de les funcionalitats a desenvolupar en les pròximes versions</p>
                    <ul>
                    <li>Millora ...</li>
                    <li>Nova funcionalitat ...</li>
                    <li>Correcció de l'error ...</li>
                    <li>....</li>
                    </ul>
                    <h2 class=" ">versió (nom servei verN.nn) Data (dd-mm-aa)</h2>
                    <h4 dir="ltr">Bugs resolts</h4>
                    <ul>
                    <li>Error 1, si s'escau amb un enllaç a l'error reportat</li>
                    <li>....</li>
                    </ul>
                    <h4 dir="ltr">Millores funcionals</h4>
                    <ul>
                    <li>La cerca d'infraestructura per marca i sn accepta doble escapament de caràcters (per exemple: %2520 per un espai en blanc) per evitar conflictes amb caràcters especials</li>
                    </ul>
                    <h4>Millores de disseny</h4>
                    <h2 class=" ">versió (nom servei verN.nn) Data (dd-mm-aa)</h2>
                    <h4 dir="ltr">Bugs resolts</h4>
                    <ul>
                    <li>Error1</li>
                    <li>...</li>
                    </ul>
                    <h4 dir="ltr">Millores funcionals</h4>
                    <ul>
                    <li>Unificació dels formats acceptats pels camps dates iguals per a totes les operacions d’infraestructures: "yyyy-MM-dd </li>
                    <li>....</li>
                    </ul>
                    <h4>Millores de disseny</h4>"""),

            ("Errors coneguts", "Document", False, False, None, None,
                None,
                u"""<p>En aquest apartat es documenten els errors que es coneixen del sistema. Estructura de la pàgina</p>
                    <h3>Nom Servei-Codi error: Descripció error</h3>
                    <h4><strong>Detall de l'error:</strong></h4>
                    <p><strong></strong><span>Descripció àmplia de l'error</span></p>
                    <p> </p>
                    <h4><strong>Solució temporal:</strong> </h4>
                    <p>Si n'hi ha solució temporal al problema (ús d'un altre navegador ...)</p>
                    <h3>Nom Servei-Codi error: Descripció error</h3>"""),
        )
    ),
    (
        "Documentació", "Folder", False, False,
        ('Document', 'File', 'Folder', 'Image'),
        'folder_index_view', None,
        (
            ("Manuals", "Folder", False, False,
                ('Document', 'File', 'Folder', 'Image'),
                None, 'manual',
                (
                    ("Manual", "Document", False, False, None, None,
                        None,
                        u"""<p>La documentació conté informació de nivell funcional per tal que l'usuari entengui el funcionament del servei i pugui ser autònom en la seva utilització. Explica les funcionalitats del servei, i la seva operativa de tal manera que l'usuari sigui capaç d'utilitzar el servei encara que canviï el seu aspecte o alguna funcionalitat menor.  </p>
                            <p>Redacta un manual per cada tipus d'usuari: </p>
                            <ul>
                            <li>Manual per a l'usuari</li>
                            <li>Manual per l'administrador</li>
                            <li>Manual per l'editor</li>
                            </ul>
                            <h4>Estructura de l'apartat documentació</h4>
                            <p>Cada manual ha d'estar en una pàgina o en una carpeta si hi ha més d'una pàgina per aquest tipus d'usuari.</p>"""),
                ),
            ),

            ("Casos d'ús", "Document", False, False, None, None,
                None,
                None),
        )
    ),
    (
        "FAQ", "Folder", False, False,
        ('Document', 'File', 'Folder', 'Image'),
        'folder_index_view', None,
        (
            ("FAQ-1", "Document", False, False, None, None,
                None,
                u"""<p style="text-align: center; "><strong>******************imprescindible per publicar****************</strong></p>
                    <p>Les FAQ expliquen com realitzar les diferents tasques del servei.</p>
                    <p>Formula cada pregunta amb un sol concepte. La resposta ha de ser única.</p>
                    <p>Sigues concís amb la resposta. Escriu-la amb enumeració de passos utilitzant la negreta i els enllaços.</p>
                    <p>Si un text es repeteix diverses vegades, fes una FAQ per respondre aquesta pregunta i enllaça-ho allà on hi facis referència.</p>
                    <p>Posa com a text dels enllaços el títol complet de la secció a la qual fa referència.</p>
                    <ul>
                    <li><strong>SÍ</strong>: &lt;a&gt;Com puc trobar serveis TIC?&lt;/a&gt;</li>
                    <li><strong>NO</strong>: Per a saber com puc trobar serveis TIC &lt;a&gt;Clica aquí&lt;/a&gt;</li>
                    <li>
                    <p><strong>NO</strong>: &lt;a&gt;Aquí&lt;/a&gt; trobaràs la resposta a saber com puc trobar els serveis TIC</p>
                    </li>
                    </ul>
                    <h4>Estructura de l'apartat FAQ</h4>
                    <p>Una pàgina per FAQ, on el títol de la pàgina és la pregunta (FAQ) i en el contingut de la pàgina la resposta a la pregunta, sense títol. </p>"""),
        )
    ),
    (
        "Doc tècnica", "Folder", False, False,
        ('Document', 'File', 'Folder', 'Image'),
        'folder_index_view', None,
        (
            ("Fitxa tècnica", "Document", False, False, None, None,
                None,
                u"""<p>Apartat que conté la documentació tècnica. Els tecnicismes redirigeix-los a les FAQ. Els diferents apartat son:</p>
                    <ul>
                    <li>Fitxa tècnica: Una fitxa amb la informació tècnica de l'aplicació o aplicacions que formen el servei, (vegeu fitxa tècnica de <a class="internal-link" href="resolveuid/902ae326d66b4e3789ac2d79db10f958" target="_self" title="">correuUPC</a> o <a class="internal-link" href="resolveuid/6b8ea27b9a9e4692ab4df5d174b98132" target="_self" title="">equipsTIC</a>) 
                    <ul>
                    <li>arquitectura del sistema d'informació</li>
                    <li>tecnologia emprada</li>
                    <li>esquema tecnològic</li>
                    <li>...</li>
                    </ul>
                    </li>
                    </ul>
                    <p>En pàgines o carpetes diferents, si escau, hi haurà els apartats </p>
                    <ul>
                    <li>Documentació de referència</li>
                    <li>Enllaços</li>
                    </ul>"""),

            ("Documentació de referència", "Document", False, False, None, None,
                None,
                None),

            ("Enllaços", "Document", False, False, None, None,
                None,
                None),
        )
    ),
    (
        "Suggeriments", "Folder", False, True,
        ('Document', 'File', 'Folder'),
        None, None,
        ()
    ),
    (
        "Notificacions", "Folder", True, False,
        ('notificaciotic',),
        None, None,
        ()
    ),
    (
        "Problemes", "Folder", True, False,
        ('problema',),
        None, None,
        ()
    ),
    (
        "Banners", "BannerContainer", True, False,
        ('Banner',),
        None, None,
        (),
    )
)
