# -*- coding: utf-8 -*-
import unittest

from plone import api
from plone.app.contenttypes.interfaces import ILink
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

from collective.videolink.interfaces import IVideoLinkThumb, IVideoLinkOembedable
from collective.videolink.testing import COLLECTIVE_VIDEOLINK_INTEGRATION_TESTING

class ContentTypeTestCase(unittest.TestCase):

    layer = COLLECTIVE_VIDEOLINK_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.f1 = api.content.create(
                self.portal, 'Folder', 'f1')
            self.l1 = api.content.create(
                container=self.f1,
                type="Link",
                id="l1",
                safe_id=False,
                title='Bored of Approval',
                remoteUrl='https://www.youtube.com/watch?v=IZ1IS7_o0zQ'
                )
            self.l2 = api.content.create(
                container=self.f1,
                type="Link",
                id="l2",
                safe_id=False,
                title='Link to Plone.com',
                remoteUrl='https://www.plone.com'
                )

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Folder')
        self.assertIsNotNone(fti)

    def test_is_selectable_as_folder_default_view(self):
        self.portal.setDefaultPage('f1')
        self.assertEqual(self.portal.default_page, 'f1')

    def test_adding_l1(self):
        self.assertTrue(ILink.providedBy(self.l1))
    
    def test_adding_l2(self):
        self.assertTrue(ILink.providedBy(self.l2))
    
    def test_has_videolinkthumb_interface(self):
        self.assertTrue(IVideoLinkThumb.providedBy(self.l1))
        
    def test_does_not_have_videolinkthumb_interface(self):
        self.assertFalse(IVideoLinkThumb.providedBy(self.l2))
    
    def test_has_videolinkoembedable_interface(self):
        self.assertTrue(IVideoLinkOembedable.providedBy(self.l1))
        
    def test_does_not_have_videolinkoembedable_interface(self):
        self.assertFalse(IVideoLinkOembedable.providedBy(self.l2))
    
    def test_nolonger_has_thumbnail_after_adding_non_oembed_url(self):
        """ remove oembed thumb after changing remoteurl to a
            non-oembedable url
        """
        # XXX Fix me
        self.l1.remoteUrl = "http://plone.com"
        self.l1.reindexObject()
        self.l1.reindexObject(idxs=['modified'])
        self.assertFalse(IVideoLinkThumb.providedBy(self.l1))

    def test_now_has_oembed_after_adding_oembed_url(self):
        """ add oembed content after changing remoteurl to
            an oembedable url
        """
        self.l2.remoteUrl = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.l2.title = "Rick Rolled"
        self.l2.reindexObject()
        self.l2.reindexObject(idxs=['modified'])
        #import pdb;pdb.set_trace()
        self.assertTrue(IVideoLinkOembedable.providedBy(self.l2))
