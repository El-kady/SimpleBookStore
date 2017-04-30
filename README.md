# SimpleBookStore
Simple Book Store Using Django Framework
# Configuration
Required Settings:
```
INSTALLED_APPS += [
    'SimpleBookStore',
]

# Template context_processors
TEMPLATES[0]['OPTIONS']['context_processors'].append("SimpleBookStore.context_processors.simple_book_store_processor")

# Database Example
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': "localhost",
        'NAME': "django_bookstore",
        'USER': "root",
        'PASSWORD': "123456"
    }
}

# Media related settings are required for avatar uploading to function properly
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

# Configure URLs
Simply include the urls
```
from django.conf.urls import url, include
from django.contrib import admin
from SimpleBookStore import urls as SimpleBookStore_urls

urlpatterns = [
    ...
    url(r'', include(SimpleBookStore_urls, namespace="SimpleBookStore")),
]
```