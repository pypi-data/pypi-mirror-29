# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class CollectiveVideoLinkLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.videolink
        import collective.videolink.tests
        import plone.patternslib
        self.loadZCML(package=collective.videolink)
        self.loadZCML(package=plone.patternslib)
        # self.loadZCML(package=collective.videolink.tests)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.videolink:default')


COLLECTIVE_VIDEOLINK_FIXTURE =\
    CollectiveVideoLinkLayer()

COLLECTIVE_VIDEOLINK_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_VIDEOLINK_FIXTURE,),
    name='Integration')
COLLECTIVE_VIDEOLINK_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_VIDEOLINK_FIXTURE,),
    name='Functional')
COLLECTIVE_VIDEOLINK_ROBOT_TESTING = FunctionalTesting(
    bases=(AUTOLOGIN_LIBRARY_FIXTURE,
           COLLECTIVE_VIDEOLINK_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name='Robot')