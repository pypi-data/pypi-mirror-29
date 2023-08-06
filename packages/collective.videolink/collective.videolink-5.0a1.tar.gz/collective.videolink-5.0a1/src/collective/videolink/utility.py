from zope.annotation.interfaces import IAnnotations
from zope.interface.declarations import alsoProvides
from zope.interface.declarations import noLongerProvides
import hashlib
import re
from plone import api
from zope.interface.declarations import providedBy
from collective.videolink.interfaces import IVideoLinkGoogleDrive, IVideoLinkThumb, IVideoLinkOembedable
import requests
    
def add_thumbnail(context, event):
    """
    annotates the current context with a thumbnail based on its remote_url
    updates the thumbnail if the remote_url has changed on save
    
    @param context: Zope object for which the event was fired for. Usually this is Plone content object.

    @param event: Subclass of event.
    """
    if '/portal_factory/' in context.absolute_url():
        return context
    if old_hashed_url(context) and not hashed_url_changed(context):
        return context
    unmark_video_link(context)
    _thumbnail = get_thumbnail(context)    
    if _thumbnail:
        update_thumbnail(context)
        mark_video_link(context)
    else:
        remove_thumbnail(
              unmark_video_link(context)
              )
        return context

def hashed_url_changed(context):
    candidate_hashed_remote_url = hashlib.md5(
                                      get_remote_url(context)
                                  ).digest()
    
    return hashed_url(context) == candidate_hashed_remote_url

def get_json(context):
    """Get the embed_json for a given context"""
    remote_url = get_remote_url(context)
    query = "https://noembed.com/embed?url={}".format(remote_url)
    response = requests.get(query)
    return response.json()

def get_remote_url(context):
    """
    Get the remote url from the context
    """
    try:
        remote_url = context.getRemoteUrl()
    except AttributeError:
        remote_url = context.remoteUrl
    return remote_url

def extract_gdrive_id(context):
    """
     if url is of form similar to 
     https://drive.google.com/file/d/1Xr-UHkW5dTSl-c66kVler6MAobvBSBtU/view
     extract the id 1Xr-UHkW5dTSl-c66kVler6MAobvBSBtU
    """
    remote_url = get_remote_url(context)
    p = re.compile('https://drive.google.com/file/d/([\w-]{30,})/view')
    return ''.join(p.findall(remote_url))

def get_gdrive_thumb(context):
    gdrive_id = extract_gdrive_id(context)
    if gdrive_id:
        return "https://drive.google.com/thumbnail?authuser=0&sz=w320&id={}".format(gdrive_id)
    return None
    
def get_thumbnail(context):
    """ given a context, use noembed.com to retrieve 
        a thumbnail
    """
    gdrive_thumb = get_gdrive_thumb(context)
    if gdrive_thumb: 
        return gdrive_thumb
    output = get_json(context)
    return output.get('thumbnail_url',None)
    
def mark_video_as_google_drive_link(context):
    """
    Mark a link as a google drive resource
    """
    alsoProvides(mark_video_link(context),
                     IVideoLinkGoogleDrive
                     )
    return context 
                     
def mark_video_link(context):
    """
    Mark a link as an oembedable resource
    (usually a video, may need to refactor because
    this works for resources like soundcloud and flickr also)
    """
    alsoProvides(context,
                     IVideoLinkThumb,
                     IVideoLinkOembedable
                     )
    #reindex(context)
    return context
    
def old_hashed_url(context):
    """
    retrieve the hashed_url, returns 'None'
    if it doesn't exist.
    """
    annotations = IAnnotations(context)
    data = annotations.get('collective.videolink.data', {})
    return data.get('hashed_remote_url', None)
    
def reindex(context, idxs=['object_provides'], update_metadata=1):
    """
      reindex object
      idea borrowed from https://gist.github.com/jensens/3518210#file-action-py-L17-L19
    """
    catalog = api.portal.get_tool(name='portal_catalog')
    catalog.reindexObject(context, 
                          idxs=idxs, 
                          update_metadata=update_metadata
                          )
    return context
                          
def remove_thumbnail(context):
    annotations = IAnnotations(context)
    has_collective_videolink_data = annotations.get('collective.videolink.data',{})
    if 'thumbnail' in has_collective_videolink_data:
        del annotations['collective.videolink.data']['thumbnail']
    return context
    
def unmark_video_link(context):
    noLongerProvides(context, IVideoLinkThumb)
    noLongerProvides(context, IVideoLinkOembedable)
    noLongerProvides(context, IVideoLinkGoogleDrive)
    #reindex(context)
    return context

def update_thumbnail(context):
    annotations = IAnnotations(context)
    if 'collective.videolink.data' not in annotations:
        annotations['collective.videolink.data'] = {}
    annotations['collective.videolink.data']['thumbnail'] = get_thumbnail(context)