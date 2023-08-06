# -*- coding: utf-8 -*-
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import collective.restapi.navigationtree


class CollectiveRestapiNavigationtreeDXLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        import webcouturier.dropdownmenu
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=webcouturier.dropdownmenu)
        self.loadZCML(package=collective.restapi.navigationtree)
        z2.installProduct(app, 'collective.restapi.navigationtree')

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        applyProfile(portal, 'collective.restapi.navigationtree:default')
        workflowTool = api.portal.get_tool('portal_workflow')
        workflowTool.setDefaultChain('simple_publication_workflow')
        for i in range(2):
            folder_id = 'folder-{0}'.format(i)
            api.content.create(
                type=u'Folder',
                id=folder_id,
                container=portal,
                title=folder_id,
            )
        setRoles(portal, TEST_USER_ID, ['Member'])


CRN_DX_FIXTURE = CollectiveRestapiNavigationtreeDXLayer()


CRN_DX_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CRN_DX_FIXTURE,),
    name='CollectiveRestapiNavigationtreeDXLayer:IntegrationTesting',
)


CRN_DX_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CRN_DX_FIXTURE, z2.ZSERVER_FIXTURE),
    name='CollectiveRestapiNavigationtreeDXLayer:FunctionalTesting',
)


class CollectiveRestapiNavigationtreeATLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.ATContentTypes
        self.loadZCML(package=Products.ATContentTypes)
        import plone.restapi
        import webcouturier.dropdownmenu
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=webcouturier.dropdownmenu)
        self.loadZCML(package=collective.restapi.navigationtree)
        z2.installProduct(app, 'Products.Archetypes')
        z2.installProduct(app, 'Products.ATContentTypes')
        z2.installProduct(app, 'collective.restapi.navigationtree')

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        if portal.portal_setup.profileExists(
                'Products.ATContentTypes:default'):
            applyProfile(portal, 'Products.ATContentTypes:default')
        applyProfile(portal, 'collective.restapi.navigationtree:default')
        workflowTool = api.portal.get_tool('portal_workflow')
        workflowTool.setDefaultChain('simple_publication_workflow')
        for i in range(2):
            folder_id = 'folder-{0}'.format(i)
            api.content.create(
                type=u'Folder',
                id=folder_id,
                container=portal,
                title=folder_id,
            )
        setRoles(portal, TEST_USER_ID, ['Member'])


CRN_AT_FIXTURE = CollectiveRestapiNavigationtreeATLayer()


CRN_AT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CRN_AT_FIXTURE,),
    name='CollectiveRestapiNavigationtreeATLayer:IntegrationTesting',
)


CRN_AT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CRN_AT_FIXTURE, z2.ZSERVER_FIXTURE),
    name='CollectiveRestapiNavigationtreeATLayer:FunctionalTesting',
)
