# -*- coding: utf-8 -*-

folder_structure = (
    (
        # title, type, exclude_from_nav, allowed_types
        "El servei", "Folder", False, ('Document', 'File', 'Folder'),
        (
            # title, type, exclude_from_nav, allow_discussion, allowed_types
            ("Descripció del servei", "Document", False, False),
            ("Normativa", "Document", False, False),
            ("Procediments", "Document", False, False),
            ("Evolució del servei", "Document", False, False)
        )
    ),
    (
        "Manuals", "Folder", False, ('Document', 'File', 'Folder'),
        (
            ("Manual usuari", "Document", False, False),
            ("Manual administrador", "Document", False, False)
        )
    ),
    (
        "Ajuda", "Folder", False, ('Document', 'File', 'Folder'),
        (
            ("FAQs", "Folder", False, False),
            ("Casos d'ús", "Document", False, False),
            ("Errors coneguts", "Document", False, False)
        )
    ),
    (
        "Documentació", "Folder", False, ('Document', 'File', 'Folder'),
        (
            ("Documentació tècnica", "Folder", False, False),
            ("Documentació de referència", "Folder", False, False),
            ("Enllaços", "Folder", False, False, ('Link',))
        )
    ),
    (
        "Suggeriments", "Folder", False, ('Document', 'File', 'Folder'),
        (
            ("Suggeriments", "Document", True, True),
        )
    ),
    (
        "Notificacions", "Folder", True, ('notificaciotic',),
        ()
    ),
    (
        "Banners", "BannerContainer", True, ('Banner',),
        (),
    )
)
