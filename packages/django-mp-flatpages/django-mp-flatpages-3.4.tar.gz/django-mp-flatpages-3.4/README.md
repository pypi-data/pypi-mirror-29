# MP-Flatpages

Django flatpages app.

### Installation

Install with pip:

```
$ pip install django-mp-flatpages
```

Add flatpages to urls.py:

```
urlpatterns += i18n_patterns(
    url(r'^', include('flatpages.urls'))
)
```

Add flatpages to settings.py:
```
from flatpages.constants import EDITOR_CKEDITOR_UPLOADER

INSTALLED_APPS = [
    'flatpages',
]

# OPTIONAL, default: None
# CHOICES: EDITOR_CKEDITOR, EDITOR_CKEDITOR_UPLOADER, EDITOR_MARTOR
FLATPAGE_DEFAULT_EDITOR = EDITOR_CKEDITOR_UPLOADER

# OPTIONAL, default: dict of editors
FLATPAGE_EDITORS = {
    'editor_name': 'path.to.widget.class'
}

# OPTIONAL, default: 'flatpages/default.html'
FLATPAGE_DEFAULT_TEMPLATE = 'path/to/template.html'
```

Run migrations:
```
$ python manage.py migrate
```

### Template

You should create templates/flatpages/default.html template in your app.

### Requirements

App require this packages:
* django-modeltranslation
