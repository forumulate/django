# forumulate-django

Add Forumulate to a Django site: comments under your articles, the docs search
/ ask-AI box, the "What's new" changelog bell, and server-rendered lists of your
blog posts, forum topics, changelog releases and docs pages (good for SEO,
cached with Django's cache).

## Install

```sh
pip install forumulate-django            # add [markdown] to render Markdown bodies
```

```python
# settings.py
INSTALLED_APPS = [..., "forumulate_django"]

FORUMULATE = {
    "ORG": "acme",          # your organization slug or id
    "SPACE": "community",   # the default space; every tag accepts space="..."
    # Optional:
    # "BASE_URL": "https://forumulate.com",   # or your custom domain
    # "API_URL": None,                        # defaults to BASE_URL + "/api"
    # "MODE": "script",                       # or "elements" for <forumulate-*> tags
    # "ELEMENTS_SRC": "https://cdn.jsdelivr.net/npm/@forumulate/embed@1",
    # "CACHE_TTL": 300, "TIMEOUT": 5, "CACHE_ALIAS": "default",
}
```

## Embeds

```django
{% load forumulate %}

{% forumulate_comments %}                                  {# comments for this URL #}
{% forumulate_comments space="blog-comments" theme="dark" accent="#0a7" %}
{% forumulate_widget mode="ask" placeholder="Ask the docs" %}
{% forumulate_changelog space="changelog" %}
```

Every keyword becomes a `data-*` attribute of the script (or an attribute of the
custom element in `elements` mode), HTML-escaped. `use_elements=True` switches a
single tag to the custom element.

## Server-rendered content

```django
{% forumulate_items "blog" limit=5 as posts %}
<ul>{% for post in posts %}
  <li><a href="{{ post.url }}">{{ post.title }}</a> {{ post.excerpt }}</li>
{% endfor %}</ul>

{% forumulate_item "forum" slug as topic %}
{% forumulate_markdown "blog" slug as body %}{{ body|forumulate_html }}
```

Kinds: `blog`, `forum`, `changelog`, `docs`. Only the public read API is used;
no token. If Forumulate is unreachable or a space is private, lists come back
empty and the page still renders. `forumulate_html` drops raw HTML and
`javascript:` links from the Markdown (forum posts are written by visitors).

## License

MIT

---

## About this repository

This repository is a public mirror, refreshed on each Forumulate release
(one commit per release). Pull requests are welcome; accepted changes are
applied upstream and arrive here with the next release.

- API reference: https://forumulate.com/reference
- Guides: https://forumulate.com/guides
- Community and support: https://forumulate.com/community
- Source: https://github.com/forumulate/django
