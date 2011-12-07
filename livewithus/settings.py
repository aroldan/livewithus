from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
# Django settings for djsite project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# add your email address below to receive errors and stuff
ADMINS = (
#     ('Admin Name', 'adminemail@gmail.com'), 
)

MANAGERS = ADMINS

# default configuration
DATABASE_ENGINE = 'mysql'          
DATABASE_NAME = 'livewith'
DATABASE_USER = 'livewith'
DATABASE_PASSWORD = 'default'
DATABASE_HOST = ''
DATABASE_PORT = ''

# Default email setup -- change to fit your configuration
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'livewith_info'
EMAIL_HOST_PASSWORD = 'default'
EMAIL_SENDER = 'info@livewith.us'
#
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/srv/livewith_media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '//site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ccrcf(t^f(s$2x_b+8@_vm-_z!s2ykybq525i-y^y@814v!a0v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'djsite.urls'

APPEND_SLASH = True

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/livewith/webapps/django/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'djsite.helloworld',
    'livewith',
    'livewith.utilities',
    'livewith.utilities.dinner',
    'photologue',
    'south'
)

AUTHENTICATION_BACKENDS = (
    'livewith.email-auth.EmailBackend',
 )


AUTH_PROFILE_MODULE = 'alpha.Person'

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    "livewith.context_processors.currenthouse",
)

LIVE_SITE_PREFIX = "lw/" # prefix for all our active site URLs

LOGIN_URL = ("/%slogin" % LIVE_SITE_PREFIX) # where to redirect if not logged in
HOUSE_NEEDED_URL = ("/%shouse_required" % LIVE_SITE_PREFIX) # where to redirect if a house is req'd but none exists
PHOTOLOGUE_DIR = "uploads/avatars/"
AVATAR_PATH = MEDIA_ROOT + 'uploads/avatars/'
DEFAULT_AVATAR = "/site_media/img/blank_user_small.gif"
