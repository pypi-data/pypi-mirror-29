# MP-Poll

Django poll app.

### Installation

Install with pip:

```
$ pip install django-mp-poll
```

Add poll to settings.py:

```
INSTALLED_APPS = [
    ...
    'poll',
]
```

Add poll to urls.py:
```
urlpatterns = [
	...
	url(r'^poll/', include('poll.urls', namespace='poll')),
]
```

Add static components:
```
poll/poll.css
poll/poll.js
```

Sync DB:

```
$ python manage.py migrate
$ python manage.py sync_translation_fields
```

## Template
```
{% load poll %}

<div>
	{% render_latest_poll %}
</div>
```

### Requirements

App require this packages:

* django-modeltranslation
