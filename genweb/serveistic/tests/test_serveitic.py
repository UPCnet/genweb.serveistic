# -*- coding: utf-8 -*-

from plone.api.content import create

from genweb.serveistic.testing import IntegrationTestCase


class TestServeiTic(IntegrationTestCase):
    def setUp(self):
        self.portal = self.layer['portal']

    def assert_content_in(self, container, id, portal_type, title):
        self.assertIn(id, container)
        content = container[id]
        self.assertEquals(content.portal_type, portal_type)
        self.assertEquals(content.title, title)

    def test_create_serveitic_folder_structure(self):
        serveitic = create(
            self.portal,
            type='serveitic',
            id='serveitic-1',
            title='Servei TIC 1'
            )

        self.assert_content_in(serveitic, 'el-servei', 'Folder', 'El servei')
        self.assert_content_in(
            serveitic['el-servei'],
            'descripcio-del-servei',
            'Document',
            'Descripció del servei')
        self.assert_content_in(
            serveitic['el-servei'],
            'normativa',
            'Document',
            'Normativa')
        self.assert_content_in(
            serveitic['el-servei'],
            'procediments',
            'Document',
            'Procediments')
        self.assert_content_in(
            serveitic['el-servei'],
            'evolucio-del-servei',
            'Document',
            'Evolució del servei')
        self.assert_content_in(
            serveitic['el-servei'],
            'errors-coneguts',
            'Document',
            'Errors coneguts')

        self.assert_content_in(serveitic, 'documentacio', 'Folder',
                               'Documentació')
        self.assert_content_in(
            serveitic['documentacio'],
            'manuals',
            'Folder',
            'Manuals')
        self.assert_content_in(
            serveitic['documentacio'],
            'casos-dus',
            'Document',
            "Casos d'ús")

        self.assert_content_in(serveitic, 'faq', 'Folder', 'FAQ')

        self.assert_content_in(serveitic, 'doc-tecnica', 'Folder',
                               'Doc tècnica')
        self.assert_content_in(
            serveitic['doc-tecnica'],
            'documentacio-tecnica',
            'Document',
            'Documentació tècnica')
        self.assert_content_in(
            serveitic['doc-tecnica'],
            'documentacio-de-referencia',
            'Document',
            "Documentació de referència")
        self.assert_content_in(
            serveitic['doc-tecnica'],
            'enllacos',
            'Document',
            "Enllaços")

        self.assert_content_in(serveitic, 'suggeriments', 'Folder',
                               'Suggeriments')
