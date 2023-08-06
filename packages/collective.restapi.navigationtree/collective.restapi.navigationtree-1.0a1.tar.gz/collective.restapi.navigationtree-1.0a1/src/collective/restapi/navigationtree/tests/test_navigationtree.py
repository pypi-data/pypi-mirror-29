# -*- coding: utf-8 -*-
from collective.restapi.navigationtree.testing import CRN_AT_FUNCTIONAL_TESTING
from collective.restapi.navigationtree.testing import CRN_DX_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from webcouturier.dropdownmenu.browser.interfaces import IDropdownConfiguration

import transaction
import unittest


class NavigationBase(object):

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({'Accept': 'application/json'})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        # we have 2 folders created on the layer right away
        self.root_folders_ids = ['folder-0', 'folder-1']

        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def addSubFolders(self, container, base_id, level=0):
        # recursively add some subfolders to one of the folders
        if level > 0:
            setRoles(self.portal, TEST_USER_ID, ['Manager'])
            for i in range(2):
                api.content.create(
                    type=u'Folder',
                    title=u'Folder{0}'.format(i),
                    id=u'{0}-{1}'.format(base_id, i),
                    container=container,
                )
            transaction.commit()
            setRoles(self.portal, TEST_USER_ID, ['Member'])
            sub = getattr(container, u'{0}-0'.format(base_id))
            # recurse one level deeper
            self.addSubFolders(sub, u'sub-{0}'.format(base_id), level-1)

    def setDepth(self, depth):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        try:
            # webcouturier.dropdownmenu version 3.x
            api.portal.set_registry_record('dropdown_depth', depth, interface=IDropdownConfiguration)  # noqa: E501
        except KeyError:
            # webcouturier.dropdownmenu version 2.x
            propertiesTool = api.portal.get_tool(u'portal_properties')
            dmprops = propertiesTool[u'dropdown_properties']
            if dmprops.hasProperty(u'dropdown_depth'):
                dmprops._setPropValue(u'dropdown_depth', depth)
        transaction.commit()
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def test_navigation(self):
        # This test is almost identical to the corresponding one in
        # plone.restapi.  It is provided to illustrate the differences
        # between @navigation and @navigationtree
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.folder = api.content.create(
            container=self.portal, type=u'Folder',
            id=u'folder',
            title=u'Some Folder')
        api.content.create(
            container=self.folder, type=u'Document',
            id=u'doc1',
            title=u'A document')
        transaction.commit()
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        response = self.api_session.get('/folder/@navigationtree')

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            response.json(),
            RESPONSE_RESTAPI,
        )

    def test_no_subfolders_without_content(self):
        # since we don't have subfolders yet, we should not have dropdowns
        response = self.api_session.get('/@navigationtree')

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            response.json(),
            RESPONSE_LEVEL_0,
        )

    def test_dropdownmenus_available(self):
        rf = getattr(self.portal, 'folder-0')
        self.addSubFolders(rf, 'sub', 1)

        response = self.api_session.get('/@navigationtree')

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            response.json(),
            RESPONSE_LEVEL_1,
        )

    def test_dropdownmenus_available_level_3_depth_1(self):
        rf = getattr(self.portal, 'folder-0')
        self.addSubFolders(rf, 'sub', 3)
        self.setDepth(1)

        response = self.api_session.get('/@navigationtree')

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            response.json(),
            RESPONSE_LEVEL_1,
        )

    def test_dropdownmenus_available_level_2(self):
        rf = getattr(self.portal, 'folder-0')
        self.addSubFolders(rf, 'sub', 2)

        response = self.api_session.get('/@navigationtree')

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            response.json(),
            RESPONSE_LEVEL_2,
        )

    def test_dropdownmenus_available_level_3_depth_2(self):
        rf = getattr(self.portal, 'folder-0')
        self.addSubFolders(rf, 'sub', 3)
        self.setDepth(2)

        response = self.api_session.get('/@navigationtree')

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            response.json(),
            RESPONSE_LEVEL_2,
        )

    def test_dropdownmenus_available_level_3(self):
        rf = getattr(self.portal, 'folder-0')
        self.addSubFolders(rf, 'sub', 3)

        response = self.api_session.get('/@navigationtree')

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            response.json(),
            RESPONSE_LEVEL_3,
        )

    def test_dropdownmenus_available_level_5(self):
        # By default, the depth is 3, so all levels beyond 3 will return the
        # same result
        rf = getattr(self.portal, 'folder-0')
        self.addSubFolders(rf, 'sub', 5)

        response = self.api_session.get('/@navigationtree')

        self.assertEqual(response.status_code, 200)
        self.maxDiff = None
        self.assertEqual(
            response.json(),
            RESPONSE_LEVEL_3,
        )


class TestDXServicesNavigation(NavigationBase, unittest.TestCase):

    layer = CRN_DX_FUNCTIONAL_TESTING


class TestATServicesNavigation(NavigationBase, unittest.TestCase):

    layer = CRN_AT_FUNCTIONAL_TESTING


RESPONSE_RESTAPI = {
    u'@id': u'http://localhost:55001/plone/folder/@navigationtree',
    u'items': [
        {
            u'title': u'Home',
            u'description': u'',
            u'items': u'',
            u'@id': u'http://localhost:55001/plone',
        },
        {
            u'title': u'folder-0',
            u'description': u'',
            u'items': [],
            u'@id': u'http://localhost:55001/plone/folder-0',
        },
        {
            u'title': u'folder-1',
            u'description': u'',
            u'items': [],
            u'@id': u'http://localhost:55001/plone/folder-1',
        },
        {
            u'title': u'Some Folder',
            u'description': u'',
            u'@id': u'http://localhost:55001/plone/folder',
            u'items': [
                {
                    u'title': u'A document',
                    u'description': u'',
                    u'@id':
                      u'http://localhost:55001/plone/folder/doc1',
                },
            ],
        },
    ],
}

RESPONSE_LEVEL_0 = {
    u'@id': u'http://localhost:55001/plone/@navigationtree',
    u'items': [
        {
            u'title': u'Home',
            u'description': u'',
            u'items': u'',
            u'@id': u'http://localhost:55001/plone',
        },
        {
            u'title': u'folder-0',
            u'description': u'',
            u'items': [],
            u'@id': u'http://localhost:55001/plone/folder-0',
        },
        {
            u'title': u'folder-1',
            u'description': u'',
            u'items': [],
            u'@id': u'http://localhost:55001/plone/folder-1',
        },
    ],
}

RESPONSE_LEVEL_1 = {
    u'@id': u'http://localhost:55001/plone/@navigationtree',
    u'items': [
        {
            u'title': u'Home',
            u'description': u'',
            u'items': u'',
            u'@id': u'http://localhost:55001/plone',
        },
        {
            u'title': u'folder-0',
            u'description': u'',
            u'items': [
                {
                    u'title': u'Folder0',
                    u'description': u'',
                    u'@id':
                      u'http://localhost:55001/plone/folder-0/sub-0',  # noqa: E501
                },
                {
                    u'title': u'Folder1',
                    u'description': u'',
                    u'@id':
                      u'http://localhost:55001/plone/folder-0/sub-1',  # noqa: E501
                },
            ],
            u'@id': u'http://localhost:55001/plone/folder-0',
        },
        {
            u'title': u'folder-1',
            u'description': u'',
            u'items': [],
            u'@id': u'http://localhost:55001/plone/folder-1',
        },
    ],
}

RESPONSE_LEVEL_2 = {
    u'@id': u'http://localhost:55001/plone/@navigationtree',
    u'items': [
        {
            u'title': u'Home',
            u'description': u'',
            u'items': u'',
            u'@id': u'http://localhost:55001/plone',
        },
        {
            u'title': u'folder-0',
            u'description': u'',
            u'items': [
                {
                    u'title': u'Folder0',
                    u'description': u'',
                    u'items': [
                        {
                            u'title': u'Folder0',
                            u'description': u'',
                            u'@id':
                              u'http://localhost:55001/plone/folder-0/sub-0/sub-sub-0',  # noqa: E501
                        },
                        {
                            u'title': u'Folder1',
                            u'description': u'',
                            u'@id':
                              u'http://localhost:55001/plone/folder-0/sub-0/sub-sub-1',  # noqa: E501
                        },
                    ],
                    u'@id':
                      u'http://localhost:55001/plone/folder-0/sub-0',  # noqa: E501
                },
                {
                    u'title': u'Folder1',
                    u'description': u'',
                    u'@id':
                      u'http://localhost:55001/plone/folder-0/sub-1',  # noqa: E501
                },
            ],
            u'@id': u'http://localhost:55001/plone/folder-0',
        },
        {
            u'title': u'folder-1',
            u'description': u'',
            u'items': [],
            u'@id': u'http://localhost:55001/plone/folder-1',
        },
    ],
}

RESPONSE_LEVEL_3 = {
    u'@id': u'http://localhost:55001/plone/@navigationtree',
    u'items': [
        {
            u'title': u'Home',
            u'description': u'',
            u'items': u'',
            u'@id': u'http://localhost:55001/plone',
        },
        {
            u'title': u'folder-0',
            u'description': u'',
            u'items': [
                {
                    u'title': u'Folder0',
                    u'description': u'',
                    u'items': [
                        {
                            u'title': u'Folder0',
                            u'description': u'',
                            u'items': [
                                {
                                    u'title': u'Folder0',
                                    u'description': u'',
                                    u'@id':
                                      u'http://localhost:55001/plone/folder-0/sub-0/sub-sub-0/sub-sub-sub-0',  # noqa: E501
                                },
                                {
                                    u'title': u'Folder1',
                                    u'description': u'',
                                    u'@id':
                                      u'http://localhost:55001/plone/folder-0/sub-0/sub-sub-0/sub-sub-sub-1',  # noqa: E501
                                },
                            ],
                            u'@id':
                              u'http://localhost:55001/plone/folder-0/sub-0/sub-sub-0',  # noqa: E501
                        },
                        {
                            u'title': u'Folder1',
                            u'description': u'',
                            u'@id':
                              u'http://localhost:55001/plone/folder-0/sub-0/sub-sub-1',  # noqa: E501
                        },
                    ],
                    u'@id':
                      u'http://localhost:55001/plone/folder-0/sub-0',  # noqa: E501
                },
                {
                    u'title': u'Folder1',
                    u'description': u'',
                    u'@id':
                      u'http://localhost:55001/plone/folder-0/sub-1',  # noqa: E501
                },
            ],
            u'@id': u'http://localhost:55001/plone/folder-0',
        },
        {
            u'title': u'folder-1',
            u'description': u'',
            u'items': [],
            u'@id': u'http://localhost:55001/plone/folder-1',
        },
    ],
}
