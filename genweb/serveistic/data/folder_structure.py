# -*- coding: utf-8 -*-

folder_structure = (
    (
        # title, type, exclude_from_nav, allow_discussion,
        # allowed_types,
        # layout, content
        "El servei", "Folder", False, False,
        ('Document', 'File', 'Folder', 'Image'),
        'folder_index_view',
        (
            # title, type, exclude_from_nav, allow_discussion, allowed_types,
            # layout
            ("Descripció del servei", "Document", False, False, None, None),
            ("Normativa", "Document", False, False, None, None),
            ("Procediments", "Document", False, False, None, None),
            ("Evolució del servei", "Document", False, False, None, None),
            ("Errors coneguts", "Document", False, False, None, None),
        )
    ),
    (
        "Documentació", "Folder", False, False,
        ('Document', 'File', 'Folder', 'Image'),
        'folder_index_view',
        (
            ("Manuals", "Folder", False, False,
                ('Document', 'File', 'Folder', 'Image'), 'folder_index_view'),
            ("Casos d'ús", "Document", False, False, None, None),
        )
    ),
    (
        "FAQ", "Folder", False, False,
        ('Document', 'File', 'Folder', 'Image'),
        'folder_index_view',
        (),
    ),
    (
        "Doc tècnica", "Folder", False, False,
        ('Document', 'File', 'Folder', 'Image'),
        'folder_index_view',
        (
            ("Documentació tècnica", "Document", False, False, None, None),
            ("Documentació de referència", "Document", False, False, None,
                None),
            ("Enllaços", "Document", False, False, None, None)
        )
    ),
    (
        "Suggeriments", "Folder", False, True, ('Document', 'File', 'Folder'),
        None,
        ()
    ),
    (
        "Notificacions", "Folder", True, False, ('notificaciotic',),
        None,
        ()
    ),
    (
        "Problemes", "Folder", True, False, ('problema',),
        None,
        ()
    ),
    (
        "Banners", "BannerContainer", True, False, ('Banner',),
        None,
        (),
    )
)
