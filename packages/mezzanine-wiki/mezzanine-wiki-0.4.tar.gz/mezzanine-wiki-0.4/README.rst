========
Overview
========

Wiki application for Mezzanine.

Features:

- markdown syntax with [[Wiki links]] extension
- page history and diff viewing

Requirements:

- Mezzanine >= 4.2.3
- markdown
- diff-match-patch


=========
Mezzanine
=========

Mezzanine is a content management platform built using the Django
framework. It is BSD licensed and designed to provide both a
consistent interface for managing content, and a simple, extensible
architecture that makes diving in and hacking on the code as easy as
possible.

Visit the Mezzanine project page to see some of the great sites
people have built using Mezzanine.

http://mezzanine.jupo.org

http://github.com/stephenmcd/mezzanine


===========
This Fork
===========

This fork borrows heavily from the original project https://github.com/dfalk/mezzanine-wiki.
Essentially the only changes are: updating the views to Class based, removing South
as the db and tweaking the urls.

===========
Quick start
===========

1. Activate your virtualenv (if applicable). Install mezzanine-wiki with "pip install mezzanine-wiki":

2. Add "mezzanine_wiki" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'mezzanine_wiki',
    )
    
3. Add "mezzanine_wiki.WikiPage" to SEARCH_MODEL_CHOICES in your app's settings like this:

   SEARCH_MODEL_CHOICES = ('pages.Page', 'blog.BlogPost', 'mezzanine_wiki.WikiPage')

4. Include the wiki URLconf in your project urls.py like this::

   url(r'^wiki/', include('mezzanine_wiki.urls')),

5. To use the RTF editor add the following to your app's settings:

   WIKI_TEXT_WIDGET_CLASS = 'mezzanine.core.forms.TinyMceWidget'

6. Run `python manage.py migrate` to create the wiki models.

7. Restart server.

8. Visit /wiki/ to use the wiki.


