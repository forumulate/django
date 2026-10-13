"""
``{% load forumulate %}``

Embeds (each returns safe markup; every value is attribute-escaped):

    {% forumulate_comments %}
    {% forumulate_comments space="blog-comments" theme="dark" accent="#0a7" %}
    {% forumulate_widget mode="ask" placeholder="Ask the docs" %}
    {% forumulate_changelog space="changelog" %}

Content (cached with Django's cache for FORUMULATE["CACHE_TTL"] seconds):

    {% forumulate_items "blog" limit=5 as posts %}
    {% for post in posts %}<a href="{{ post.url }}">{{ post.title }}</a>{% endfor %}

    {% forumulate_item "blog" slug as post %}
    {% forumulate_markdown "blog" slug as body %}{{ body|forumulate_html }}
"""
from django import template
from django.utils.safestring import mark_safe

from ..conf import client, config
from ..core import embed_html, markdown_to_html

register = template.Library()


def _embed(kind, options):
    return mark_safe(embed_html(kind, config(), **options))


@register.simple_tag
def forumulate_comments(**options):
    return _embed("comments", options)


@register.simple_tag
def forumulate_widget(**options):
    return _embed("widget", options)


@register.simple_tag
def forumulate_changelog(**options):
    return _embed("changelog", options)


@register.simple_tag
def forumulate_feed(**options):
    return _embed("feed", options)


@register.simple_tag
def forumulate_search(**options):
    return _embed("search", options)


@register.simple_tag
def forumulate_items(kind, limit=10, space=None):
    return client().items(kind, space=space, limit=limit)


@register.simple_tag
def forumulate_item(kind, slug, space=None):
    return client().item(kind, slug, space=space)


@register.simple_tag
def forumulate_markdown(kind, slug, space=None):
    # Plain text: autoescaped if printed directly, or pass it to |forumulate_html.
    return client().markdown(kind, slug, space=space)


@register.filter
def forumulate_html(text):
    """Markdown -> HTML with raw HTML and javascript: links stripped."""
    return mark_safe(markdown_to_html(str(text or "")))
