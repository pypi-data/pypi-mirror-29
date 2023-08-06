# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.portlets.portlets.navigation import Assignment
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from webcouturier.dropdownmenu.browser.dropdown import DropdownQueryBuilder
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class NavigationTree(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        portal_props = api.portal.get_tool(name=u'portal_properties')
        self.properties = portal_props.navtree_properties
        self.portal_state = getMultiAdapter((context, request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        portal_path = '/'.join(self.portal.getPhysicalPath())
        navroot_path = getNavigationRoot(context)
        if portal_path != navroot_path:
            self.portal = self.portal.restrictedTraverse(navroot_path)
        if api.env.plone_version() < '5':
            self.data = Assignment(root=navroot_path)
        else:
            self.data = Assignment(root_uid=None)

    def __call__(self, expand=False):
        context = self.context
        result = {
            'navigationtree': {
                '@id': '{0}/@navigationtree'.format(context.absolute_url()),
            },
        }
        if not expand:
            return result

        tabs = getMultiAdapter((context, self.request),
                               name='portal_tabs_view')
        items = []
        for tab in tabs.topLevelTabs():
            subitems = self.getTabObject(tabUrl=tab['url'],
                                         tabPath=tab.get('path'))
            items.append({
                'title': tab.get('title', tab.get('name')),
                '@id': tab['url'] + '',
                'description': tab.get('description', ''),
                'items': subitems,
            })
        result['navigationtree']['items'] = items
        return result

    def getTabObject(self, tabUrl='', tabPath=None):
        if tabPath is None:
            # get path for current tab's object
            tabPath = tabUrl.split(self.portal.absolute_url())[-1]

            if tabPath == '' or '/view' in tabPath:
                return ''

            if tabPath.startswith('/'):
                tabPath = tabPath[1:]
            elif tabPath.endswith('/'):
                # we need a real path, without a slash that might appear
                # at the end of the path occasionally
                tabPath = str(tabPath.split('/')[0])

            if '%20' in tabPath:
                # we have the space in object's ID that has to be
                # converted to the real spaces
                tabPath = tabPath.replace('%20', ' ').strip()

        tabObj = self.portal.restrictedTraverse(tabPath, None)
        if tabObj is None:
            return ''
        strategy = getMultiAdapter((tabObj, self.data),
                                   INavtreeStrategy)
        queryBuilder = DropdownQueryBuilder(tabObj)
        query = queryBuilder()
        data = buildFolderTree(tabObj, obj=tabObj, query=query,
                               strategy=strategy)
        bottomLevel = self.data.bottomLevel or self.properties.getProperty(
            'bottomLevel', 0)

        return self.recurse(children=data.get('children', []), level=1,
                            bottomLevel=bottomLevel)

    def recurse(self, children=None, level=0, bottomLevel=0):
        li = []
        for node in children:
            item = {'title': node['Title'], 'description': node['Description']}
            item['@id'] = node['getURL']
            if bottomLevel <= 0 or level <= bottomLevel:
                nc = node['children']
                nc = self.recurse(nc, level+1, bottomLevel)
                if nc:
                    item['items'] = nc
            li.append(item)
        return li


class NavigationTreeGet(Service):

    def reply(self):
        navigationtree = NavigationTree(self.context, self.request)
        return navigationtree(expand=True)['navigationtree']
