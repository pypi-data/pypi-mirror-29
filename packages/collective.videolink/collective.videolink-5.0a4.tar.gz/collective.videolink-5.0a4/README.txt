Introduction
============

This package adds a new view to Plone's Link content type. If the remote url of
the link is an oembedable video collective.videolink will
override the default `link_redirect_view` browserview to show
the embedded video.

.. contents::


Credits
======================================
The code was originally forked from another project
nmd.ploneaslinkvideoembed

.. _plonelinkasvideoembed:  http://plone.org/products/nmd.plonelinkasvideoembed


Dependencies
============

* Plone
* requests
* plone.patternslib

Plone 4 compatibility
==========================
Use collective.videolink 3.0a5

Plone 5 compatibility
=======================
Use collective.videolink >5.0

Version 5 has support for video from Vimeo and Youtube and experimental support for public video links from Google Drive.


Why this package ?
==================

I needed a way to display video links in a thumbnail gallery style view
This provides a simple view for collections of video links. 
This is known to work with videos from youtube and vimeo. It also works with
soundcloud and other oembedable links.
