#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals
import os

if os.environ.get("BLOG_DEV") == "YES":
    SITEURL = "http://localhost:8000"

elif os.environ.get("BLOG_DEV") == "NO":
    SITEURL = "https://reachip.github.io"
    RELATIVE_URLS = False

else:
    raise Exception(
        "On doit mettre BLOG_DEV à YES ou à NO afin de déterminer l'URL à soumettre à Pelican !"
    )

ARTICLE_URL = "articles/{lang}/{slug}.html"
ARTICLE_SAVE_AS = "articles/{lang}/{slug}.html"

PAGE_URL = "annexe/{slug}.html"
PAGE_SAVE_AS = "annexe/{slug}.html"

TWITTER_USERNAME = "SirRached"

THEME = "./themes/flex"
DISQUS_SITENAME = "http://reachip.github.io/"
USE_LESS = True
USE_GOOGLE_FONTS = True
SITELOGO = "https://avatars0.githubusercontent.com/u/26501917?s=460&v=4"
GOOGLE_ANALYTICS = os.environ.get("GOOGLE_AN")

if GOOGLE_ANALYTICS is None:
    raise Exception(
        "Jeton de Google Analytics non fourni dans la variable d'environnement GOOGLE_AN !"
    )

AUTHOR = "Rached MEJRI"
SITENAME = "Rached"
SITEDESCRIPTION = "Lycéen écrivant du code gargouilleux à en devenir coquefredouille."
DISABLE_URL_HASH = False
RELATED_POSTS_MAX = 2
OG_LOCALE = "fr_FR"
LOCALE = "fr_FR"
FAVICON = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/GNOME_Terminal_icon_2019.svg/128px-GNOME_Terminal_icon_2019.svg.png"
GITHUB_CORNER_URL = "https://github.com/Reachip/reachip.github.io"
I18N_TEMPLATES_LANG = "fr"
STATIC_PATHS = ["images"]
CC_LICENSE = True
BROWSER_COLOR = "#090a0b"
ROBOTS = "index, follow"
PYGMENTS_STYLE = "monokai"
COPYRIGHT_NAME = "Rached MEJRI"
DISQUS_SITENAME = "sir-rached"
PATH = "content"
TIMEZONE = "Europe/Paris"
DEFAULT_CATEGORY = "sujets random"

DEFAULT_LANG = "fr"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
USE_FOLDER_AS_CATEGORY = True
PLUGINS = [
    'extended_sitemap'
]
EXTENDED_SITEMAP_PLUGIN = {
    'priorities': {
        'index': 1.0,
        'articles': 0.8,
        'pages': 0.5,
        'others': 0.4
    },
    'changefrequencies': {
        'index': 'daily',
        'articles': 'weekly',
        'pages': 'monthly',
        'others': 'monthly',
    }
}
SHOW_SOCIAL_ON_INDEX_PAGE_HEADER = True
SOCIAL = (
    ("gitlab", "https://gitlab.com/reachip"),
    ("twitter", "https://twitter.com/SirRached"),
    ("envelope", "mailto:r.mejri74100@gmail.com"),
    ("github", "https://github.com/Reachip"),
    ("linkedin", "https://www.linkedin.com/in/rached-mejri")
)
SITESUBTITLE = "Blog d'un lycéen de terminal STI2D SIN, utilisateur de Linux, Python et Rust en ce qui concerne l'informatique"
DEFAULT_PAGINATION = 10
AUTHOR_BIO = "Blog d'un lycéen de terminal STI2D SIN, utilisateur de Linux, Python et Rust en ce qui concerne l'informatique"
GITHUB_URL = "https://github.com/Reachip"
