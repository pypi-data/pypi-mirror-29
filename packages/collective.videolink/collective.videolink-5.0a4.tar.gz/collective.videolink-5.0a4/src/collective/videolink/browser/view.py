import requests
from collective.videolink.utility import add_thumbnail
from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

try:
    from collective.flowplayer.interfaces import IVideo
    from collective.flowplayer.interfaces import IAudio
    HAS_FLOWPLAYER = True
except ImportError:
    HAS_FLOWPLAYER = False

class VideoLink(BrowserView):
    """ Default view for links with awareness for videos

        Check if the context is a video link from known provider
        or a flowplayer resource.
        If not, just fall back to default view
    """

    index = ViewPageTemplateFile("embeddedvideo.pt")

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        


    # FIXME add annotation so that it doesn't go there everytime
#    def thumbnail(self):
#        return add_thumbnail(self.context,'non event')

    def embedcode(self):
        try:
            # is archetypes
            remote_url = self.context.getRemoteUrl()
        except AttributeError:
            # is dexterity
            remote_url = self.context.remoteUrl
        gdrive_embed = self.is_google_drive(remote_url)
        if gdrive_embed:
            return gdrive_embed
        query = "https://noembed.com/embed?url={}".format(remote_url)
        response = requests.get(query)
        embed_json = response.json()
        return embed_json['html']

#    @property
    def is_google_drive(self,remote_url):
        if remote_url.startswith('https://drive.google.com'):
            if remote_url.endswith('/view'):
                return """<iframe src="{}" 
                            allowfullscreen="true" 
                            webkitallowfullscreen="true" 
                            mozallowfullscreen="true">
                </iframe>""".format(
                              remote_url.replace('/view','/preview')) 
        return None
        
    def _view(self):
        context_here = aq_inner(self.context)
        traverse_view =  context_here.restrictedTraverse
        if HAS_FLOWPLAYER and (IVideo.providedBy(self.context) or
                               IAudio.providedBy(self.context)):
            return traverse_view('flowplayer')
        elif not self.embedcode():
            link = traverse_view('link_redirect_view')
            return link()
        else:
            return self.index()

    def __call__(self, *args, **kwargs):
        return self._view()

class VideoLinkList(BrowserView):
    """ Default view for list of video links, checks if the link has a video
    """
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
       
    def thumbnail(self,item_brain):
        item = item_brain.getObject()
        annotations = IAnnotations(item)
        data = annotations.get('collective.videolink.data',{})
        if 'thumbnail' in data:
            return data['thumbnail']