"""Common settings and globals."""


from os.path import abspath, basename, dirname, join, normpath
from sys import path
from environ import Env


########## PROJECT CONFIGURATION
CASSETTO = {
    'STORAGE_NAME_MAX_LENGTH': 255,
    'FILENAME_MAX_LENGTH': 1023,
}
########## END PROJECT CONFIGURATION


########## PATH CONFIGURATION
PACKAGE_PATH = dirname(dirname(abspath(__file__)))
PACKAGE_NAME = basename(PACKAGE_PATH)

PROJECT_PATH = dirname(PACKAGE_PATH)
PROJECT_NAME = "Cassetto" or PACKAGE_NAME
PROJECT_PACKAGE = "cassetto" or PACKAGE_NAME

REPO_PATH = dirname(PROJECT_PATH)
REPO_NAME = "op-cassetto" or basename(REPO_PATH)

CONFIG_DIR = 'config'
CONFIG_PATH = join(REPO_PATH, CONFIG_DIR)

RESOURCE_DIR = 'resources'
RESOURCES_PATH = join(REPO_PATH, RESOURCE_DIR)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(PROJECT_PATH)

# load environment variables
Env.read_env(normpath(join(CONFIG_PATH, '.env')))
env = Env()
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DEBUG', False)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG

QUERY_DEBUG = env.bool('QUERY_DEBUG', False)
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
ADMIN_EMAIL = env.str('ADMIN_EMAIL', 'admin@%s.com' % PROJECT_NAME)
ADMIN_NAME = env.str('ADMIN_NAME', ADMIN_EMAIL.split('@')[0])

# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    (ADMIN_EMAIL, ADMIN_NAME),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# See: https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', ADMIN_EMAIL)
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db(default='sqlite:///{0}'.format(normpath(join(RESOURCES_PATH, 'db', 'default.db'))))
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Rome'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'it-IT'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(RESOURCES_PATH, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(RESOURCES_PATH, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(PACKAGE_PATH, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"l-%a=$(w7ch(ry8eb&z-rwh)j1&%ikvd#ym0qrfmv7hm4b5hgj"
########## END SECRET CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
########## END SITE CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(RESOURCES_PATH, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(PACKAGE_PATH, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    # Default Django middleware.
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % PACKAGE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    # Django helper
    'django_extensions',

    # API REST
    'rest_framework',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'attrezzi.accesso',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'cassetto.apps.storage',
    'cassetto.apps.sharing',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
########## END AUTHENTICATION CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': normpath(join(RESOURCES_PATH, 'logs', 'op-cassetto.log')),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', ],
            'level': 'DEBUG',
        },
        'django.db': {
            'handlers': ['file', ],
            'level': 'DEBUG' if QUERY_DEBUG else 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
        'cassetto': {
            'handlers': ['file', ],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % PACKAGE_NAME
########## END WSGI CONFIGURATION


########## TESTING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/releases/1.6/#new-test-runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
########## END TESTING CONFIGURATION


########## API REST CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
########## END API REST CONFIGURATION


########## SENDFILE CONFIGURATION
# See: https://github.com/johnsensible/django-sendfile#readme
SENDFILE_BACKEND = 'sendfile.backends.development'

SENDFILE_ROOT = join(RESOURCES_PATH, 'storage')
SENDFILE_URL = '/protected_download'
########## END SENDFILE CONFIGURATION


########## ATTREZZI CONFIGURATION
ATTREZZI_ACCESSO_URL = env.str('ATTREZZI_ACCESSO_URL', 'http://example.com')
ATTREZZI = {
    'ACCESSO_ACCESS_TOKEN_URL': '%s/o/token/' % ATTREZZI_ACCESSO_URL,
    'ACCESSO_AUTHORIZE_URL': '%s/o/authorize/' % ATTREZZI_ACCESSO_URL,
    'ACCESSO_PROFILE_URL': '%s/api/v1/users/me' % ATTREZZI_ACCESSO_URL,
}
