from plone.indexer.decorator import indexer
from collective.videolink.utility import add_thumbnail
from Products.ATContentTypes.interface import IATLink
from plone.app.contenttypes.interfaces import ILink

@indexer(IATLink)
def videolink_thumbnail_at(object, **kw):
    return add_thumbnail(object,'index event')
     
@indexer(ILink)
def videolink_thumbnail(object, **kw):
    return add_thumbnail(object,'index event')