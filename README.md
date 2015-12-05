# Pelican "Coming Soon" Plugin

Allows to list draft posts as "coming soon" on the articles list page without any links to them

![Screenshot]
(https://raw.githubusercontent.com/chiragjn/pelican-coming-soon-plugin/master/screenshot.png)


Draft's metadata needs to have the "visible_draft" field with value "true"

```
:status: draft
:visible_draft: true
```

Then adapt your theme's index.html accordingly

Example:

```
{% for article in articles_page.object_list %}
<article>
  <div id="article_title">
    <h1 id="no_vertical_margin">
      {% if article.status.lower() == "draft" and article.metadata.visible_draft %}
        <a class="button_more" href="{{ SITEURL }}/">{{ article.title }}</a>
      {% else %}
        <a class="button_more" href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a>
      {% endif %}
  </div>
  <div id="article_text">
    {{ article.summary }}
  </div>
  <div id="article_more">
	{% if article.status.lower() == "draft" and article.metadata.visible_draft %}
		<a class="button_more" href="{{ SITEURL }}/">Coming Soon</a>
	{% else %}
		<a class="button_more" href="{{ SITEURL }}/{{ article.url }}">Read &rarr;</a>
	{% endif %}	
  </div>
</article>
{% if not loop.last %}
<hr />
{% endif %}
{% endfor %}
```

Also your archives.html

```
{% extends "base.html" %}
{% block title %}Archives{% endblock %}

{% block content %}
<article>
  <div id="article_text">
    <dl>
      {% for article in dates %}
      	{% if article.status.lower() == "published" %}
	      <dt>{{ article.locale_date }}</dt>
	      <dd><a href="{{ SITEURL }}/{{ article.url }}">{{ article.title }}</a></dd>
	    {% endif %}
      {% endfor %}
    </dl>
  </div>
</article>
{% endblock %}
{% block footer %}
<p><a href="{{ SITEURL }}/" class="button_accent">&larr; Back to Index</a></p>
{% endblock %}

```
