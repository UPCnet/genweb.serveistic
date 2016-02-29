# -*- coding: utf-8 -*-

folder_structure = (
    (
        # title, type, exclude_from_nav, allow_discussion, allowed_types,
        # layout, content
        "El servei", "Folder", False, False, ('Document', 'File', 'Folder'),
        'folder_index_view',
        (
            # title, type, exclude_from_nav, allow_discussion, allowed_types,
            # layout
            ("Descripció del servei", "Document", False, False, None, None),
            ("Normativa", "Document", False, False, None, None),
            ("Procediments", "Document", False, False, None, None),
            ("Evolució del servei", "Document", False, False, None, None)
        )
    ),
    (
        "Manuals", "Folder", False, False, ('Document', 'File', 'Folder'),
        'folder_index_view',
        (
            ("Manual usuari", "Document", False, False, None, None),
            ("Manual administrador", "Document", False, False, None, None)
        )
    ),
    (
        "Ajuda", "Folder", False, False, ('Document', 'File', 'Folder'),
        'folder_index_view',
        (
            ("FAQs", "Folder", False, False, None, 'folder_index_view'),
            ("Casos d'ús", "Document", False, False, None, None),
            ("Errors coneguts", "Document", False, False, None, None)
        )
    ),
    (
        "Documentació", "Folder", False, False, ('Document', 'File', 'Folder'),
        'folder_index_view',
        (
            ("Documentació tècnica", "Folder", False, False, None,
                'folder_index_view'),
            ("Documentació de referència", "Folder", False, False, None,
                'folder_index_view'),
            ("Enllaços", "Folder", False, False, ('Link',),
                'folder_index_view')
        )
    ),
    (
        "Suggeriments", "Folder", False, True, ('Document', 'File', 'Folder'),
        None,
        ()
    ),
    (
        "Notificacions", "Folder", True, True, ('notificaciotic',),
        None,
        ()
    ),
    (
        "Banners", "BannerContainer", True, True, ('Banner',),
        None,
        (),
    )
)
