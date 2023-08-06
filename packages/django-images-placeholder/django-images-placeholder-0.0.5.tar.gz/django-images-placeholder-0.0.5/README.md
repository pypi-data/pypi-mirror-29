Django Images Placeholder
=========================

Automatic generates images with the right dimensions when
it's missing from the local media storage using metadata of
a common database to generate a image or fetching from an
alternative MEDIA_URL.

Installation
------------

1. Install the package with:

    `pip install django-images-placeholder`

2. Uninstall the package with:

    `pip uninstall django-images-placeholder`

3. Add "django_images_placeholder" to your INSTALLED_APPS setting like this::
```
    INSTALLED_APPS = [
        ...
        'django_images_placeholder',
    ]
```

4. Add and URL to your URLCONF:
```
    ...
    # This is NOT meant to be used in production environment.
    if settings.DEBUG:
        from django_images_placeholder.views import serve_image_placeholder
        urlpatterns = [
            url(r'^media/', serve_image_placeholder, name='images_placeholder'),
        ] + urlpatterns
```

5. On `settings.py`, set `MEDIA_URL` to point to it
```
    ...
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
    STATIC_ROOT = os.path.join(DATA_DIR, 'static')
    DEFAULT_FILE_STORAGE = 'django_images_placeholder.custom_storage.OverwritingStorage'
    STATICFILES_LOCATION = STATIC_URL
    MEDIAFILES_LOCATION = MEDIA_URL
```

6. Optionally, set `ALTERNATIVE_MEDIA_URL` to point to a production MEDIA_URL,
so with the view fail to provide an image by openning it locally or trying
to generating it by original image reference' metadata, it you ultimatelly
try to fetch `ALTERNATIVE_MEDIA_URL` and cache it:

    `ALTERNATIVE_MEDIA_URL = 'https://mybucket.s3.amazonaws.com/media/'`
