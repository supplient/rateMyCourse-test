from flamenco.settings import *

__CSRF_MIDWARE = "django.middleware.csrf.CsrfViewMiddleware"
if __CSRF_MIDWARE in MIDDLEWARE:
    MIDDLEWARE.remove(__CSRF_MIDWARE)

FIXTURE_DIRS = [
    "test",
]

INSTALLED_APPS.append(
    'werkzeug_debugger_runserver',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

CSRF_TRUSTED_ORIGINS = [
    "ratemycourse.tk"
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}


###########################################
# Following are our settings, not django's
###########################################

FRONT_FIXTURE = "test/fixture.json"

LOG_PATH = "test/test.log"